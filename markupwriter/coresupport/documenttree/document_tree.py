#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
    pyqtSignal,
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

from markupwriter.common.factory import (
    TreeItemFactory,
)

from .treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
    PlotFolderItem,
    TimelineFolderItem,
    CharsFolderItem,
    LocFolderItem,
    ObjFolderItem,
    TrashFolderItem,
)

import markupwriter.coresupport.documenttree as dt


class DocumentTree(QTreeWidget):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str)
    fileDoubleClicked = pyqtSignal(str)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.helper = dt.DocumentTreeHelper(self)
        self.draggedItem = None

        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setDragDropMode(self.DragDropMode.InternalMove)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.add(PlotFolderItem(), False)
        self.add(TimelineFolderItem(), False)
        self.add(CharsFolderItem(), False)
        self.add(LocFolderItem(), False)
        self.add(ObjFolderItem(), False)
        self.add(TrashFolderItem(), False)

        self.itemDoubleClicked.connect(self.helper.onItemDoubleClick)
        self.customContextMenuRequested.connect(self.helper.onContextMenuRequest)

    def add(self, widget: BaseTreeItem, isActive: bool = True):
        parent = self.currentItem()
        if parent is None:
            self.addTopLevelItem(widget.item)
        elif not widget.hasFlag(ITEM_FLAG.draggable):
            self.addTopLevelItem(widget.item)
        else:
            parent.addChild(widget.item)

        self.setItemWidget(widget.item, 0, widget)
        if isActive:
            self.setCurrentItem(widget.item)

        if widget.hasFlag(ITEM_FLAG.file):
            self.fileAdded.emit(widget.UUID())

    def remove(self, item: QTreeWidgetItem, parent: QTreeWidgetItem | None):
        for i in range(item.childCount() - 1, -1, -1):
            child = item.child(i)
            self.remove(child, item)

        widget: BaseTreeItem = self.itemWidget(item, 0)
        if widget.hasFlag(ITEM_FLAG.file):
            self.fileRemoved.emit(widget.UUID())

        if parent is None:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(item)

        self.removeItemWidget(item, 0)
        self.clearSelection()
        self.setCurrentItem(None)

    def translate(self, direction: int):
        item = self.currentItem()
        if item is None:
            return

        parent = item.parent()
        if parent is None:  # root index
            size = self.topLevelItemCount()
            index = self.indexFromItem(item, 0).row()
            self.insertAt(item, parent, (index + direction) % size)
        else:  # child index
            size = parent.childCount()
            index = parent.indexOfChild(item)
            self.insertAt(item, parent, (index + direction) % size)

    def moveTo(self, item: QTreeWidgetItem, target: QTreeWidgetItem | None):
        widgetList = self.takeOut(item)
        if target is None:  # add to root
            self.addTopLevelItem(item)
        else:  # add to target
            target.addChild(item)

        self.setWidgetList(widgetList)
        self.setCurrentItem(item)

    def insertAt(
        self, item: QTreeWidgetItem, target: QTreeWidgetItem | None, targetIndex: int
    ):
        widgetList = self.takeOut(item)
        if target is None:  # insert to root
            self.insertTopLevelItem(targetIndex, item)
        else:  # insert to target
            target.insertChild(targetIndex, item)

        self.setWidgetList(widgetList)
        self.setCurrentItem(item)

    def takeOut(self, item: QTreeWidgetItem) -> list[BaseTreeItem]:
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
        self, pItem: QTreeWidgetItem, itemList: list[BaseTreeItem]
    ) -> list[BaseTreeItem]:
        result = itemList

        for i in range(pItem.childCount()):
            cItem = pItem.child(i)
            result = self.copyWidgets(cItem, result)

        widget: BaseTreeItem = self.itemWidget(pItem, 0)
        result.append(widget.shallowcopy())

        return result

    def setWidgetList(self, items: list[BaseTreeItem]):
        for i in items:
            self.setItemWidget(i.item, 0, i)

    def isInTrash(self, item: QTreeWidgetItem) -> bool:
        trash = self.findTrash()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash

    def findTrash(self) -> QTreeWidgetItem | None:
        for i in range(self.topLevelItemCount() - 1, -1, -1):
            item = self.topLevelItem(i)
            widget = self.itemWidget(item, 0)
            if isinstance(widget, TrashFolderItem):
                return item
        return None

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        self.helper.onDragEnterEvent(super(), e)

    def dropEvent(self, e: QDropEvent) -> None:
        self.helper.onDropEvent(super(), e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.helper.onMousePressEvent(super(), e)

    def _writeHelper(self, sOut: QDataStream, iParent: QTreeWidgetItem):
        cCount = iParent.childCount()
        sOut.writeInt(cCount)

        for i in range(cCount):
            iChild = iParent.child(i)
            wChild: BaseTreeItem = self.itemWidget(iChild, 0)
            sOut.writeQString(wChild.__class__.__name__)
            self._writeHelper(sOut, iChild)
            sOut << wChild

    def _readHelper(self, sIn: QDataStream, iParent: QTreeWidgetItem):
        cCount = sIn.readInt()

        for i in range(cCount):
            type = sIn.readQString()
            wChild: BaseTreeItem = TreeItemFactory.make(type)
            self._readHelper(sIn, wChild.item)
            sIn >> wChild

            iParent.addChild(wChild.item)
            self.setItemWidget(wChild.item, 0, wChild)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        iCount = self.topLevelItemCount()
        sOut.writeInt(iCount)

        # Top level items
        for i in range(iCount):
            iParent = self.topLevelItem(i)
            wParent: BaseTreeItem = self.itemWidget(iParent, 0)
            sOut.writeQString(wParent.__class__.__name__)
            sOut << wParent

            # Child level items
            self._writeHelper(sOut, iParent)

        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self.clear()

        iCount = sIn.readInt()

        # Top level items
        for i in range(iCount):
            type = sIn.readQString()
            wParent: BaseTreeItem = TreeItemFactory.make(type)
            sIn >> wParent

            # Child level items
            self._readHelper(sIn, wParent.item)

            self.addTopLevelItem(wParent.item)
            self.setItemWidget(wParent.item, 0, wParent)

        return sIn
