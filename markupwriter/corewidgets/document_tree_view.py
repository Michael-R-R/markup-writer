#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

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

from markupwriter.util import (
    File,
)

from markupwriter.coresupport.documenttree import (
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
        self.setStyleSheet(Style.TREE_VIEW)

    def setupConnections(self):
        # --- Tree bar --- #
        self.treeBar.addItemAction.itemCreated.connect(
            lambda item: self.tree.add(item, True)
        )
        self.treeBar.navUpAction.triggered.connect(lambda: self.tree.translate(-1))
        self.treeBar.navDownAction.triggered.connect(lambda: self.tree.translate(1))

        # --- Tree --- #
        self.tree.fileAdded.connect(self._onFileAdded)
        self.tree.fileRemoved.connect(self._onFileRemoved)

    def _onFileAdded(self, uuid: str):
        contentPath = AppConfig.projectContentPath()
        if contentPath is None:
            return
        contentPath += uuid
        File.write(contentPath, "")

    def _onFileRemoved(self, uuid: str):
        pass

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeViewSize = e.size()
        return super().resizeEvent(e)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << self.tree
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> self.tree
        return sIn
