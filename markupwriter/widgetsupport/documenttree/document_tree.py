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

from markupwriter.util.serialize import serialize, deserialize

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

    def onItemDoubleClick(self, item: QTreeWidgetItem, col: int):
        widget: BaseTreeItem = self.itemWidget(item, col)
        if widget.isFolder():
            return
        self.fileDoubleClicked.emit(widget)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        self._draggedItem = self.currentItem()

        return super().dragEnterEvent(e)
    
    def dropEvent(self, e: QDropEvent) -> None:
        if not self.currentIndex().isValid():
            return
        if self._draggedItem is None:
            return

        result = self.copyItemsAt(self._draggedItem, list())
        super().dropEvent(e)
        [self.setItemWidget(i.item, 0, i) for i in result]
        self.clearSelection()
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
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn