#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QPoint,
    QSize,
    QMimeData,
    QDataStream,
)

from PyQt6.QtGui import (
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

import markupwriter.support.doceditor as de
import markupwriter.support.doceditor.state as s


class DocumentEditorWidget(QPlainTextEdit):
    stateChanged = pyqtSignal(str)
    docStatusChanged = pyqtSignal(bool)
    showRefPopupClicked = pyqtSignal(QPoint)
    showRefPreviewClicked = pyqtSignal(QPoint)
    wordCountChanged = pyqtSignal(str, int)
    resized = pyqtSignal(QSize)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.state: s.BaseEditorState = None
        self.plainDocument = de.PlainDocument(self)
        self.spellChecker = de.SpellCheck()
        self.highlighter = Highlighter(self.plainDocument, self.spellChecker.endict)
        self.searchHotkey = QAction("search", self)
        self.canResizeMargins = True
        self.docUUID = ""

        shortcut = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_F)
        self.searchHotkey.setShortcut(shortcut)
        self.addAction(self.searchHotkey)

        self.setDocument(self.plainDocument)
        self.setEnabled(False)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setTabStopDistance(20.0)
        
        self.setState(s.NormalEditorState(self, self))

    def reset(self):
        self.clear()
        self.setEnabled(False)
        self.docUUID = ""
        self.docStatusChanged.emit(False)

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
        
    def setDocumentText(self, uuid: str, text: str, cpos: int):
        if uuid == "":
            self.reset()
            return
        
        self.docUUID = uuid
        self.setPlainText(text)
        self.moveCursorTo(cpos)
        self.setEnabled(True)
        self.docStatusChanged.emit(True)
    
    def hasOpenDocument(self) -> bool:
        return self.docUUID != ""
    
    def setState(self, state: s.BaseEditorState):
        if self.state is not None:
            self.state.exit()
        
        self.state = state
        self.state.enter()
        
        self.state.changedState.connect(self.onChangedState)
    
    @pyqtSlot(s.STATE)
    def onChangedState(self, state: s.STATE):
        match state:
            case s.STATE.normal:
                self.setState(s.NormalEditorState(self, self))
                self.stateChanged.emit("-- NORMAL -- ")
            case s.STATE.insert:
                self.setState(s.InsertEditorState(self, self))
                self.stateChanged.emit("-- INSERT --")
            case s.STATE.append:
                self.setState(s.InsertEditorState(self, self, True))
                self.stateChanged.emit("-- INSERT --")
            case s.STATE.visual:
                self.setState(s.VisualEditorState(self, self))
                self.stateChanged.emit("-- VISUAL --")

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
                imgTag = "@img({})".format(imgPath)
                self.textCursor().insertText(imgTag)
        else:
            return super().insertFromMimeData(source)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        if self.canResizeMargins:
            self.canResizeMargins = False
            self.resized.emit(e.size())
            self.canResizeMargins = True
        
        return super().resizeEvent(e)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())

        if not self.state.process(e):
            super().keyPressEvent(e)

    def keyReleaseEvent(self, e: QKeyEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())

        return super().keyReleaseEvent(e)

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        ctrl = Qt.KeyboardModifier.ControlModifier
        alt = Qt.KeyboardModifier.AltModifier
        button = Qt.MouseButton.LeftButton

        if e.modifiers() == ctrl:
            if e.button() == button:
                self.showRefPopupClicked.emit(e.pos())
                return None
        elif e.modifiers() == (ctrl | alt):
            if e.button() == button:
                self.showRefPreviewClicked.emit(e.pos())
                return None

        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())

        return super().mouseMoveEvent(e)

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
