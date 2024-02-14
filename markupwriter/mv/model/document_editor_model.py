#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    QThreadPool,
)

from markupwriter.common.referencetag import RefTagManager
from markupwriter.common.parsers import EditorParser


class DocumentEditorModel(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.currDocPath = ""
        self.currDocUUID = ""
        self.refManager = RefTagManager()
        self.parser = EditorParser()
        self.threadPool = QThreadPool(self)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
