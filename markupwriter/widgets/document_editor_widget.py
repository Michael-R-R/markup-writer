#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
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
    tagPopupRequested = pyqtSignal(str, int)
    tagPreviewRequested = pyqtSignal(str, int)

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
        self._onChangeCursorShape(e.modifiers(), self.viewport())
        
        cursor = de.KeyProcessor.process(self.textCursor(), e.key())
        self.setTextCursor(cursor)

        return super().keyPressEvent(e)
    
    def keyReleaseEvent(self, e: QKeyEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())
        
        return super().keyReleaseEvent(e)

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        ctrl = Qt.KeyboardModifier.ControlModifier
        alt = Qt.KeyboardModifier.AltModifier
        button = Qt.MouseButton.LeftButton

        if e.modifiers() == ctrl:
            if e.button() == button:
                pair: (str, int) = self._onTextBlockClicked(e.pos())
                if pair != (None, None):
                    self.tagPopupRequested.emit(pair[0], pair[1])
                return None
        elif e.modifiers() == (ctrl | alt):
            if e.button() == button:
                pair: (str, int) = self._onTextBlockClicked(e.pos())
                if pair != (None, None):
                    self.tagPreviewRequested.emit(pair[0], pair[1])
                return None

        return super().mousePressEvent(e)
    
    def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())
        
        return super().mouseMoveEvent(e)
    
    def _onTextBlockClicked(self, pos: QPoint) -> (str | None, int | None):
        cursor = self.cursorForPosition(pos)
        cpos = cursor.positionInBlock()
        textBlock = cursor.block().text()
        if cpos <= 0 or cpos >= len(textBlock):
            return (None, None)
        
        return (textBlock, cpos)
    
    def _onChangeCursorShape(self, mods: Qt.KeyboardModifier, vp: QWidget):
        ctrl = Qt.KeyboardModifier.ControlModifier
        alt = Qt.KeyboardModifier.AltModifier
        
        if mods == ctrl or mods == (ctrl | alt):
            vp.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            vp.setCursor(Qt.CursorShape.IBeamCursor)
