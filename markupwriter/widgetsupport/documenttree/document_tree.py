#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
    pyqtSignal,
    QPoint,
)
from PyQt6.QtGui import (
    QDragEnterEvent,
    QDropEvent,
)

from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QFrame,
)

from .treeitem import (
    BaseTreeItem,
    BaseFileItem,
    PlotFolderItem,
    TimelineFolderItem,
    CharsFolderItem,
    LocFolderItem,
    ObjFolderItem,
    TrashFolderItem,
)

from markupwriter.menus.documenttree import (
    TreeContextMenu,
)

class DocumentTree(QTreeWidget):
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

        self._draggedItem = None
        self._contextMenu = TreeContextMenu(self)
        self._contextMenu.addItemMenu.itemCreated.connect(self.addItem)
        self._contextMenu.moveToTrash.triggered.connect(self.onMoveToTrash)

        self.addItem(PlotFolderItem("Plot", QTreeWidgetItem(), self))
        self.addItem(TimelineFolderItem("Timeline", QTreeWidgetItem(), self))
        self.addItem(CharsFolderItem("Characters", QTreeWidgetItem(), self))
        self.addItem(LocFolderItem("Locations", QTreeWidgetItem(), self))
        self.addItem(ObjFolderItem("Objects", QTreeWidgetItem(), self))
        self.addItem(TrashFolderItem("Trash", QTreeWidgetItem(), self))

        self.itemDoubleClicked.connect(self.onItemDoubleClick)
        self.customContextMenuRequested.connect(self.onContextMenuRequest)

    def addItem(self, item: BaseTreeItem, isActive: bool = False):
        parent = self.currentItem()
        if parent is None:
            self.addTopLevelItem(item.item)
        elif not item.isDraggable:
            self.addTopLevelItem(item.item)
        else:
            parent.addChild(item.item)
                
        self.setItemWidget(item.item, 0, item)
        if isActive:
            self.setCurrentItem(item.item)

    def removeItem(self, parent: QTreeWidgetItem):
        for i in range(parent.childCount()):
            child = parent.child(i)
            self.removeItem(child)
            parent.removeChild(child)

        index = self.indexOfTopLevelItem(parent)
        if index > -1:
            self.takeTopLevelItem(index)
        self.removeItemWidget(parent, 0)

    def moveCurrentItem(self, direction: int):
        child = self.currentItem()
        if child is None:
            return
        
        result: list[BaseTreeItem] = list()
        
        parent = child.parent()
        if parent is None: # root item
            size = self.topLevelItemCount()
            index = self.indexFromItem(child, 0).row()
            result = self.copyItems(child, list())
            child = self.takeTopLevelItem(index)
            self.insertTopLevelItem((index+direction) % size, child)
        else: # child item
            size = parent.childCount()
            index = parent.indexOfChild(child)
            result = self.copyItems(child, list())
            child = parent.takeChild(index)
            parent.insertChild((index+direction) % size, child)
        
        [self.setItemWidget(i.item, 0, i) for i in result]
        self.setCurrentItem(child)

    def copyItems(self, parent: QTreeWidgetItem, itemList: list[BaseTreeItem]) -> list[BaseTreeItem]:
        result = itemList

        for i in range(parent.childCount()):
            child = parent.child(i)
            result = self.copyItems(child, result)

        widget: BaseTreeItem = self.itemWidget(parent, 0)
        result.append(widget.deepcopy())

        return result

    def onItemDoubleClick(self, item: QTreeWidgetItem, col: int):
        widget: BaseTreeItem = self.itemWidget(item, col)
        if widget.isFolder():
            return
        self.fileDoubleClicked.emit(widget)

    def onContextMenuRequest(self, pos: QPoint):
        self._contextMenu.exec(self.mapToGlobal(pos))

    def onMoveToTrash(self):
        item = self.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self.itemWidget(item, 0)
        if not widget.isEditable:
            return

        # TODO implement

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        item = self.currentItem()
        widget: BaseTreeItem = self.itemWidget(item, 0)
        if not widget.isDraggable:
            return
            
        self._draggedItem = item

        return super().dragEnterEvent(e)
    
    def dropEvent(self, e: QDropEvent) -> None:
        if not self.currentIndex().isValid():
            return
        if self._draggedItem is None:
            return

        result = self.copyItems(self._draggedItem, list())
        super().dropEvent(e)
        [self.setItemWidget(i.item, 0, i) for i in result]
        self.setCurrentItem(self._draggedItem)
        self._draggedItem = None

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        raise NotImplementedError()
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        raise NotImplementedError()