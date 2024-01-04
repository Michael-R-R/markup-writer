#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
    QGuiApplication,
    QTextOption,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QFrame,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.common.provider import (
    Style,
)

from markupwriter.coresupport.documenteditor import (
    PlainDocument,
)

class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.plainDocument = PlainDocument()
        
        self.setDocument(self.plainDocument)
        self.setStyleSheet(Style.EDITOR)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(20.0)
        self.updateViewportMargins()

    def updateViewportMargins(self):
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
        AppConfig.docEditorSize = e.size()
        self.updateViewportMargins()
        super().resizeEvent(e)