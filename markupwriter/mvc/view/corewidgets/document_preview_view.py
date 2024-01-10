#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QTextBrowser,
    QVBoxLayout,
)


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        textbrowser = QTextBrowser(self)
        self.textbrowser = textbrowser
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.textbrowser)
        self.vLayout = vLayout

