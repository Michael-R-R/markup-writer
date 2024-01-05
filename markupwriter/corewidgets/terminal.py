#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget,
)

from markupwriter.config import (
    AppConfig,
)

class Terminal(QTabWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.terminalSize = e.size()
        return super().resizeEvent(e)
    
    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn
