#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.common.provider import (
    Style,
)

from markupwriter.coresupport.documenttree import (
    DocumentTreeBar,
    DocumentTree,
)

class DocumentTreeView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.docTreeBar = DocumentTreeBar(self)
        self.docTree = DocumentTree(self)

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        vLayout.addWidget(self.docTreeBar)
        vLayout.addWidget(self.docTree)

        self.setupConnections()
        self.setStyleSheet(Style.TREE_VIEW)

    def setupConnections(self):
        self.docTreeBar.addItemAction.itemCreated.connect(lambda item: self.docTree.addWidget(item, True))
        self.docTreeBar.navUpAction.triggered.connect(lambda: self.docTree.translateItem(-1))
        self.docTreeBar.navDownAction.triggered.connect(lambda: self.docTree.translateItem(1))

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeViewSize = e.size()
        return super().resizeEvent(e)
    