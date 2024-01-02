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

from markupwriter.support.provider import (
    Style,
)

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.plainDocument = PlainDocument()
        
        self.setDocument(self.plainDocument)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(20.0)
        self.setViewportMargins(1, 1, 1, 1)
        self.setStyleSheet(Style.EDITOR)

    def updateMargins(self):
        mW = QGuiApplication.primaryScreen().size().width()

        wW = self.width()
        wW = int(wW * 0.1) if wW < int(mW / 2) else int(wW * 0.3)
        wH = int(self.height() * 0.1)

        self.setViewportMargins(wW, wH, wW, wH)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        self.updateMargins()
        super().resizeEvent(e)