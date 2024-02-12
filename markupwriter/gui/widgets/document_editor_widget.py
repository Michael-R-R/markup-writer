#!/usr/bin/python

import re
import enchant

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QPoint,
    QMimeData,
)

from PyQt6.QtGui import (
    QContextMenuEvent,
    QKeyEvent,
    QMouseEvent,
    QResizeEvent,
    QTextOption,
    QTextCursor,
    QGuiApplication,
    QAction,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QFrame,
    QMenu,
)

from markupwriter.common.syntax import Highlighter

import markupwriter.support.doceditor as de


class DocumentEditorWidget(QPlainTextEdit):
    tagPopupRequested = pyqtSignal(str, int)
    tagPreviewRequested = pyqtSignal(str, int)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.plainDocument = de.PlainDocument(self)
        self.enchantDict = enchant.Dict("en_US")
        self.highlighter = Highlighter(self.plainDocument, self.enchantDict)
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

    def canInsertFromMimeData(self, source: QMimeData | None) -> bool:
        hasUrls = source.hasUrls()
        status = super().canInsertFromMimeData(source)

        return hasUrls or status

    def insertFromMimeData(self, source: QMimeData | None) -> None:
        if source.hasUrls():
            extRegex = re.compile(r"\b\.(jpeg|jpg|png|gif)\b")
            for url in source.urls():
                imgPath = url.path()
                found = extRegex.search(url.toString().strip())
                if found is None:
                    continue
                imgTag = "@img({})\n".format(imgPath)
                self.textCursor().insertText(imgTag)
        else:
            return super().insertFromMimeData(source)
        
    # TODO refactor this
    def contextMenuEvent(self, e: QContextMenuEvent | None) -> None:
        menu = self.createStandardContextMenu()
        
        cursor = self.cursorForPosition(e.pos())
        cpos = cursor.positionInBlock()
        textBlock = cursor.block().text()
        if cpos > 0 or cpos < len(textBlock):
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            self.setTextCursor(cursor)
            word = self.textCursor().selectedText()
            if not self.enchantDict.check(word):
                spellingMenu = QMenu("Spelling suggestions")
                slist = self.enchantDict.suggest(word)
                count = 5 if len(slist) > 5 else len(slist)
                for i in range(count):
                    action = QAction(slist[i], spellingMenu)
                    action.triggered.connect(lambda _, val=slist[i]: self.makeWordCorrection(val))
                    spellingMenu.addAction(action)
                if len(spellingMenu.actions()) > 0:
                    menu.insertSeparator(menu.actions()[0])
                    menu.insertMenu(menu.actions()[0], spellingMenu)
        
        menu.exec(e.globalPos())
        
    # TODO refactor this
    def makeWordCorrection(self, word: str):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(word)
        cursor.endEditBlock()
        self.setTextCursor(cursor)

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
                pair: tuple[str, int] = self._onTextBlockClicked(e.pos())
                if pair != (None, None):
                    self.tagPopupRequested.emit(pair[0], pair[1])
                return None
        elif e.modifiers() == (ctrl | alt):
            if e.button() == button:
                pair: tuple[str, int] = self._onTextBlockClicked(e.pos())
                if pair != (None, None):
                    self.tagPreviewRequested.emit(pair[0], pair[1])
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
