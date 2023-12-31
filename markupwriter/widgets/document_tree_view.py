#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from markupwriter.config import AppConfig
from markupwriter.widgetsupport.documenttree import (
    DocumentTreeBar,
    DocumentTree,
)

class DocumentTreeView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.treeBar = DocumentTreeBar(self)
        self.tree = DocumentTree(self)

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        vLayout.addWidget(self.treeBar)
        vLayout.addWidget(self.tree)

        self.setupConnections()

    def setupConnections(self):
        self.treeBar.addItemAction.itemCreated.connect(lambda item: self.tree.addItem(item, True))
        self.treeBar.navUpAction.triggered.connect(lambda: self.tree.translateItem(-1))
        self.treeBar.navDownAction.triggered.connect(lambda: self.tree.translateItem(1))

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeViewSize = e.size()
        return super().resizeEvent(e)
    