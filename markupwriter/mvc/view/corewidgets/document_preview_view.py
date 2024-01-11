#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent
)

from PyQt6.QtWidgets import (
    QWidget,
    QTextBrowser,
    QVBoxLayout,
)

from markupwriter.config import AppConfig


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        textbrowser = QTextBrowser(self)
        self.textbrowser = textbrowser
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.textbrowser)
        self.vLayout = vLayout

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        return super().resizeEvent(e)
