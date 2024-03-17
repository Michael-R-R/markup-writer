#!/usr/bin/python

from PyQt6.QtCore import (
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
from markupwriter.support.doceditor import SpellCheck
from markupwriter.common.syntax import Highlighter


class EditorContextMenu(BaseContextMenu):
    def __init__(
        self,
        textEdit: QPlainTextEdit,
        spellCheck: SpellCheck,
        highlighter: Highlighter,
        pos: QPoint,
        parent: QWidget | None,
    ) -> None:
        super().__init__(parent)

        self._menu = textEdit.createStandardContextMenu()
        self._textEdit = textEdit
        self._spellCheck = spellCheck
        self._highlighter = highlighter

        self._setup(pos)

    def preprocess(self, args: list[object] | None):
        pass

    def postprocess(self, args: list[object] | None):
        pass

    def _setup(self, pos: QPoint):
        cursor = self._textEdit.textCursor()
        if cursor.hasSelection():
            return
        
        cursor = self._textEdit.cursorForPosition(pos)
        
        cpos = cursor.positionInBlock()
        block = cursor.block()
        text = block.text()
        
        if cpos > 0 or cpos < len(text):
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            self._textEdit.setTextCursor(cursor)
            word = self._textEdit.textCursor().selectedText()
            if word == "":
                return

            actions = self._menu.actions()
            self._menu.insertSeparator(actions[0])

            endict = self._spellCheck.endict
            if not endict.check(word):
                self._setupAddWord(word)
                self._setupSuggestions(word)
                
            self._setupForgetWord(word)

    def _setupAddWord(self, word: str):
        action = QAction("Add word", self._menu)
        action.triggered.connect(lambda _, val=word: self._addWord(val))

        actions = self._menu.actions()
        self._menu.insertAction(actions[0], action)

    def _setupSuggestions(self, word: str):
        spellingMenu = QMenu("Spelling suggestions", self._menu)

        endict = self._spellCheck.endict
        slist = endict.suggest(word)
        count = 5 if len(slist) > 5 else len(slist)

        for i in range(count):
            action = QAction(slist[i], spellingMenu)
            action.triggered.connect(lambda _, val=slist[i]: self._correctWord(val))
            spellingMenu.addAction(action)

        if len(spellingMenu.actions()) > 0:
            actions = self._menu.actions()
            self._menu.insertMenu(actions[0], spellingMenu)

    def _setupForgetWord(self, word: str):
        if not self._spellCheck.hasWord(word):
            return

        action = QAction("Forget word", self._menu)
        action.triggered.connect(lambda _, val=word: self._forgetWord(val))
        
        actions = self._menu.actions()
        self._menu.insertAction(actions[0], action)
            
    def _addWord(self, word: str):
        self._spellCheck.addWord(word)
        self._highlighter.rehighlight()
        
    def _correctWord(self, word: str):
        cursor = self._textEdit.textCursor()
        if not cursor.hasSelection():
            return

        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(word)
        cursor.endEditBlock()

        self._textEdit.setTextCursor(cursor)

    def _forgetWord(self, word: str):
        self._spellCheck.removeWord(word)
        self._highlighter.rehighlight()
