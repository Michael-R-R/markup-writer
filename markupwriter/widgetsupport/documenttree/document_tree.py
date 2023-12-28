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
    FOLDER, FolderTreeItem,
    FILE, FileTreeItem,
    BaseTreeItem,
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
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._draggedItem = None

        self.itemDoubleClicked.connect(self.onItemDoubleClick)

    def addItemAtTop(self, item: BaseTreeItem):
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
        item = self.itemWidget(item, col)
        if not isinstance(item, FileTreeItem):
            return
        self.fileDoubleClicked.emit(item)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        self._draggedItem = self.currentItem()

        return super().dragEnterEvent(e)
    
    def dropEvent(self, e: QDropEvent) -> None:
        if not self.currentIndex().isValid():
            return
        if self._draggedItem is None:
            return

        result = self.rebuildAt(self._draggedItem, list())
        super().dropEvent(e)
        [self.setItemWidget(i.item, 0, i) for i in result]
        self._draggedItem = None

    def rebuildAt(self, parent: QTreeWidgetItem, itemList: list[BaseTreeItem]) -> list[BaseTreeItem]:
        result = itemList

        for i in range(parent.childCount()):
            child = parent.child(i)
            result = self.rebuildAt(child, result)

        widget = self.itemWidget(parent, 0)
        if isinstance(widget, FolderTreeItem):
            widget: FolderTreeItem = widget
            result.append(widget.deepcopy(self))
        else:
            widget: FileTreeItem = widget
            result.append(widget.deepcopy(self))

        return result

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn