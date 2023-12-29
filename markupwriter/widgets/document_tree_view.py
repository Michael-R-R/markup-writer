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

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        
        treeBar = DocumentTreeBar(self)
        tree = DocumentTree(self)

        vLayout.addWidget(treeBar)
        vLayout.addWidget(tree)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeViewSize = e.size()
        return super().resizeEvent(e)
    