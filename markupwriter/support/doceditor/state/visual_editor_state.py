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


class VisualEditorState(s.BaseEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(editor, parent)

    def enter(self):
        pass

    def exit(self):
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        self.editor.setTextCursor(cursor)

    def process(self, e: QKeyEvent) -> bool:
        pass

    def _handleEscape(self):
        self.changedState.emit(s.STATE.normal)

    def _handleHKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(
            QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor
        )
        self.editor.setTextCursor(cursor)

    def _handleJKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(
            QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.KeepAnchor
        )
        self.editor.setTextCursor(cursor)

    def _handleKKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(
            QTextCursor.MoveOperation.Up, QTextCursor.MoveMode.KeepAnchor
        )
        self.editor.setTextCursor(cursor)

    def _handleLKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(
            QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor
        )
        self.editor.setTextCursor(cursor)
