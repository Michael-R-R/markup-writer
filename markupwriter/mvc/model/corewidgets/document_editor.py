#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QThreadPool,
)

from markupwriter.common.referencetag import (
    RefTagManager,
)

from markupwriter.common.tokenizers import (
    Tokenizer,
)

class DocumentEditor(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.currDocPath = ""
        self.currDocUUID = ""
        self.refTagManager = RefTagManager()
        self.tokenizer = Tokenizer(self)
        self.threadPool = QThreadPool(self)
