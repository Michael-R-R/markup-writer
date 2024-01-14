#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSignal,
)

from PyQt6.QtGui import (
    QResizeEvent,
    QTextOption,
    QGuiApplication,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QFrame,
)

import markupwriter.support.doceditor as de


class DocumentTextEdit(QPlainTextEdit):
    textAdded = pyqtSignal(str)
    textRemoved = pyqtSignal(str)
    
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        self.plainDocument = de.PlainDocument(self)

        self.setDocument(self.plainDocument)
        self.setEnabled(False)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(20.0)
        self.resizeMargins()

    def resizeMargins(self):
        mSize = QGuiApplication.primaryScreen().size()
        mW = mSize.width()

        wW = self.width()
        if wW > int(mW * 0.75):
            wW = int(wW * 0.3)
        elif wW > int(mW * 0.5):
            wW = int(wW * 0.2)
        else:
            wW = int(wW * 0.1)

        wH = int(self.height() * 0.1)

        self.setViewportMargins(wW, wH, wW, wH)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        self.resizeMargins()
        super().resizeEvent(e)
