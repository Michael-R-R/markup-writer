#!/usr/bin/python

from PyQt6.QtGui import (
    QTextDocument,
)

from PyQt6.QtWidgets import (
    QPlainTextDocumentLayout,
)

from markupwriter.support.syntax import (
    Highlighter,
    Parser,
)

class PlainDocument(QTextDocument):
    def __init__(self):
        super().__init__()
        
        self.setDocumentLayout(QPlainTextDocumentLayout(self))
        self._highlighter = Highlighter(self)
        self._parser = Parser(self._highlighter)

        self.contentsChange.connect(self.showChanged)

    def showChanged(self, pos: int, removed: int, added: int):
        print(pos, removed, added)
        