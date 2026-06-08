#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QObject,
)

from PyQt6.QtGui import (
    QKeyEvent,
    QTextCursor,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
)

from markupwriter.common.provider import Key

import markupwriter.support.doceditor.state as s


class InsertEditorState(s.BaseEditorState):
    def __init__(
        self, editor: QPlainTextEdit, parent: QObject | None, append: bool = False
    ) -> None:
        super().__init__(editor, parent)
        
        self.funcDict = {
            "(": self._lparen,
            "backspace": self._backspace,
            "esc": self._esc,
            "tab": self._tab,
        }
        
        if append:
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Right)
            self.editor.setTextCursor(cursor)

    def enter(self):
        pass

    def exit(self):
        pass

    def process(self, e: QKeyEvent) -> bool:
        ckey: str = Key.get(e.modifiers(), e.key())
        if ckey in self.funcDict:
            return self.funcDict[ckey]()
        
        return False

    def _lparen(self) -> bool:
        cursor = self.editor.textCursor()
        cursor.insertText("()")
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        self.editor.setTextCursor(cursor)

        return True

    def _backspace(self) -> bool:
        cursor = self.editor.textCursor()

        # get the character to the left of the cursor
        cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor)
        lcharacter = cursor.selectedText()
        cursor.clearSelection()
        if lcharacter != "(":
            return False

        # get the character to the right of the cursor original position
        cursor.movePosition(QTextCursor.MoveOperation.Right)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
        rcharacter = cursor.selectedText()
        cursor.clearSelection()
        if rcharacter != ")":
            return False
        
        # delete the parentheses
        cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, 2)
        cursor.removeSelectedText()
        self.editor.setTextCursor(cursor)

        return True

    def _esc(self) -> bool:
        self.changedState.emit(s.STATE.normal)

        return True
    
    def _tab(self) -> bool:
        cursor = self.editor.textCursor()

        # get the character to the right of the cursor original position
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
        rcharacter = cursor.selectedText()
        cursor.clearSelection()
        if rcharacter != ")":
            return False
        
        self.editor.setTextCursor(cursor)

        return True
