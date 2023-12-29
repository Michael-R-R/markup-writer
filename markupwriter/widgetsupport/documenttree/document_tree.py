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

        # TODO test
        item = QTreeWidgetItem()
        folder1 = FolderTreeItem(FOLDER.root, "Novel 1", item, self)
        self.addItemAtRoot(folder1)

        item = QTreeWidgetItem()
        folder2 = FolderTreeItem(FOLDER.root, "Novel 2", item, self)
        self.addItemAtRoot(folder2)

        item = QTreeWidgetItem()
        file1 = FileTreeItem(FILE.title, "Title Page", "", item, self)
        self.addChildItem(folder1, file1)

        item = QTreeWidgetItem()
        file2 = FileTreeItem(FILE.chapter, "Chapter One", "", item, self)
        self.addChildItem(folder1, file2)

        item = QTreeWidgetItem()
        file3 = FileTreeItem(FILE.scene, "Scene One", "", item, self)
        self.addChildItem(folder1, file3)

    def addItemAtRoot(self, item: BaseTreeItem):
        self.addTopLevelItem(item.item)
        self.setItemWidget(item.item, 0, item)

    def addChildItem(self, parent: BaseTreeItem, child: BaseTreeItem):
        p: QTreeWidgetItem = parent.item
        c: QTreeWidgetItem = child.item
        p.addChild(c)
        self.setItemWidget(c, 0, child)

    def removeItemAt(self, parent: QTreeWidgetItem):
        for i in range(parent.childCount()):
            child = parent.child(i)
            self.removeItemAt(child)
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