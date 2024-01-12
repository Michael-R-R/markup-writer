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

from markupwriter.common.syntax import (
    Highlighter,
)

from markupwriter.common.referencetag import (
    RefTagManager,
)

from markupwriter.common.parsers import (
    PassiveParser,
)


class PlainDocument(QTextDocument):
    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.highlighter = Highlighter(self)
        self.refTagManager = RefTagManager()
        self.passiveParser = PassiveParser(self)

        self.setDocumentLayout(QPlainTextDocumentLayout(self))
