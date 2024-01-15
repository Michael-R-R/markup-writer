#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QThreadPool,
)

from markupwriter.common.syntax import (
    Highlighter,
)

from markupwriter.common.referencetag import (
    RefTagManager,
)


from markupwriter.common.parsers import (
    EditorParser,
)


class DocumentEditor(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.currDocPath = ""
        self.currDocUUID = ""
        self.highlighter = Highlighter(None)
        self.refManager = RefTagManager()
        self.parser = EditorParser(self.refManager, self)
        self.threadPool = QThreadPool(self)
        
    def setHighlighterDoc(self, document):
        self.highlighter.setDocument(document)
