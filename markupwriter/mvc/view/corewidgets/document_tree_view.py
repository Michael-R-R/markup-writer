#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from markupwriter.config import AppConfig
import markupwriter.widgets as mw


class DocumentTreeView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.treebar = mw.DocumentTreeBarWidget(self)
        self.treewidget = mw.DocumentTreeWidget(self)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.treebar, 0, 0)
        self.gLayout.addWidget(self.treewidget, 1, 0)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeSize = e.size()
        return super().resizeEvent(e)
