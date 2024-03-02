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

import markupwriter.support.doceditor.state as s


class InsertEditorState(s.BaseEditorState):
    def __init__(
        self, editor: QPlainTextEdit, parent: QObject | None, append: bool = False
    ) -> None:
        super().__init__(editor, parent)
        
        if append:
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Right)
            self.editor.setTextCursor(cursor)

        self.actionDict = {
            Qt.Key.Key_Escape: self.handleEscape,
            Qt.Key.Key_ParenLeft: self._handleLeftParen,
        }

    def enter(self):
        pass

    def exit(self):
        pass

    def process(self, e: QKeyEvent) -> bool:
        key = e.key()
        if key in self.actionDict:
            return self.actionDict[key]()

        return False

    def handleEscape(self) -> bool:
        self.changedState.emit(s.STATE.normal)

        return True

    def _handleLeftParen(self) -> bool:
        cursor = self.editor.textCursor()
        cursor.insertText("()")
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        self.editor.setTextCursor(cursor)

        return True
