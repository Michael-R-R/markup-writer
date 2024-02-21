#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
    pyqtSignal,
    QDataStream,
    QPoint,
    QModelIndex,
)
from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QDragEnterEvent,
    QDropEvent,
    QMouseEvent,
)

from PyQt6.QtWidgets import (
    QTreeView,
    QWidget,
    QFrame,
    QAbstractItemView,
)

from markupwriter.common.factory import TreeItemFactory
import markupwriter.gui.contextmenus.doctree as dt
import markupwriter.support.doctree.item as dti


class DocumentTreeWidget(QTreeView):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)
    fileRenamed = pyqtSignal(str, str, str)
    dragDropDone = pyqtSignal()

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.dataModel = QStandardItemModel(self)
        self.setModel(self.dataModel)

        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setDragDropMode(QTreeView.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)

        self.draggedItems: list[QStandardItem] = list()
        self.treeContextMenu = dt.TreeContextMenu(self)
        self.itemContextMenu = dt.ItemContextMenu(self)
        self.trashContextMenu = dt.TrashContextMenu(self)

        self.customContextMenuRequested.connect(self._onCustomContextMenu)
        self.doubleClicked.connect(self._onItemDoubleClicked)

    def add(self, widget: dti.BaseTreeItem):
        index = self.currentIndex()
        selected = self.dataModel.itemFromIndex(index)
        if selected is None:
            self.dataModel.appendRow(widget.item)
        elif not widget.hasFlag(dti.ITEM_FLAG.draggable):
            self.dataModel.appendRow(widget.item)
        else:
            selected.appendRow(widget.item)

        index = self.dataModel.indexFromItem(widget.item)
        self.setIndexWidget(index, widget)
        self.expand(index)
        self.setCurrentIndex(index)

        self._emitAdded(widget)

    def insertMove(self, index: int, item: QStandardItem, target: QStandardItem | None):
        if index < 0:
            index = 0

        widgetList = self.takeOut(item)
        if target is None:  # insert to root
            if index > self.dataModel.rowCount():
                index = self.dataModel.rowCount()
            self.dataModel.insertRow(index, item)
        else:  # insert to target
            if index > target.rowCount():
                index = target.rowCount()
            target.insertRow(index, item)

        index = self.dataModel.indexFromItem(item)
        self.setWidgetList(widgetList)
        self.setCurrentIndex(index)
        self._emitMoved(widgetList)

    def appendMove(self, item: QStandardItem, target: QStandardItem | None):
        widgetList = self.takeOut(item)
        if target is None:  # add to root
            self.dataModel.appendRow(item)
        else:  # add to target
            target.appendRow(item)

        index = self.dataModel.indexFromItem(item)
        self.setWidgetList(widgetList)
        self.setCurrentIndex(index)
        self._emitMoved(widgetList)

    def remove(self, item: QStandardItem):
        for i in range(item.rowCount() - 1, -1, -1):
            child = item.child(i)
            self.remove(child)

        index = self.dataModel.indexFromItem(item)
        widget: dti.BaseTreeItem = self.indexWidget(index)

        parent = item.parent()
        if parent is None:
            self.dataModel.takeRow(index.row())
        else:
            parent.takeRow(index.row())

        self.clearSelection()

        self._emitRemoved(widget)

    def rename(self, item: QStandardItem, name: str):
        index = self.dataModel.indexFromItem(item)
        widget: dti.BaseTreeItem = self.indexWidget(index)
        if widget is None:
            return

        oldName = widget.title()
        widget.setTitle(name)

        if widget.hasFlag(dti.ITEM_FLAG.file):
            self.fileRenamed.emit(widget.UUID(), oldName, name)

    def translate(self, direction: int):
        row = self.currentIndex()
        selected = self.dataModel.itemFromIndex(row)
        if selected is None:
            return

        parent = selected.parent()
        if parent is None:  # root index
            size = self.dataModel.rowCount()
            index = self.dataModel.indexFromItem(selected)
            row = index.row()
            self.insertMove((row + direction) % size, selected, parent)
        else:  # child index
            size = parent.rowCount()
            index = self.dataModel.indexFromItem(selected)
            row = index.row()
            self.insertMove((row + direction) % size, selected, parent)

        index = self.dataModel.indexFromItem(selected)
        self.setCurrentIndex(index)

    def filter(self, text: str):
        # TODO implement
        pass

    def takeOut(self, item: QStandardItem) -> list[dti.BaseTreeItem]:
        widgetList = self.copyWidgets(item, list())
        parent = item.parent()
        if parent is None:  # is root item
            index = self.dataModel.indexFromItem(item)
            item = self.dataModel.takeRow(index.row())
        else:  # is child item
            index = self.dataModel.indexFromItem(item)
            item = parent.takeRow(index.row())

        return widgetList

    def copyWidgets(
        self, pItem: QStandardItem, itemList: list[dti.BaseTreeItem]
    ) -> list[dti.BaseTreeItem]:
        result = itemList

        for i in range(pItem.rowCount()):
            cItem = pItem.child(i)
            result = self.copyWidgets(cItem, result)

        index = self.dataModel.indexFromItem(pItem)
        widget: dti.BaseTreeItem = self.indexWidget(index)
        result.append(widget.shallowcopy())

        return result

    def refreshWordCounts(self, item: QStandardItem, owc: int, wc: int):
        while item is not None:
            index = self.dataModel.indexFromItem(item)
            widget: dti.BaseTreeItem = self.indexWidget(index)
            twc = widget.totalWordCount() - owc + wc
            widget.setTotalWordCount(twc)
            item = item.parent()

    def refreshAllWordCounts(self):
        def helper(pitem: QStandardItem) -> int:
            index = self.dataModel.indexFromItem(pitem)
            pw: dti.BaseTreeItem = self.indexWidget(index)
            twc = pw.wordCount()

            for j in range(pitem.rowCount()):
                citem = pitem.child(j)
                twc += helper(citem)

            pw.setTotalWordCount(twc)

            return twc

        for i in range(self.dataModel.rowCount()):
            item = self.dataModel.item(i)
            helper(item)

    def buildExportList(self, root: QStandardItem) -> list[list[dti.BaseFileItem]]:

        def helper(
            pitem: QStandardItem, flist: list[dti.BaseFileItem]
        ) -> list[dti.BaseFileItem]:
            index = self.dataModel.indexFromItem(pitem)
            pw: dti.BaseTreeItem = self.indexWidget(index)

            if pw.hasFlag(dti.ITEM_FLAG.file):
                flist.append(pw)

            for i in range(pitem.rowCount()):
                citem = pitem.child(i)
                flist = helper(citem, flist)

            return flist

        buildList: list[list[dti.BaseFileItem]] = list()
        for i in range(root.rowCount()):
            pitem = root.child(i)
            buildList.append(helper(pitem, list()))

        return buildList

    def findTrash(self) -> QStandardItem | None:
        for i in range(self.dataModel.rowCount() - 1, -1, -1):
            item = self.dataModel.item(i)
            index = self.dataModel.indexFromItem(item)
            widget = self.indexWidget(index)
            if isinstance(widget, dti.TrashFolderItem):
                return item

        return None

    def findWidget(self, uuid: str) -> dti.BaseTreeItem | None:

        def helper(item: QStandardItem) -> dti.BaseTreeItem | None:
            for i in range(item.rowCount()):
                child = item.child(i)
                index = self.dataModel.indexFromItem(child)
                widget: dti.BaseTreeItem = self.indexWidget(index)
                if widget.UUID() == uuid:
                    return widget
                widget = helper(child)
                if widget is not None:
                    return widget

            return None

        for i in range(self.dataModel.rowCount()):
            item = self.dataModel.item(i)
            index = self.dataModel.indexFromItem(item)
            widget: dti.BaseTreeItem = self.indexWidget(index)
            if widget.UUID() == uuid:
                return widget
            widget = helper(item)
            if widget is not None:
                return widget

        return None

    def isInTrash(self, item: QStandardItem) -> bool:
        trash = self.findTrash()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash

    def getParentNameList(self, item: QStandardItem) -> list[str]:
        nameList: list[str] = list()
        iTemp = item
        while iTemp is not None:
            index = self.dataModel.indexFromItem(iTemp)
            wTemp: dti.BaseTreeItem = self.indexWidget(index)
            nameList.insert(0, wTemp.title())
            iTemp = iTemp.parent()
        return nameList

    def setWidgetList(self, items: list[dti.BaseTreeItem]):
        for widget in items:
            index = self.dataModel.indexFromItem(widget.item)
            self.setIndexWidget(index, widget)

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        index = self.indexAt(e.pos())
        super().mousePressEvent(e)
        if not index.isValid():
            self.clearSelection()

    def dragEnterEvent(self, e: QDragEnterEvent | None) -> None:
        indexes = self.selectedIndexes()
        for i in indexes:
            widget: dti.BaseTreeItem = self.indexWidget(i)
            if not widget.hasFlag(dti.ITEM_FLAG.draggable):
                self.draggedItems.clear()
                return
            item = self.dataModel.itemFromIndex(i)
            self.draggedItems.append(item)

        super().dragEnterEvent(e)

    def dropEvent(self, e: QDropEvent | None) -> None:
        pos = e.position()
        pos = QPoint(int(pos.x()), int(pos.y()))
        index = self.indexAt(pos)

        match self.dropIndicatorPosition():
            case self.DropIndicatorPosition.OnItem:
                target = self.dataModel.itemFromIndex(index)
                for item in self.draggedItems:
                    self.appendMove(item, target)
            case self.DropIndicatorPosition.AboveItem:
                targetRow = index.row()
                target = self.dataModel.itemFromIndex(index).parent()
                for item in self.draggedItems:
                    row = targetRow
                    if item.parent() == target:
                        row = targetRow if ((item.row() - targetRow) > -1) else targetRow - 1
                    self.insertMove(row, item, target)
            case self.DropIndicatorPosition.BelowItem:
                targetRow = index.row()
                target = self.dataModel.itemFromIndex(index).parent()
                for item in self.draggedItems:
                    row = targetRow
                    if item.parent() == target:
                        row = targetRow if ((targetRow - item.row()) > -1) else targetRow + 1
                    else:
                        row += 1
                    self.insertMove(row, item, target)
            case self.DropIndicatorPosition.OnViewport:
                for item in self.draggedItems:
                    self.appendMove(item, None)

        self.draggedItems.clear()

    def _emitAdded(self, widget: dti.BaseTreeItem):
        if widget.hasFlag(dti.ITEM_FLAG.file):
            nameList = self.getParentNameList(widget.item)
            self.fileAdded.emit(widget.UUID())
            self.fileOpened.emit(widget.UUID(), nameList)

    def _emitRemoved(self, widget: dti.BaseTreeItem):
        if widget.hasFlag(dti.ITEM_FLAG.file):
            self.fileRemoved.emit(widget.title(), widget.UUID())

    def _emitMoved(self, widgetList: list[dti.BaseTreeItem]):
        for w in widgetList:
            if w.hasFlag(dti.ITEM_FLAG.file):
                nameList = self.getParentNameList(w.item)
                self.fileMoved.emit(w.UUID(), nameList)

    @pyqtSlot(QPoint)
    def _onCustomContextMenu(self, pos: QPoint):
        index = self.indexAt(pos)
        item = self.dataModel.itemFromIndex(index)
        widget: dti.BaseTreeItem = self.indexWidget(index)
        pos = self.mapToGlobal(pos)
        if item is None:
            self.treeContextMenu.onShowMenu(pos)
        elif isinstance(widget, dti.TrashFolderItem):
            isEmpty = item.rowCount() < 1
            args = [isEmpty]
            self.trashContextMenu.onShowMenu(pos, args)
        else:
            isFile = widget.hasFlag(dti.ITEM_FLAG.file)
            inTrash = self.isInTrash(item)
            isMutable = widget.hasFlag(dti.ITEM_FLAG.mutable)
            args = [isFile, inTrash, isMutable]
            self.itemContextMenu.onShowMenu(pos, args)

    @pyqtSlot(QModelIndex)
    def _onItemDoubleClicked(self, index: QModelIndex):
        widget: dti.BaseTreeItem = self.indexWidget(index)
        if widget.hasFlag(dti.ITEM_FLAG.file):
            item = self.dataModel.itemFromIndex(index)
            nameList = self.getParentNameList(item)
            self.fileOpened.emit(widget.UUID(), nameList)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:

        # recursive helper
        def helper(sOut: QDataStream, iParent: QStandardItem):
            cCount = iParent.rowCount()
            sOut.writeInt(cCount)

            for i in range(cCount):
                iChild = iParent.child(i)
                index = self.dataModel.indexFromItem(iChild)
                wChild: dti.BaseTreeItem = self.indexWidget(index)
                sOut.writeQString(wChild.__class__.__name__)
                helper(sOut, iChild)
                sOut << wChild

        iCount = self.dataModel.rowCount()
        sout.writeInt(iCount)

        # Top level items
        for i in range(iCount):
            iParent = self.dataModel.item(i)
            index = self.dataModel.indexFromItem(iParent)
            wParent: dti.BaseTreeItem = self.indexWidget(index)
            sout.writeQString(wParent.__class__.__name__)
            sout << wParent

            # Child level items
            helper(sout, iParent)

        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:

        # recursive helper
        def helper(sIn: QDataStream, iParent: QStandardItem):
            cCount = sIn.readInt()

            for _ in range(cCount):
                type = sIn.readQString()
                cwidget: dti.BaseTreeItem = TreeItemFactory.make(type)
                helper(sIn, cwidget.item)
                sIn >> cwidget

                iParent.appendRow(cwidget.item)
                index = self.dataModel.indexFromItem(cwidget.item)
                self.setIndexWidget(index, cwidget)

                self.fileAdded.emit(cwidget.UUID())

        iCount = sin.readInt()

        # Top level items
        for i in range(iCount):
            type = sin.readQString()
            pwidget: dti.BaseTreeItem = TreeItemFactory.make(type)
            sin >> pwidget

            # Child level items
            helper(sin, pwidget.item)

            self.dataModel.appendRow(pwidget.item)
            index = self.dataModel.indexFromItem(pwidget.item)
            self.setIndexWidget(index, pwidget)

            self.fileAdded.emit(pwidget.UUID())

        return sin
