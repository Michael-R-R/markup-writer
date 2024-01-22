#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
    pyqtSignal,
    QDataStream,
    QPoint,
)
from PyQt6.QtGui import (
    QDragEnterEvent,
    QDropEvent,
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
import markupwriter.support.doctree.item as dti


class DocumentTreeWidget(QTreeWidget):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.draggedItem = None
        self.treeContextMenu = dt.TreeContextMenu(self)
        self.itemContextMenu = dt.ItemContextMenu(self)
        self.trashContextMenu = dt.TrashContextMenu(self)

        self.customContextMenuRequested.connect(self._onCustomContextMenu)
        self.itemDoubleClicked.connect(self._onItemDoubleClicked)

    def add(self, widget: dti.BaseTreeItem):
        selected = self.currentItem()
        if selected is None:
            self.addTopLevelItem(widget.item)
        elif not widget.hasFlag(dti.ITEM_FLAG.draggable):
            self.addTopLevelItem(widget.item)
        else:
            selected.addChild(widget.item)

        self.setItemWidget(widget.item, 0, widget)
        self.expandItem(selected)
        self.setCurrentItem(widget.item)

        self._emitAdded(widget)

    def remove(self, item: QTreeWidgetItem):
        for i in range(item.childCount() - 1, -1, -1):
            child = item.child(i)
            self.remove(child)

        widget: dti.BaseTreeItem = self.itemWidget(item, 0)
        self._emitRemoved(widget)

        parent = item.parent()
        if parent is None:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(item)

        self.removeItemWidget(item, 0)
        self.clearSelection()
        self.setCurrentItem(None)
        
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

    def moveTo(self, item: QTreeWidgetItem, target: QTreeWidgetItem | None):
        widgetList = self.takeOut(item)
        if target is None:  # add to root
            self.addTopLevelItem(item)
        else:  # add to target
            target.addChild(item)

        self.setWidgetList(widgetList)
        self.setCurrentItem(item)

        self._emitMoved(widgetList)

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

    def takeOut(self, item: QTreeWidgetItem) -> list[dti.BaseTreeItem]:
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
        self, pItem: QTreeWidgetItem, itemList: list[dti.BaseTreeItem]
    ) -> list[dti.BaseTreeItem]:
        result = itemList

        for i in range(pItem.childCount()):
            cItem = pItem.child(i)
            result = self.copyWidgets(cItem, result)

        widget: dti.BaseTreeItem = self.itemWidget(pItem, 0)
        result.append(widget.shallowcopy())

        return result

    def findTrash(self) -> QTreeWidgetItem | None:
        for i in range(self.topLevelItemCount() - 1, -1, -1):
            item = self.topLevelItem(i)
            widget = self.itemWidget(item, 0)
            if isinstance(widget, dti.TrashFolderItem):
                return item

        return None
    
    def findWidget(self, uuid: str) -> dti.BaseTreeItem | None:
        def helper(item: QTreeWidgetItem) -> dti.BaseTreeItem | None:
            for i in range(item.childCount()):
                child = item.child(i)
                widget: dti.BaseTreeItem = self.itemWidget(child, 0)
                if widget.UUID() == uuid:
                    return widget
                widget = helper(child)
                if widget is not None:
                    return widget
            
            return None
        
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            widget: dti.BaseTreeItem = self.itemWidget(item, 0)
            if widget.UUID() == uuid:
                return widget
            widget = helper(item)
            if widget is not None:
                return widget
        
        return None

    def isInTrash(self, item: QTreeWidgetItem) -> bool:
        trash = self.findTrash()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash

    def getParentNameList(self, item: QTreeWidgetItem) -> list[str]:
        nameList: list[str] = list()
        iTemp = item
        while iTemp is not None:
            wTemp: dti.BaseTreeItem = self.itemWidget(iTemp, 0)
            nameList.insert(0, wTemp.title())
            iTemp = iTemp.parent()
        return nameList

    def setWidgetList(self, items: list[dti.BaseTreeItem]):
        for i in items:
            self.setItemWidget(i.item, 0, i)

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        index = self.indexAt(e.pos())
        super().mousePressEvent(e)
        if not index.isValid():
            self.clearSelection()
            self.setCurrentItem(None)

    def dragEnterEvent(self, e: QDragEnterEvent | None) -> None:
        selected = self.currentItem()
        widget: dti.BaseTreeItem = self.itemWidget(selected, 0)
        if not widget.hasFlag(dti.ITEM_FLAG.draggable):
            return

        self.draggedItem = selected

        super().dragEnterEvent(e)

    def dropEvent(self, e: QDropEvent | None) -> None:
        if not self.currentIndex().isValid():
            return

        item = self.draggedItem
        if item is None:
            return

        widgetList = self.copyWidgets(item, list())
        super().dropEvent(e)
        self.setWidgetList(widgetList)
        self.setCurrentItem(item)
        self.expandItem(item)

        self.draggedItem = None

        self._emitMoved(widgetList)
                
    def _emitAdded(self, widget: dti.BaseTreeItem):
        if widget.hasFlag(dti.ITEM_FLAG.file):
            nameList = self.getParentNameList(widget.item)
            self.fileAdded.emit(widget.UUID())
            self.fileOpened.emit(widget.UUID(), nameList)    
            
    def _emitRemoved(self, widget: dti.BaseTreeItem):
        if widget.hasFlag(dti.ITEM_FLAG.file):
            self.fileRemoved.emit(widget.UUID())
                
    def _emitMoved(self, widgetList: list[dti.BaseTreeItem]):
        for w in widgetList:
            if w.hasFlag(dti.ITEM_FLAG.file):
                nameList = self.getParentNameList(w.item)
                self.fileMoved.emit(w.UUID(), nameList)

    @pyqtSlot(QPoint)
    def _onCustomContextMenu(self, pos: QPoint):
        item = self.itemAt(pos)
        widget: dti.BaseTreeItem = self.itemWidget(item, 0)
        pos = self.mapToGlobal(pos)
        if item is None:
            self.treeContextMenu.onShowMenu(pos)
        elif isinstance(widget, dti.TrashFolderItem):
            isEmpty = item.childCount() < 1
            args = [isEmpty]
            self.trashContextMenu.onShowMenu(pos, args)
        else:
            isFile = widget.hasFlag(dti.ITEM_FLAG.file)
            inTrash = self.isInTrash(item)
            isMutable = widget.hasFlag(dti.ITEM_FLAG.mutable)
            args = [isFile, inTrash, isMutable]
            self.itemContextMenu.onShowMenu(pos, args)

    @pyqtSlot(QTreeWidgetItem, int)
    def _onItemDoubleClicked(self, item: QTreeWidgetItem, col: int):
        widget: dti.BaseTreeItem = self.itemWidget(item, col)
        if widget.hasFlag(dti.ITEM_FLAG.file):
            nameList = self.getParentNameList(item)
            self.fileOpened.emit(widget.UUID(), nameList)
            
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        
        # recursive helper
        def helper(sOut: QDataStream, iParent: QTreeWidgetItem):
            cCount = iParent.childCount()
            sOut.writeInt(cCount)

            for i in range(cCount):
                iChild = iParent.child(i)
                wChild: dti.BaseTreeItem = self.itemWidget(iChild, 0)
                sOut.writeQString(wChild.__class__.__name__)
                helper(sOut, iChild)
                sOut << wChild
        
        iCount = self.topLevelItemCount()
        sout.writeInt(iCount)

        # Top level items
        for i in range(iCount):
            iParent = self.topLevelItem(i)
            wParent: dti.BaseTreeItem = self.itemWidget(iParent, 0)
            sout.writeQString(wParent.__class__.__name__)
            sout << wParent

            # Child level items
            helper(sout, iParent)

        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        
        # recursive helper
        def helper(sIn: QDataStream, iParent: QTreeWidgetItem):
            cCount = sIn.readInt()

            for _ in range(cCount):
                type = sIn.readQString()
                wChild: dti.BaseTreeItem = TreeItemFactory.make(type)
                helper(sIn, wChild.item)
                sIn >> wChild

                iParent.addChild(wChild.item)
                self.setItemWidget(wChild.item, 0, wChild)
        
        iCount = sin.readInt()

        # Top level items
        for i in range(iCount):
            type = sin.readQString()
            wParent: dti.BaseTreeItem = TreeItemFactory.make(type)
            sin >> wParent

            # Child level items
            helper(sin, wParent.item)

            self.addTopLevelItem(wParent.item)
            self.setItemWidget(wParent.item, 0, wParent)

        return sin
