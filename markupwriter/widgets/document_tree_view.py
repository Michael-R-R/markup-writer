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

        self._treeBar = DocumentTreeBar(self)
        self._tree = DocumentTree(self)

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        vLayout.addWidget(self._treeBar)
        vLayout.addWidget(self._tree)

        self.setupConnections()

    def setupConnections(self):
        self._treeBar.addItemAction.itemCreated.connect(lambda item: self._tree.addItem(item))
        self._treeBar.navUpAction.triggered.connect(lambda: self._tree.moveSelectedItem(-1))
        self._treeBar.navDownAction.triggered.connect(lambda: self._tree.moveSelectedItem(1))

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeViewSize = e.size()
        return super().resizeEvent(e)
    