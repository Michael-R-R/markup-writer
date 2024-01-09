#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSlot,
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

from markupwriter.util import (
    File,
)

from markupwriter.common.provider import (
    Style,
)

from markupwriter.coresupport.documenttree import (
    DocumentTreeBar,
    DocumentTree,
)

from markupwriter.coresupport.documenttree.treeitem import (
    BaseTreeItem,
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

        self.setStyleSheet(Style.TREE_VIEW)
        
    @pyqtSlot(BaseTreeItem)
    def onItemCreated(self, item: BaseTreeItem):
        self.tree.add(item)
        
    @pyqtSlot()
    def onNavUpClicked(self):
        self.tree.translate(-1)
    
    @pyqtSlot()
    def onNavDownClicked(self):
        self.tree.translate(1)

    @pyqtSlot(str)
    def onFileAdded(self, uuid: str):
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += uuid
        File.write(path, "")

    @pyqtSlot(str)
    def onFileRemoved(self, uuid: str):
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += uuid
        File.remove(path)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeViewSize = e.size()
        return super().resizeEvent(e)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << self.tree
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> self.tree
        return sIn
