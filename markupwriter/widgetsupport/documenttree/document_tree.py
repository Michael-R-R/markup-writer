#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
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
)

class DocumentTree(QTreeWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # TODO test
        item = QTreeWidgetItem()
        folder = FolderTreeItem(FOLDER.root, "path/", "Novel", item, self)
        self.addTopLevelItem(item)
        self.setItemWidget(item, 0, folder)

        item = QTreeWidgetItem()
        file = FileTreeItem(FILE.title, "path/", "Title Page", "", item, self)
        self.addTopLevelItem(item)
        self.setItemWidget(item, 0, file)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn