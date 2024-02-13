#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
)


class DocumentPreviewModel(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin