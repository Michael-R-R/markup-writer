#!/usr/bin/python

import re

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


class Node(object):
    def __init__(self, item: QTreeWidgetItem, widget: dti.BaseTreeItem) -> None:
        self.item = item
        self.widget = widget
        self.children: list[Node] = list()


class DocumentTreeWidget(QTreeWidget):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
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

        self.treeCopy: list[Node] = list()
        self.draggedItems: list[QTreeWidgetItem] = list()
        self.treeContextMenu = dt.TreeContextMenu(self)
        self.itemContextMenu = dt.ItemContextMenu(self)
        self.trashContextMenu = dt.TrashContextMenu(self)

        self.customContextMenuRequested.connect(self._onCustomContextMenu)
        self.itemDoubleClicked.connect(self._onItemDoubleClicked)

    def add(self, item: QTreeWidgetItem, widget: dti.BaseTreeItem):
        selected = self.currentItem()

        if selected is None:
            self.addTopLevelItem(item)
        elif not widget.hasFlag(dti.ITEM_FLAG.draggable):
            self.addTopLevelItem(item)
        else:
            selected.addChild(item)

        self.setItemWidget(item, 0, widget)
        self.expandItem(selected)
        self.setCurrentItem(item)

        self._emitAdded(item)

    def remove(self, item: QTreeWidgetItem):
        for i in range(item.childCount() - 1, -1, -1):
            child = item.child(i)
            self.remove(child)

        widget: dti.BaseTreeItem = self.itemWidget(item, 0)

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

    def moveInsert(
        self, index: int, item: QTreeWidgetItem, target: QTreeWidgetItem | None
    ):
        widgetList = self.takeOut(item)

        if target is None:  # insert to root
            self.insertTopLevelItem(index, item)
        else:  # insert to target
            target.insertChild(index, item)

        self.setWidgetList(widgetList)

        self._emitMoved(widgetList)

    def moveAppend(self, item: QTreeWidgetItem, target: QTreeWidgetItem | None):
        widgetList = self.takeOut(item)

        if target is None:  # add to root
            self.addTopLevelItem(item)
        else:  # add to target
            target.addChild(item)

        self.setWidgetList(widgetList)
        self.setCurrentItem(item)

        self._emitMoved(widgetList)

    def translate(self, direction: int):
        selected = self.currentItem()
        if selected is None:
            return

        parent = selected.parent()
        if parent is None:  # root index
            size = self.topLevelItemCount()
            index = self.indexFromItem(selected, 0).row()
            self.moveInsert((index + direction) % size, selected, parent)
        else:  # child index
            size = parent.childCount()
            index = parent.indexOfChild(selected)
            self.moveInsert((index + direction) % size, selected, parent)

        self.setCurrentItem(selected)

    def takeOut(
        self, item: QTreeWidgetItem
    ) -> list[(QTreeWidgetItem, dti.BaseTreeItem)]:
        widgetList = self.mkWidgetCopies(item, list())

        parent = item.parent()
        if parent is None:  # is root item
            index = self.indexFromItem(item, 0).row()
            item = self.takeTopLevelItem(index)
        else:  # is child item
            index = parent.indexOfChild(item)
            item = parent.takeChild(index)

        return widgetList

    def mkWidgetCopies(
        self,
        pItem: QTreeWidgetItem,
        itemList: list[(QTreeWidgetItem, dti.BaseTreeItem)],
    ) -> list[(QTreeWidgetItem, dti.BaseTreeItem)]:
        result = itemList

        for i in range(pItem.childCount()):
            cItem = pItem.child(i)
            result = self.mkWidgetCopies(cItem, result)

        widget: dti.BaseTreeItem = self.itemWidget(pItem, 0)
        result.append((pItem, widget.deepcopy()))

        return result

    def deepCopyTree(self) -> list[Node]:
        result = list()

        def helper(pitem: QTreeWidgetItem) -> Node:
            pwidget: dti.BaseTreeItem = self.itemWidget(pitem, 0)
            node = Node(QTreeWidgetItem(), pwidget.deepcopy())

            for i in range(pitem.childCount()):
                citem = pitem.child(i)
                node.children.append(helper(citem))

            return node

        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            result.append(helper(item))

        return result

    def restoreTreeFrom(self, nodes: list[Node]):
        self.clear()

        def helper(pnode: Node):
            for cnode in pnode.children:
                pitem = pnode.item
                pitem.addChild(cnode.item)
                self.setItemWidget(cnode.item, 0, cnode.widget)
                helper(cnode)

        for node in nodes:
            self.addTopLevelItem(node.item)
            self.setItemWidget(node.item, 0, node.widget)
            helper(node)

    def filterItems(self, text: str):
        # TODO fix original widgets not being changed
        # I.E: word count, renames, etc.

        if text == "":
            self.restoreTreeFrom(self.treeCopy)
            self.treeCopy = list()
            return

        if len(self.treeCopy) <= 0:
            self.treeCopy = self.deepCopyTree()

        self.clear()

        # add items that fit the match
        regex = re.compile(text)

        def helper(pnode: Node):
            for cnode in pnode.children:
                title = cnode.widget.title()
                found = regex.search(title)
                if found is not None:
                    item = QTreeWidgetItem()
                    self.addTopLevelItem(item)
                    self.setItemWidget(item, 0, cnode.widget.deepcopy())
                helper(cnode)

        for node in self.treeCopy:
            title = node.widget.title()
            found = regex.search(title)
            if found is not None:
                item = QTreeWidgetItem()
                self.addTopLevelItem(item)
                self.setItemWidget(item, 0, node.widget.deepcopy())
            helper(node)

    def rename(self, item: QTreeWidgetItem, name: str):
        widget: dti.BaseTreeItem = self.itemWidget(item, 0)
        if widget is None:
            return

        oldName = widget.title()
        widget.setTitle(name)

        if widget.hasFlag(dti.ITEM_FLAG.file):
            self.fileRenamed.emit(widget.UUID(), oldName, name)

    def refreshWordCounts(self, item: QTreeWidgetItem, owc: int, wc: int):
        while item is not None:
            widget: dti.BaseTreeItem = self.itemWidget(item, 0)
            twc = widget.totalWordCount() - owc + wc
            widget.setTotalWordCount(twc)
            item = item.parent()

    def refreshAllWordCounts(self):

        def helper(pitem: QTreeWidgetItem) -> int:
            pw: dti.BaseTreeItem = self.itemWidget(pitem, 0)
            twc = pw.wordCount()

            for j in range(pitem.childCount()):
                citem = pitem.child(j)
                twc += helper(citem)

            pw.setTotalWordCount(twc)

            return twc

        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            helper(item)

    def buildExportList(self, root: QTreeWidgetItem) -> list[list[dti.BaseFileItem]]:

        def helper(
            pitem: QTreeWidgetItem, flist: list[dti.BaseFileItem]
        ) -> list[dti.BaseFileItem]:
            pw: dti.BaseTreeItem = self.itemWidget(pitem, 0)

            if pw.hasFlag(dti.ITEM_FLAG.file):
                flist.append(pw)

            for i in range(pitem.childCount()):
                citem = pitem.child(i)
                flist = helper(citem, flist)

            return flist

        buildList: list[list[dti.BaseFileItem]] = list()
        for i in range(root.childCount()):
            pitem = root.child(i)
            buildList.append(helper(pitem, list()))

        return buildList

    def findTrash(self) -> QTreeWidgetItem | None:
        for i in range(self.topLevelItemCount() - 1, -1, -1):
            item = self.topLevelItem(i)
            widget = self.itemWidget(item, 0)
            if isinstance(widget, dti.TrashFolderItem):
                return item

        return None

    def findItem(self, uuid: str) -> QTreeWidgetItem | None:

        def helper(item: QTreeWidgetItem) -> QTreeWidgetItem | None:
            for i in range(item.childCount()):
                child = item.child(i)
                widget: dti.BaseTreeItem = self.itemWidget(child, 0)
                if widget.UUID() == uuid:
                    return child

                found = helper(child)
                if found is not None:
                    return found

            return None

        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            widget: dti.BaseTreeItem = self.itemWidget(item, 0)
            if widget.UUID() == uuid:
                return item

            found = helper(item)
            if found is not None:
                return found

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

    def setWidgetList(self, pairs: list[(QTreeWidgetItem, dti.BaseTreeItem)]):
        for p in pairs:
            self.setItemWidget(p[0], 0, p[1])

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        index = self.indexAt(e.pos())
        super().mousePressEvent(e)
        if not index.isValid():
            self.clearSelection()
            self.setCurrentItem(None)

    def dragEnterEvent(self, e: QDragEnterEvent | None) -> None:
        self.draggedItems.clear()
        sList = self.selectedItems()
        for s in sList:
            widget: dti.BaseTreeItem = self.itemWidget(s, 0)
            if not widget.hasFlag(dti.ITEM_FLAG.draggable):
                self.draggedItems.clear()
                return
            self.draggedItems.append(s)

        super().dragEnterEvent(e)

    def dropEvent(self, e: QDropEvent | None) -> None:
        if not self.currentIndex().isValid():
            return

        copyList: list[list[(QTreeWidgetItem, dti.BaseTreeItem)]] = list()
        for item in self.draggedItems:
            copyList.append(self.mkWidgetCopies(item, list()))

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

    def _emitAdded(self, item: QTreeWidgetItem):
        widget: dti.BaseTreeItem = self.itemWidget(item, 0)
        if widget is None:
            return
        if widget.hasFlag(dti.ITEM_FLAG.file):
            nameList = self.getParentNameList(item)
            self.fileAdded.emit(widget.UUID())
            self.fileOpened.emit(widget.UUID(), nameList)

    def _emitRemoved(self, widget: dti.BaseTreeItem):
        if widget.hasFlag(dti.ITEM_FLAG.file):
            self.fileRemoved.emit(widget.title(), widget.UUID())

    def _emitMoved(self, pairList: list[(QTreeWidgetItem, dti.BaseTreeItem)]):
        for p in pairList:
            widget: dti.BaseTreeItem = p[1]
            if widget.hasFlag(dti.ITEM_FLAG.file):
                nameList = self.getParentNameList(p[0])
                self.fileMoved.emit(widget.UUID(), nameList)

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
            pitem = self.topLevelItem(i)
            pwidget: dti.BaseTreeItem = self.itemWidget(pitem, 0)
            sout.writeQString(pwidget.__class__.__name__)
            sout << pwidget

            # Child level items
            helper(sout, pitem)

        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        # recursive helper
        def helper(sIn: QDataStream, pitem: QTreeWidgetItem):
            cCount = sIn.readInt()

            for _ in range(cCount):
                type = sIn.readQString()
                item = QTreeWidgetItem()
                cwidget: dti.BaseTreeItem = TreeItemFactory.make(type)
                helper(sIn, item)
                sIn >> cwidget

                pitem.addChild(item)
                self.setItemWidget(item, 0, cwidget)

                self.fileAdded.emit(cwidget.UUID())

        iCount = sin.readInt()

        # Top level items
        for i in range(iCount):
            type = sin.readQString()
            item = QTreeWidgetItem()
            pwidget: dti.BaseTreeItem = TreeItemFactory.make(type)
            sin >> pwidget

            # Child level items
            helper(sin, item)

            self.addTopLevelItem(item)
            self.setItemWidget(item, 0, pwidget)

            self.fileAdded.emit(pwidget.UUID())

        return sin
