#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from markupwriter.config import AppConfig
import markupwriter.widgets as mw


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        self.textbrowser = mw.DocumentPreviewBrowser(self)
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.textbrowser)
        self.vLayout = vLayout

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        return super().resizeEvent(e)
