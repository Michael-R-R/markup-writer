#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
    pyqtSignal,
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
    FOLDER, FolderTreeItem,
    FILE, FileTreeItem,
)

class DocumentTree(QTreeWidget):
    fileDoubleClicked = pyqtSignal(FileTreeItem)

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

        self.itemDoubleClicked.connect(self.onItemDoubleClick)

    def addItem(self, item: BaseTreeItem):
        parent = self.currentItem()
        if parent is None: # add to root
            self.addTopLevelItem(item.item)
        else: # add as child
            if item.isFolder():
                folder: FolderTreeItem = item
                if folder.folderType == FOLDER.root:
                    self.addTopLevelItem(item.item)
                else:
                    parent.addChild(item.item)
            else:
                parent.addChild(item.item)

        self.setItemWidget(item.item, 0, item)
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

    def moveSelectedItem(self, direction: int):
        child = self.currentItem()
        if child is None:
            return
        
        result: list[BaseTreeItem] = list()
        
        parent = child.parent()
        if parent is None: # root item
            size = self.topLevelItemCount()
            index = self.indexFromItem(child, 0).row()
            result = self.copyItemsAt(child, list())
            child = self.takeTopLevelItem(index)
            self.insertTopLevelItem((index+direction) % size, child)
        else: # child item
            size = parent.childCount()
            index = parent.indexOfChild(child)
            result = self.copyItemsAt(child, list())
            child = parent.takeChild(index)
            parent.insertChild((index+direction) % size, child)
        
        [self.setItemWidget(i.item, 0, i) for i in result]
        self.setCurrentItem(child)

    def onItemDoubleClick(self, item: QTreeWidgetItem, col: int):
        widget: BaseTreeItem = self.itemWidget(item, col)
        if widget.isFolder():
            return
        self.fileDoubleClicked.emit(widget)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        item = self.currentItem()
        widget: BaseTreeItem = self.itemWidget(item, 0)
        if widget.isFolder():
            widget: FolderTreeItem = widget
            if widget.folderType != FOLDER.misc:
                return
            
        self._draggedItem = item

        return super().dragEnterEvent(e)
    
    def dropEvent(self, e: QDropEvent) -> None:
        if not self.currentIndex().isValid():
            return
        if self._draggedItem is None:
            return

        result = self.copyItemsAt(self._draggedItem, list())
        super().dropEvent(e)
        [self.setItemWidget(i.item, 0, i) for i in result]
        self.setCurrentItem(self._draggedItem)
        self._draggedItem = None

    def copyItemsAt(self, parent: QTreeWidgetItem, itemList: list[BaseTreeItem]) -> list[BaseTreeItem]:
        result = itemList

        for i in range(parent.childCount()):
            child = parent.child(i)
            result = self.copyItemsAt(child, result)

        widget: BaseTreeItem = self.itemWidget(parent, 0)
        result.append(widget.deepcopy(self))

        return result

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        raise NotImplementedError()
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        raise NotImplementedError()