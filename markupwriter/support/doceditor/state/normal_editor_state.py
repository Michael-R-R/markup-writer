#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QObject,
)

from PyQt6.QtGui import (
    QKeyEvent,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
)

import markupwriter.support.doceditor.state as s


class NormalEditorState(s.BaseEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(editor, parent)
        
        self.actionDict = {
            Qt.Key.Key_I: self._enterInsert,
        }
        
    def enter(self):
        pass
    
    def exit(self):
        pass
    
    def process(self, e: QKeyEvent) -> bool:
        key = e.key()
        if key in self.actionDict:
            self.actionDict[key]()
        
        return True
        
    def _enterInsert(self):
        self.changedState.emit(s.STATE.insert)
