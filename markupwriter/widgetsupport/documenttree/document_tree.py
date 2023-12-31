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

from markupwriter.contextmenus.documenttree import (
    TreeContextMenu,
)

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

        self._draggedItem = None
        self._contextMenu = TreeContextMenu()
        self._contextMenu.addItemMenu.itemCreated.connect(self.addItem)
        self._contextMenu.moveToTrash.triggered.connect(self._onMoveToTrash)
        self._contextMenu.emptyTrash.triggered.connect(self._onEmptyTrash)

        self.addItem(PlotFolderItem("Plot", QTreeWidgetItem(), self), False)
        self.addItem(TimelineFolderItem("Timeline", QTreeWidgetItem(), self), False)
        self.addItem(CharsFolderItem("Characters", QTreeWidgetItem(), self), False)
        self.addItem(LocFolderItem("Locations", QTreeWidgetItem(), self), False)
        self.addItem(ObjFolderItem("Objects", QTreeWidgetItem(), self), False)
        self.addItem(TrashFolderItem("Trash", QTreeWidgetItem(), self), False)

        self.itemDoubleClicked.connect(self._onItemDoubleClick)
        self.customContextMenuRequested.connect(self._onContextMenuRequest)

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
            self.collapseItem(item.item)

        if not item.isFolder():
            self.fileAdded.emit(item.shallowcopy())

    def removeItem(self, item: QTreeWidgetItem):
        for i in range(item.childCount()):
            child = item.child(i)
            self.removeItem(child)
            item.takeChild(i)

        index = self.indexOfTopLevelItem(item)
        if index > -1:
            self.takeTopLevelItem(index)

        widget: BaseTreeItem = self.itemWidget(item, 0)
        if not widget.isFolder():
            self.fileRemoved.emit(widget.shallowcopy())

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
            self._insertItemAt(item, parent, (index + direction) % size)
        else: # child index
            size = parent.childCount()
            index = parent.indexOfChild(item)
            self._insertItemAt(item, parent, (index + direction) % size)

    def updateItemWidget(self, item: QTreeWidgetItem, widget: BaseTreeItem):
        self.setItemWidget(item, 0, widget)

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

        itemList = self._copyWidgets(self._draggedItem, list())
        super().dropEvent(e)
        self._setItemWidgetList(itemList)
        self.setCurrentItem(self._draggedItem)
        self.collapseItem(self._draggedItem)
        self._draggedItem = None

    def mousePressEvent(self, e: QMouseEvent) -> None:
        index = self.indexAt(e.pos())
        super().mousePressEvent(e)
        if not index.isValid():
            self.clearSelection()
            self.setCurrentItem(None)

    def _moveItemTo(self, item: QTreeWidgetItem, target: QTreeWidgetItem | None):
        widgetList = self._takeItemOut(item)
        if target is None: # add to root
            self.addTopLevelItem(item)
        else: # add to target
            target.addChild(item)

        self._setItemWidgetList(widgetList)
        self.setCurrentItem(item)
        self.collapseItem(item)

    def _insertItemAt(self, item: QTreeWidgetItem, target: QTreeWidgetItem | None, targetIndex: int):
        widgetList = self._takeItemOut(item)
        if target is None: # insert to root
            self.insertTopLevelItem(targetIndex, item)
        else: # insert to target
            target.insertChild(targetIndex, item)

        self._setItemWidgetList(widgetList)
        self.setCurrentItem(item)
        self.collapseItem(item)

    def _takeItemOut(self, item: QTreeWidgetItem) -> list[BaseTreeItem]:
        widgetList = self._copyWidgets(item, list())
        parent = item.parent()
        if parent is None: # is root item
            index = self.indexFromItem(item, 0).row()
            item = self.takeTopLevelItem(index)
        else: # is child item
            index = parent.indexOfChild(item)
            item = parent.takeChild(index)

        return widgetList

    def _copyWidgets(self, parent: QTreeWidgetItem, itemList: list[BaseTreeItem]) -> list[BaseTreeItem]:
        result = itemList

        for i in range(parent.childCount()):
            child = parent.child(i)
            result = self._copyWidgets(child, result)

        widget: BaseTreeItem = self.itemWidget(parent, 0)
        result.append(widget.shallowcopy())

        return result

    def _setItemWidgetList(self, items: list[BaseTreeItem]):
        for i in items:
            self.setItemWidget(i.item, 0, i)

    def _onItemDoubleClick(self, item: QTreeWidgetItem, col: int):
        widget: BaseTreeItem = self.itemWidget(item, col)
        if not widget.isFolder():
            self.fileDoubleClicked.emit(widget.shallowcopy())

    def _onContextMenuRequest(self, pos: QPoint):
        item = self.itemAt(pos)
        widget = self.itemWidget(item, 0)
        pos = self.mapToGlobal(pos)
        if item is None:
            self._contextMenu.onEmptyClickMenu(pos)
        elif isinstance(widget, TrashFolderItem):
            self._contextMenu.onTrashFolderMenu(pos)
        else:
            self._contextMenu.onBaseItemMenu(pos)

    def _onMoveToTrash(self):
        item = self.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self.itemWidget(item, 0)
        if not widget.isEditable:
            return
        
        trash = self._findTrashFolder()
        if trash is None:
            return
        
        self._moveItemTo(item, trash)

    def _onEmptyTrash(self):
        raise NotImplementedError()

    def _findTrashFolder(self) -> QTreeWidgetItem | None:
        for i in range(self.topLevelItemCount()-1, -1, -1):
            item = self.topLevelItem(i)
            widget = self.itemWidget(item, 0)
            if isinstance(widget, TrashFolderItem):
                return item
        return None

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        raise NotImplementedError()
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        raise NotImplementedError()