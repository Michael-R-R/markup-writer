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

from .treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
    BaseFileItem,
    PlotFolderItem,
    TimelineFolderItem,
    CharsFolderItem,
    LocFolderItem,
    ObjFolderItem,
    TrashFolderItem,
)

import markupwriter.coresupport.documenttree as dt

class DocumentTree(QTreeWidget):
    fileAdded = pyqtSignal(BaseFileItem)
    fileRemoved = pyqtSignal(BaseFileItem)
    fileDoubleClicked = pyqtSignal(BaseFileItem)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
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

        self.helper = dt.DocumentTreeHelper(self)
        self.draggedItem = None

        self.addWidget(PlotFolderItem("Plot", QTreeWidgetItem(), self), False)
        self.addWidget(TimelineFolderItem("Timeline", QTreeWidgetItem(), self), False)
        self.addWidget(CharsFolderItem("Characters", QTreeWidgetItem(), self), False)
        self.addWidget(LocFolderItem("Locations", QTreeWidgetItem(), self), False)
        self.addWidget(ObjFolderItem("Objects", QTreeWidgetItem(), self), False)
        self.addWidget(TrashFolderItem("Trash", QTreeWidgetItem(), self), False)

        self.itemDoubleClicked.connect(self.helper.onItemDoubleClick)
        self.customContextMenuRequested.connect(self.helper.onContextMenuRequest)

    def addWidget(self, widget: BaseTreeItem, isActive: bool = True):
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
            self.fileAdded.emit(widget.shallowcopy())

    def removeItem(self, item: QTreeWidgetItem, parent: QTreeWidgetItem | None):
        for i in range(item.childCount()-1, -1, -1):
            child = item.child(i)
            self.removeItem(child, item)
        
        widget: BaseTreeItem = self.itemWidget(item, 0)
        if widget.hasFlag(ITEM_FLAG.file):
            self.fileRemoved.emit(widget.shallowcopy())

        if parent is None:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(item)
        
        self.removeItemWidget(item, 0)
        self.clearSelection()
        self.setCurrentItem(None)

    def translateItem(self, direction: int):
        item = self.currentItem()
        if item is None:
            return
        
        parent = item.parent()
        if parent is None: # root index
            size = self.topLevelItemCount()
            index = self.indexFromItem(item, 0).row()
            self.insertItemAt(item, parent, (index + direction) % size)
        else: # child index
            size = parent.childCount()
            index = parent.indexOfChild(item)
            self.insertItemAt(item, parent, (index + direction) % size)

    def moveItemTo(self,
                   item: QTreeWidgetItem,
                   target: QTreeWidgetItem | None):
        widgetList = self.takeItemOut(item)
        if target is None: # add to root
            self.addTopLevelItem(item)
        else: # add to target
            target.addChild(item)

        self.setItemWidgetList(widgetList)
        self.setCurrentItem(item) 

    def insertItemAt(self,
                     item: QTreeWidgetItem,
                     target: QTreeWidgetItem | None,
                     targetIndex: int):
        widgetList = self.takeItemOut(item)
        if target is None: # insert to root
            self.insertTopLevelItem(targetIndex, item)
        else: # insert to target
            target.insertChild(targetIndex, item)

        self.setItemWidgetList(widgetList)
        self.setCurrentItem(item)

    def takeItemOut(self, item: QTreeWidgetItem) -> list[BaseTreeItem]:
        widgetList = self.copyWidgets(item, list())
        parent = item.parent()
        if parent is None: # is root item
            index = self.indexFromItem(item, 0).row()
            item = self.takeTopLevelItem(index)
        else: # is child item
            index = parent.indexOfChild(item)
            item = parent.takeChild(index)

        return widgetList
    
    def copyWidgets(self,
                    parent: QTreeWidgetItem,
                    itemList: list[BaseTreeItem]) -> list[BaseTreeItem]:
        result = itemList

        for i in range(parent.childCount()):
            child = parent.child(i)
            result = self.copyWidgets(child, result)

        widget: BaseTreeItem = self.itemWidget(parent, 0)
        result.append(widget.shallowcopy())

        return result
    
    def setItemWidgetList(self, items: list[BaseTreeItem]):
        for i in items:
            self.setItemWidget(i.item, 0, i)

    def isItemInTrash(self, item: QTreeWidgetItem) -> bool:
        trash = self.findTrashFolder()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash

    def findTrashFolder(self) -> QTreeWidgetItem | None:
        for i in range(self.topLevelItemCount()-1, -1, -1):
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

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        raise NotImplementedError()
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        raise NotImplementedError()
    