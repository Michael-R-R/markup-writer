#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QPoint,
    QSize,
    QMimeData,
    QDataStream,
)

from PyQt6.QtGui import (
    QContextMenuEvent,
    QKeyEvent,
    QMouseEvent,
    QResizeEvent,
    QTextOption,
    QTextCursor,
    QAction,
    QKeySequence,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QFrame,
)

from markupwriter.common.syntax import Highlighter
from markupwriter.gui.contextmenus.doceditor import EditorContextMenu

import markupwriter.support.doceditor as de


class DocumentEditorWidget(QPlainTextEdit):
    statusChanged = pyqtSignal(bool)
    popupRequested = pyqtSignal(str, int)
    previewRequested = pyqtSignal(str, int)
    wordCountChanged = pyqtSignal(str, int)
    resized = pyqtSignal(QSize)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.plainDocument = de.PlainDocument(self)
        self.spellChecker = de.SpellCheck()
        self.highlighter = Highlighter(self.plainDocument, self.spellChecker.endict)
        self.searchHotkey = QAction("search", self)
        self.canResizeMargins = True
        self.docUUID = ""

        shortcut = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_F)
        self.searchHotkey.setShortcut(shortcut)

        self.setDocument(self.plainDocument)
        self.setEnabled(False)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setTabStopDistance(20.0)

    def reset(self):
        self.clear()
        self.setEnabled(False)
        self.docUUID = ""
        self.statusChanged.emit(False)

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
    
    def runWordCount(self):
        if not self.hasDocument():
            return
        
        uuid = self.docUUID
        text = self.toPlainText()
        count = len(re.findall(r"[a-zA-Z'-]+", text))
        
        self.wordCountChanged.emit(uuid, count)
    
    def hasDocument(self) -> bool:
        return self.docUUID != ""

    def canInsertFromMimeData(self, source: QMimeData | None) -> bool:
        hasUrls = source.hasUrls()
        status = super().canInsertFromMimeData(source)

        return hasUrls or status

    def insertFromMimeData(self, source: QMimeData | None) -> None:
        if source.hasUrls():
            extRegex = re.compile(r"\b\.(jpeg|jpg|png|gif)\b")
            for url in source.urls():
                imgPath = url.path()
                found = extRegex.search(imgPath)
                if found is None:
                    continue
                imgTag = "@img({})\n".format(imgPath)
                self.textCursor().insertText(imgTag)
        else:
            return super().insertFromMimeData(source)

    def contextMenuEvent(self, e: QContextMenuEvent | None) -> None:
        contextMenu = EditorContextMenu(
            self, self.spellChecker, self.highlighter, e.pos(), self
        )
        contextMenu.onShowMenu(e.globalPos())

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        self.resized.emit(e.size())
        
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
                pair: tuple[str, int] = self._onTextBlockClicked(e.pos())
                if pair != (None, None):
                    self.popupRequested.emit(pair[0], pair[1])
                return None
        elif e.modifiers() == (ctrl | alt):
            if e.button() == button:
                pair: tuple[str, int] = self._onTextBlockClicked(e.pos())
                if pair != (None, None):
                    self.previewRequested.emit(pair[0], pair[1])
                return None

        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())

        return super().mouseMoveEvent(e)

    def _onTextBlockClicked(self, pos: QPoint) -> tuple[str | None, int | None]:
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

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.spellChecker
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.spellChecker
        return sin
