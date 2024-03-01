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
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(editor, parent)
        
        self.actionDict = {
            Qt.Key.Key_Escape: self._enterNormal,
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
    
    def _enterNormal(self) -> bool:
        self.changedState.emit(s.STATE.normal)
        
        return True
    
    def _handleLeftParen(self) -> bool:
        cursor = self.editor.textCursor()
        cursor.insertText("()")
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        self.editor.setTextCursor(cursor)
        
        return True
