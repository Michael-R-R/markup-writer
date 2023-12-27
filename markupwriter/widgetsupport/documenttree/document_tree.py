#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QFrame,
)

from .treeitem import DocumentTreeItem

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

        item = QTreeWidgetItem()
        folder = DocumentTreeItem("Folder", "", item, self)
        self.addTopLevelItem(item)
        self.setItemWidget(item, 0, folder)