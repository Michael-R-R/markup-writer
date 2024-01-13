#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

from PyQt6.QtGui import (
    QTextDocument,
)

from PyQt6.QtWidgets import (
    QPlainTextDocumentLayout,
)

from markupwriter.common.syntax import (
    Highlighter,
)


class PlainDocument(QTextDocument):
    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.highlighter = Highlighter(self)

        self.setDocumentLayout(QPlainTextDocumentLayout(self))
