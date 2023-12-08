#!/usr/bin/python

from PyQt6.QtWidgets import (
    QTextBrowser,
    QWidget,
)

class DocumentPreview(QTextBrowser):
    def __init__(self, parent: QWidget):
        super().__init__(parent)