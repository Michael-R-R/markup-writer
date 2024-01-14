#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from PyQt6.QtGui import (
    QTextDocument,
)

from PyQt6.QtWidgets import (
    QPlainTextDocumentLayout,
)

class PlainDocument(QTextDocument):
    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.setDocumentLayout(QPlainTextDocumentLayout(self))
