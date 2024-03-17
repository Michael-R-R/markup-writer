#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
    pyqtSignal,
    QDataStream,
)
from PyQt6.QtGui import (
    QDragEnterEvent,
    QDropEvent,
    QKeyEvent,
    QMouseEvent,
)

from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QFrame,
)

from markupwriter.common.factory import TreeItemFactory
import markupwriter.gui.contextmenus.doctree as dt
import markupwriter.support.doctree.item as ti


class DocumentTreeWidget(QTreeWidget):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    filePreviewed = pyqtSignal(str, str)
    fileMoved = pyqtSignal(str, list)
    fileRenamed = pyqtSignal(str, str, str)
    dragDropDone = pyqtSignal()

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)

        self.draggedItems: list[QTreeWidgetItem] = list()
        self.treeContextMenu = dt.TreeContextMenu(self)
        self.itemContextMenu = dt.ItemContextMenu(self)
        self.trashContextMenu = dt.TrashContextMenu(self)

        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def add(self, widget: ti.BaseTreeItem):
        selected = self.currentItem()
        if selected is None:
            self.addTopLevelItem(widget.item)
        elif not widget.hasFlag(ti.ITEM_FLAG.draggable):
            self.addTopLevelItem(widget.item)
        else:
            selected.addChild(widget.item)

        self.setItemWidget(widget.item, 0, widget)
        self.expandItem(selected)
        self.setCurrentItem(widget.item)

        self._emitAdded(widget)

    def insertAt(
        self, index: int, item: QTreeWidgetItem, target: QTreeWidgetItem | None
    ):
        widgetList = self.takeOut(item)
        if target is None:  # insert to root
            self.insertTopLevelItem(index, item)
        else:  # insert to target
            target.insertChild(index, item)

        self.setWidgetList(widgetList)

        self._emitMoved(widgetList)

    def moveTo(self, item: QTreeWidgetItem, target: QTreeWidgetItem | None):
        widgetList = self.takeOut(item)
        if target is None:  # add to root
            self.addTopLevelItem(item)
        else:  # add to target
            target.addChild(item)

        self.setWidgetList(widgetList)
        self.setCurrentItem(item)

        self._emitMoved(widgetList)

    def remove(self, item: QTreeWidgetItem):
        for i in range(item.childCount() - 1, -1, -1):
            child = item.child(i)
            self.remove(child)

        widget: ti.BaseTreeItem = self.itemWidget(item, 0)

        parent = item.parent()
        if parent is None:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(item)

        self.removeItemWidget(item, 0)
        self.clearSelection()
        self.setCurrentItem(None)

        self._emitRemoved(widget)

    def rename(self, item: QTreeWidgetItem, name: str):
        widget: ti.BaseTreeItem = self.itemWidget(item, 0)
        if widget is None:
            return

        oldName = widget.title()
        widget.setTitle(name)

        if widget.hasFlag(ti.ITEM_FLAG.file):
            self.fileRenamed.emit(widget.UUID(), oldName, name)

    def translate(self, direction: int):
        selected = self.currentItem()
        if selected is None:
            return

        parent = selected.parent()
        if parent is None:  # root index
            size = self.topLevelItemCount()
            index = self.indexFromItem(selected, 0).row()
            self.insertAt((index + direction) % size, selected, parent)
        else:  # child index
            size = parent.childCount()
            index = parent.indexOfChild(selected)
            self.insertAt((index + direction) % size, selected, parent)

        self.setCurrentItem(selected)

    def takeOut(self, item: QTreeWidgetItem) -> list[ti.BaseTreeItem]:
        widgetList = self.copyWidgets(item, list())
        parent = item.parent()
        if parent is None:  # is root item
            index = self.indexFromItem(item, 0).row()
            item = self.takeTopLevelItem(index)
        else:  # is child item
            index = parent.indexOfChild(item)
            item = parent.takeChild(index)

        return widgetList

    def copyWidgets(
        self, pItem: QTreeWidgetItem, itemList: list[ti.BaseTreeItem]
    ) -> list[ti.BaseTreeItem]:
        result = itemList

        for i in range(pItem.childCount()):
            cItem = pItem.child(i)
            result = self.copyWidgets(cItem, result)

        widget: ti.BaseTreeItem = self.itemWidget(pItem, 0)
        result.append(widget.shallowcopy())

        return result

    def buildExportList(self, root: QTreeWidgetItem) -> list[list[ti.BaseFileItem]]:
        def helper(
            pitem: QTreeWidgetItem, flist: list[ti.BaseFileItem]
        ) -> list[ti.BaseFileItem]:
            pw: ti.BaseTreeItem = self.itemWidget(pitem, 0)

            if pw.hasFlag(ti.ITEM_FLAG.file):
                flist.append(pw)

            for i in range(pitem.childCount()):
                citem = pitem.child(i)
                flist = helper(citem, flist)

            return flist

        # End helper

        buildList: list[list[ti.BaseFileItem]] = list()
        for i in range(root.childCount()):
            pitem = root.child(i)
            buildList.append(helper(pitem, list()))

        return buildList

    def refreshParentWordCounts(self, child: QTreeWidgetItem, owc: int, wc: int):
        item = child.parent()
        while item is not None:
            widget: ti.BaseTreeItem = self.itemWidget(item, 0)
            twc = widget.totalWordCount() - owc + wc
            widget.setTotalWordCount(twc)
            item = item.parent()
        
    def refreshAllWordCounts(self):
        def helper(pitem: QTreeWidgetItem) -> int:
            pw: ti.BaseTreeItem = self.itemWidget(pitem, 0)
            twc = pw.wordCount()

            for j in range(pitem.childCount()):
                citem = pitem.child(j)
                twc += helper(citem)

            pw.setTotalWordCount(twc)

            return twc

        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            helper(item)
            
    def findTrashFolder(self) -> QTreeWidgetItem | None:
        for i in range(self.topLevelItemCount() - 1, -1, -1):
            item = self.topLevelItem(i)
            widget = self.itemWidget(item, 0)
            if isinstance(widget, ti.TrashFolderItem):
                return item

        return None
            
    def isInTrash(self, item: QTreeWidgetItem) -> bool:
        trash = self.findTrashFolder()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash

    def findWidget(self, uuid: str) -> ti.BaseTreeItem | None:
        def helper(item: QTreeWidgetItem) -> ti.BaseTreeItem | None:
            for i in range(item.childCount()):
                child = item.child(i)
                widget: ti.BaseTreeItem = self.itemWidget(child, 0)
                if widget.UUID() == uuid:
                    return widget
                widget = helper(child)
                if widget is not None:
                    return widget

            return None
        
        # End helper

        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            widget: ti.BaseTreeItem = self.itemWidget(item, 0)
            if widget.UUID() == uuid:
                return widget
            widget = helper(item)
            if widget is not None:
                return widget

        return None

    def getNamesList(self, item: QTreeWidgetItem) -> list[str]:
        nameList: list[str] = list()
        iTemp = item
        while iTemp is not None:
            wTemp: ti.BaseTreeItem = self.itemWidget(iTemp, 0)
            nameList.insert(0, wTemp.title())
            iTemp = iTemp.parent()
        return nameList

    def setWidgetList(self, items: list[ti.BaseTreeItem]):
        for i in items:
            self.setItemWidget(i.item, 0, i)

    def navigateTree(self, direction: int):
        index = self.currentIndex()
        
        selected = None
        if direction < 0:
            selected = self.indexAbove(index)
        elif direction > 0:
            selected = self.indexBelow(index)
        
        if selected == self.rootIndex():
            return
        
        self.setCurrentIndex(selected)
        self.setExpanded(selected, True)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        match e.key():
            case Qt.Key.Key_W:
                self.navigateTree(-1)
            case Qt.Key.Key_S:
                self.navigateTree(1)
            case Qt.Key.Key_O:
                self._emitOpened(self.currentItem())
            case Qt.Key.Key_P:
                self._emitPreviewed(self.currentItem())
            case _:
                return super().keyPressEvent(e)

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        index = self.indexAt(e.pos())
        super().mousePressEvent(e)
        if not index.isValid():
            self.clearSelection()

    def dragEnterEvent(self, e: QDragEnterEvent | None) -> None:
        self.draggedItems.clear()
        sList = self.selectedItems()
        for s in sList:
            widget: ti.BaseTreeItem = self.itemWidget(s, 0)
            if not widget.hasFlag(ti.ITEM_FLAG.draggable):
                self.draggedItems.clear()
                return
            self.draggedItems.append(s)

        super().dragEnterEvent(e)

    def dropEvent(self, e: QDropEvent | None) -> None:
        if not self.currentIndex().isValid():
            return

        copyList: list[list[ti.BaseTreeItem]] = list()
        for s in self.draggedItems:
            copyList.append(self.copyWidgets(s, list()))

        super().dropEvent(e)

        for i in range(len(copyList)):
            clist = copyList[i]
            self.setWidgetList(clist)

            item = self.draggedItems[i]
            item.setSelected(True)
            self.expandItem(item.parent())

        for clist in copyList:
            self._emitMoved(clist)

        self.draggedItems.clear()
        self.dragDropDone.emit()

    @pyqtSlot(QTreeWidgetItem, int)
    def onItemDoubleClicked(self, item: QTreeWidgetItem, _: int):
        if item is None:
            return
        
        self._emitOpened(item)

    def _emitAdded(self, widget: ti.BaseTreeItem):
        if widget.hasFlag(ti.ITEM_FLAG.file):
            nameList = self.getNamesList(widget.item)
            self.fileAdded.emit(widget.UUID())
            self.fileOpened.emit(widget.UUID(), nameList)

    def _emitRemoved(self, widget: ti.BaseTreeItem):
        if widget.hasFlag(ti.ITEM_FLAG.file):
            self.fileRemoved.emit(widget.title(), widget.UUID())

    def _emitMoved(self, widgetList: list[ti.BaseTreeItem]):
        for w in widgetList:
            if w.hasFlag(ti.ITEM_FLAG.file):
                nameList = self.getNamesList(w.item)
                self.fileMoved.emit(w.UUID(), nameList)

    def _emitOpened(self, item: QTreeWidgetItem):
        widget: ti.BaseTreeItem = self.itemWidget(item, 0)
        if widget.hasFlag(ti.ITEM_FLAG.file):
            nameList = self.getNamesList(item)
            self.fileOpened.emit(widget.UUID(), nameList)

    def _emitPreviewed(self, item: QTreeWidgetItem):
        widget: ti.BaseTreeItem = self.itemWidget(item, 0)
        if widget is None:
            return
        
        if not widget.hasFlag(ti.ITEM_FLAG.file):
            return
        
        self.filePreviewed.emit(widget.title(), widget.UUID())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:

        # recursive helper
        def helper(sOut: QDataStream, iParent: QTreeWidgetItem):
            cCount = iParent.childCount()
            sOut.writeInt(cCount)

            for i in range(cCount):
                iChild = iParent.child(i)
                wChild: ti.BaseTreeItem = self.itemWidget(iChild, 0)
                sOut.writeQString(wChild.__class__.__name__)
                sout.writeBool(iChild.isExpanded())
                helper(sOut, iChild)
                sOut << wChild
                
        # End helper

        iCount = self.topLevelItemCount()
        sout.writeInt(iCount)

        # Top level items
        for i in range(iCount):
            iParent = self.topLevelItem(i)
            wParent: ti.BaseTreeItem = self.itemWidget(iParent, 0)
            sout.writeQString(wParent.__class__.__name__)
            sout.writeBool(iParent.isExpanded())
            sout << wParent

            # Child level items
            helper(sout, iParent)

        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:

        # recursive helper
        def helper(sin: QDataStream, iParent: QTreeWidgetItem):
            cCount = sin.readInt()

            for _ in range(cCount):
                type = sin.readQString()
                isExpanded = sin.readBool()
                cwidget: ti.BaseTreeItem = TreeItemFactory.make(type)
                helper(sin, cwidget.item)
                sin >> cwidget

                iParent.addChild(cwidget.item)
                self.setItemWidget(cwidget.item, 0, cwidget)
                
                if isExpanded:
                    self.expandItem(cwidget.item)
                
        # End helper

        iCount = sin.readInt()

        # Top level items
        for _ in range(iCount):
            type = sin.readQString()
            isExpanded = sin.readBool()
            pwidget: ti.BaseTreeItem = TreeItemFactory.make(type)
            sin >> pwidget

            # Child level items
            helper(sin, pwidget.item)

            self.addTopLevelItem(pwidget.item)
            self.setItemWidget(pwidget.item, 0, pwidget)
            
            if isExpanded:
                self.expandItem(pwidget.item)

        return sin
