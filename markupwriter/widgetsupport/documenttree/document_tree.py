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
    QMouseEvent,
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
        self._contextMenu = TreeContextMenu()
        self._contextMenu.addItemMenu.itemCreated.connect(self.addItem)
        self._contextMenu.moveToTrash.triggered.connect(self.onMoveToTrash)
        self._contextMenu.emptyTrash.triggered.connect(self.onEmptyTrash)

        self.addItem(PlotFolderItem("Plot", QTreeWidgetItem(), self), False)
        self.addItem(TimelineFolderItem("Timeline", QTreeWidgetItem(), self), False)
        self.addItem(CharsFolderItem("Characters", QTreeWidgetItem(), self), False)
        self.addItem(LocFolderItem("Locations", QTreeWidgetItem(), self), False)
        self.addItem(ObjFolderItem("Objects", QTreeWidgetItem(), self), False)
        self.addItem(TrashFolderItem("Trash", QTreeWidgetItem(), self), False)

        self.itemDoubleClicked.connect(self.onItemDoubleClick)
        self.customContextMenuRequested.connect(self.onContextMenuRequest)

    def addItem(self, item: BaseTreeItem, isActive: bool = True):
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
        else:
            self.clearSelection()

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
        
        itemList: list[BaseTreeItem] = list()
        
        parent = child.parent()
        if parent is None: # root item
            size = self.topLevelItemCount()
            index = self.indexFromItem(child, 0).row()
            itemList = self.copyItems(child, list())
            child = self.takeTopLevelItem(index)
            self.insertTopLevelItem((index+direction) % size, child)
        else: # child item
            size = parent.childCount()
            index = parent.indexOfChild(child)
            itemList = self.copyItems(child, list())
            child = parent.takeChild(index)
            parent.insertChild((index+direction) % size, child)
        
        self.massSetItemWidgets(itemList)
        self.setCurrentItem(child)

    def copyItems(self, parent: QTreeWidgetItem, itemList: list[BaseTreeItem]) -> list[BaseTreeItem]:
        result = itemList

        for i in range(parent.childCount()):
            child = parent.child(i)
            result = self.copyItems(child, result)

        widget: BaseTreeItem = self.itemWidget(parent, 0)
        result.append(widget.deepcopy())

        return result

    def massSetItemWidgets(self, items: list[BaseTreeItem]):
        [self.setItemWidget(i.item, 0, i) for i in items]

    def onItemDoubleClick(self, item: QTreeWidgetItem, col: int):
        widget: BaseTreeItem = self.itemWidget(item, col)
        if widget.isFolder():
            return
        self.fileDoubleClicked.emit(widget)

    def onContextMenuRequest(self, pos: QPoint):
        item = self.itemAt(pos)
        widget = self.itemWidget(item, 0)
        pos = self.mapToGlobal(pos)
        if item is None:
            self._contextMenu.onEmptyClickMenu(pos)
        elif isinstance(widget, TrashFolderItem):
            self._contextMenu.onTrashFolderMenu(pos)
        else:
            self._contextMenu.onBaseItemMenu(pos)

    def onMoveToTrash(self):
        item = self.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self.itemWidget(item, 0)
        if not widget.isEditable:
            return

        # find trash folder
        trashItem = None
        for i in range(self.topLevelItemCount()-1, -1, -1):
            temp = self.topLevelItem(i)
            widget = self.itemWidget(temp, 0)
            if isinstance(widget, TrashFolderItem):
                trashItem = temp
                break
        if trashItem is None:
            return
        
        # take item out
        itemList = self.copyItems(item, list())
        parent = item.parent()
        if parent is None: # root item
            index = self.indexFromItem(item, 0).row()
            item = self.takeTopLevelItem(index)
        else: # child item
            index = parent.indexOfChild(item)
            item = parent.takeChild(index)

        # add item to trash folder
        trashItem.addChild(item)
        self.massSetItemWidgets(itemList)

    def onEmptyTrash(self):
        raise NotImplementedError()

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

        itemList = self.copyItems(self._draggedItem, list())
        super().dropEvent(e)
        self.massSetItemWidgets(itemList)
        self.setCurrentItem(self._draggedItem)
        self._draggedItem = None

    def mousePressEvent(self, e: QMouseEvent) -> None:
        index = self.indexAt(e.pos())
        super().mousePressEvent(e)
        if not index.isValid():
            self.clearSelection()
            self.setCurrentItem(None)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        raise NotImplementedError()
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        raise NotImplementedError()