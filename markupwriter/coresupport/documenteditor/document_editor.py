#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QCloseEvent,
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

from markupwriter.util import (
    File,
)

from markupwriter.common.provider import (
    Style,
)

from .plain_document import PlainDocument


class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.currUUID = ""
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

    def onFileDoubleClicked(self, uuid: str):
        if self.currUUID == uuid:
            return

        self._writeCurrentDoc() # write old file
        self.currUUID = uuid
        self._readCurrentDoc() # read new file

    def onFileRemoved(self, uuid: str):
        if self.currUUID != uuid:
            return

        self.currUUID = ""
        self.plainDocument.clear()
        
    def _writeCurrentDoc(self):
        if self.currUUID == "":
            return
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += self.currUUID
        File.write(path, self.toPlainText())
        
    def _readCurrentDoc(self):
        if self.currUUID == "":
            return
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += self.currUUID
        content = File.read(path)
        self.setPlainText(content)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        self.updateViewportMargins()
        super().resizeEvent(e)

    def closeEvent(self, e: QCloseEvent | None) -> None:
        self._writeCurrentDoc()

        super().closeEvent(e)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn
