#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QPoint,
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
    tagPopupRequested = pyqtSignal(str)
    tagPreviewRequested = pyqtSignal(str)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.plainDocument = de.PlainDocument(self)
        self.highlighter = Highlighter(self.plainDocument)

        self.canResizeMargins = True

        self.setDocument(self.plainDocument)
        self.setEnabled(False)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(20.0)
        self.resizeMargins()

    def reset(self):
        self.clear()
        self.setEnabled(False)

    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        self.centerCursor()

    def moveCursorTo(self, pos: int):
        cursor = self.textCursor()
        cursor.setPosition(pos)
        self.setTextCursor(cursor)
        self.centerCursor()

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

        return super().resizeEvent(e)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        cursor = de.KeyProcessor.process(self.textCursor(), e.key())
        self.setTextCursor(cursor)

        return super().keyPressEvent(e)

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        ctrl = Qt.KeyboardModifier.ControlModifier
        alt = Qt.KeyboardModifier.AltModifier
        button = Qt.MouseButton.LeftButton

        if e.modifiers() == ctrl:
            if e.button() == button:
                tag = self._checkForTag(e.pos())
                if tag is not None:
                    self.tagPopupRequested.emit(tag)
                return None
        elif e.modifiers() == (ctrl | alt):
            if e.button() == button:
                tag = self._checkForTag(e.pos())
                if tag is not None:
                    self.tagPreviewRequested.emit(tag)
                return None

        return super().mousePressEvent(e)
    
    def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
        viewport = self.viewport()
        mods = e.modifiers()
        ctrl = Qt.KeyboardModifier.ControlModifier
        alt = Qt.KeyboardModifier.AltModifier
        if mods == ctrl or mods == (ctrl | alt):
            tag = self._checkForTag(e.pos())
            if tag is not None:
                viewport.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                viewport.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            viewport.setCursor(Qt.CursorShape.IBeamCursor)
        
        return super().mouseMoveEvent(e)

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
