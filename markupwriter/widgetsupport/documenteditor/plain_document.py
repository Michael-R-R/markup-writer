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

class PlainDocument(QTextDocument):
    def __init__(self):
        super().__init__()
        
        self.setDocumentLayout(QPlainTextDocumentLayout(self))
        self.__highlighter = Highlighter(self)
        self.__refTagManager = RefTagManager()

    def highlighter(self) -> Highlighter:
        return self.__highlighter
    
    def refTagManager(self) -> RefTagManager:
        return self.__refTagManager
        