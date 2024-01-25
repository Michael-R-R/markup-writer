#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QPoint,
    QTimer,
)

from PyQt6.QtGui import (
    QKeyEvent,
    QMouseEvent,
    QResizeEvent,
    QTextOption,
    QTextCursor,
    QGuiApplication,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QFrame,
)

from markupwriter.common.syntax import (
    Highlighter,
)

import markupwriter.support.doceditor as de


class DocumentEditorWidget(QPlainTextEdit):
    tagHovered = pyqtSignal(str)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.plainDocument = de.PlainDocument(self)
        self.highlighter = Highlighter(self.plainDocument)

        self.hoverTag = ""
        self.hoverTimer = QTimer(self)
        self.hoverTimer.timeout.connect(self._onTimer)
        self.canResizeMargins = True

        self.setDocument(self.plainDocument)
        self.setEnabled(False)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setMouseTracking(True)
        self.setTabStopDistance(20.0)
        self.resizeMargins()
        
    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)

    def resizeMargins(self):
        if not self.canResizeMargins:
            return 
        
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

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        cursor = de.KeyProcessor.process(self.textCursor(), e.key())
        self.setTextCursor(cursor)

        super().keyPressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
        if e.buttons() == Qt.MouseButton.LeftButton:
            self.hoverTimer.stop()
        else:
            tag = self._checkForTag(e.pos())
            if self.hoverTimer.isActive():
                if tag is None:
                    self.hoverTimer.stop()
            else:
                if tag is not None:
                    self.hoverTag = tag
                    self.hoverTimer.start(1000)

        super().mouseMoveEvent(e)

    def _onTimer(self):
        self.hoverTimer.stop()
        self.tagHovered.emit(self.hoverTag)

    def _checkForTag(self, pos: QPoint) -> str | None:
        cursor = self.cursorForPosition(pos)
        cursorPos = cursor.positionInBlock()
        blockText = cursor.block().text()
        if cursorPos <= 0 or cursorPos >= len(blockText):
            return None

        tagFound = re.search(r"^@(ref|pov|loc)(\(.*\))", blockText)
        if tagFound is None:
            return None

        rcomma = blockText.rfind(",", 0, cursorPos)
        fcomma = blockText.find(",", cursorPos)
        text = None

        # single tag
        if rcomma < 0 and fcomma < 0:
            rindex = blockText.rfind("(", 0, cursorPos)
            lindex = blockText.find(")", cursorPos)
            text = blockText[rindex + 1 : lindex].strip()
        # tag start
        elif rcomma < 0 and fcomma > -1:
            index = blockText.rfind("(", 0, cursorPos)
            text = blockText[index + 1 : fcomma].strip()
        # tag middle
        elif rcomma > -1 and fcomma > -1:
            text = blockText[rcomma + 1 : fcomma].strip()
        # tag end
        elif rcomma > -1 and fcomma < 0:
            index = blockText.find(")", cursorPos)
            text = blockText[rcomma + 1 : index].strip()

        return text
