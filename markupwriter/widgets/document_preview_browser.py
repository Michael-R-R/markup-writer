#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
    QTextOption,
    QGuiApplication,
)

from PyQt6.QtWidgets import (
    QTextBrowser,
    QWidget,
    QFrame,
)

class DocumentPreviewBrowser(QTextBrowser):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
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
