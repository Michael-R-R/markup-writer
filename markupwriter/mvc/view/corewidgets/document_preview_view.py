#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from markupwriter.config import AppConfig


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        self.widget = None
        self.vLayout = QVBoxLayout(self)
        
    def addWidget(self, widget: QWidget):
        self.widget = widget
        self.vLayout.addWidget(widget)
        
    def removeWidget(self):
        if self.widget is None:
            return
        self.vLayout.removeWidget(self.widget)
        self.widget = None

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        return super().resizeEvent(e)
