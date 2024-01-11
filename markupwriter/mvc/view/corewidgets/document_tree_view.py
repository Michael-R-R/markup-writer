#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from markupwriter.config import AppConfig
import markupwriter.widgets as w


class DocumentTreeView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.treebar = w.DocumentTreeBarWidget(self)
        self.treewidget = w.DocumentTreeWidget(self)

        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.treebar)
        vLayout.addWidget(self.treewidget)
        self.vLayout = vLayout
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeSize = e.size()
        return super().resizeEvent(e)
