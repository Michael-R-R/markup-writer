#!/usr/bin/python

from PyQt6.QtGui import (
    QTextDocument,
)

from PyQt6.QtWidgets import (
    QPlainTextDocumentLayout,
)

from markupwriter.support.syntax import (
    Highlighter,
)

from markupwriter.support.referencetag import (
    RefTagManager,
)

from markupwriter.support.editorparser import (
    PassiveDocumentParser,
)

class PlainDocument(QTextDocument):
    def __init__(self):
        super().__init__()
        
        self.setDocumentLayout(QPlainTextDocumentLayout(self))
        self._highlighter = Highlighter(self)
        self._refTagManager = RefTagManager()
        self._passiveParser = PassiveDocumentParser(self._highlighter,
                                                    self._refTagManager)

    def highlighter(self) -> Highlighter:
        return self._highlighter
    
    def refTagManager(self) -> RefTagManager:
        return self._refTagManager
        