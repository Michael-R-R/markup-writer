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

from .passive_parser import (
    PassiveParser,
)


class PlainDocument(QTextDocument):
    def __init__(self, parent: QObject):
        super().__init__(parent)

        self._highlighter = Highlighter(self)
        self._refTagManager = RefTagManager()
        self._passiveParser = PassiveParser(self)

        self.setDocumentLayout(QPlainTextDocumentLayout(self))

    def highlighter(self) -> Highlighter:
        return self._highlighter

    def refTagManager(self) -> RefTagManager:
        return self._refTagManager

    def passiveParser(self) -> PassiveParser:
        return self._passiveParser
