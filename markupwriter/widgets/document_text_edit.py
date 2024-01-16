#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QPoint,
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
    tagClicked = pyqtSignal(str, QPoint)
    
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.plainDocument = de.PlainDocument(self)

        self.setDocument(self.plainDocument)
        self.setEnabled(False)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setMouseTracking(True)
        self.setTabStopDistance(20.0)
        self.resizeMargins()

        self.customContextMenuRequested.connect(self.onContextMenu)

    @pyqtSlot(QPoint)
    def onContextMenu(self, pos: QPoint):
        tag = self._checkForTag(pos)
        if tag is None:
            return
        self.tagClicked.emit(tag, pos)

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

    def _checkForTag(self, pos: QPoint) -> str | None:
        cursor = self.cursorForPosition(pos)
        cursorPos = cursor.positionInBlock()
        blockText = cursor.block().text()
        if cursorPos == 0 or cursorPos >= len(blockText):
            return None
        
        found = re.search("^@(pov|loc)", blockText)
        if found is None:
            return None

        rcomma = blockText.rfind(",", 0, cursorPos)
        fcomma = blockText.find(",", cursorPos)
        text = ""

        # single tag
        if rcomma < 0 and fcomma < 0:
            rindex = blockText.rfind("[", 0, cursorPos)
            lindex = blockText.find("]", cursorPos)
            text = blockText[rindex + 1 : lindex]
        # tag start
        elif rcomma < 0 and fcomma > -1:
            index = blockText.rfind("[", 0, cursorPos)
            text = blockText[index + 1 : fcomma]
        # tag middle
        elif rcomma > -1 and fcomma > -1:
            text = blockText[rcomma + 1 : fcomma]
        # tag end
        elif rcomma > -1 and fcomma < 0:
            index = blockText.find("]", cursorPos)
            text = blockText[rcomma + 1 : index]

        return text.strip()
