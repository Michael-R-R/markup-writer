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


class NormalEditorState(s.BaseEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(editor, parent)
        
        self.actionDict = {
            Qt.Key.Key_I: self._handleIKey,
            Qt.Key.Key_V: self._handleVKey,
            Qt.Key.Key_H: self._handleHKey,
            Qt.Key.Key_J: self._handleJKey,
            Qt.Key.Key_K: self._handleKKey,
            Qt.Key.Key_L: self._handleLKey,
            Qt.Key.Key_X: self._handleXKey,
            Qt.Key.Key_A: self._handleAKey,
        }
        
    def enter(self):
        pass
    
    def exit(self):
        pass
    
    def process(self, e: QKeyEvent) -> bool:
        key = e.key()
        if key in self.actionDict:
            self.actionDict[key]()
            
        super().process(e)
        
        return True
        
    def _handleIKey(self):
        self.changedState.emit(s.STATE.insert)
        
    def _handleVKey(self):
        self.changedState.emit(s.STATE.visual)
    
    def _handleHKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        self.editor.setTextCursor(cursor)
    
    def _handleJKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Down)
        self.editor.setTextCursor(cursor)
    
    def _handleKKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Up)
        self.editor.setTextCursor(cursor)
    
    def _handleLKey(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Right)
        self.editor.setTextCursor(cursor)
        
    def _handleXKey(self):
        cursor = self.editor.textCursor()
        cursor.deleteChar()
        self.editor.setTextCursor(cursor)
        
    def _handleAKey(self):
        self.changedState.emit(s.STATE.append)
