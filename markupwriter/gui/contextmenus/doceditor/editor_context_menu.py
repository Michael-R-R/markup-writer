#!/usr/bin/python

import enchant

from PyQt6.QtCore import (
    pyqtSlot,
    QPoint,
)

from PyQt6.QtGui import (
    QTextCursor,
    QAction,
)

from PyQt6.QtWidgets import (
    QWidget,
    QPlainTextEdit,
    QMenu,
)

from markupwriter.gui.contextmenus import BaseContextMenu


class EditorContextMenu(BaseContextMenu):
    def __init__(
        self,
        textEdit: QPlainTextEdit,
        endict: enchant.Dict,
        pos: QPoint,
        parent: QWidget | None,
    ) -> None:
        super().__init__(parent)

        self._menu = textEdit.createStandardContextMenu()
        self._textEdit = textEdit
        self._endict = endict
        self._setup(pos)

    def preprocess(self, args: list[object] | None):
        pass

    def postprocess(self, args: list[object] | None):
        pass

    def _setup(self, pos: QPoint):
        cursor = self._textEdit.cursorForPosition(pos)
        cpos = cursor.positionInBlock()
        textBlock = cursor.block().text()
        if cpos > 0 or cpos < len(textBlock):
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            self._textEdit.setTextCursor(cursor)
            word = self._textEdit.textCursor().selectedText()
            self._setupSuggestions(word)

    def _setupSuggestions(self, word: str):
        if self._endict.check(word):
            return

        spellingMenu = QMenu("Spelling suggestions", self._menu)
        slist = self._endict.suggest(word)
        count = 5 if len(slist) > 5 else len(slist)
        for i in range(count):
            action = QAction(slist[i], spellingMenu)
            action.triggered.connect(
                lambda _, val=slist[i]: self._makeWordCorrection(val)
            )
            spellingMenu.addAction(action)
            
        if len(spellingMenu.actions()) > 0:
            actions = self._menu.actions()
            self._menu.insertSeparator(actions[0])
            self._menu.insertMenu(actions[0], spellingMenu)

    def _makeWordCorrection(self, word: str):
        cursor = self._textEdit.textCursor()
        if not cursor.hasSelection():
            return
        
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(word)
        cursor.endEditBlock()
        self._textEdit.setTextCursor(cursor)
