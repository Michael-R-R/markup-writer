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

import markupwriter.support.doceditor as de
import markupwriter.support.doceditor.state as s


class InsertEditorState(s.BaseEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(editor, parent)
        
    def enter(self):
        pass
    
    def exit(self):
        pass
    
    def process(self, e: QKeyEvent):
        cursor = de.KeyProcessor.process(self.editor.textCursor(), e.key())
        self.editor.setTextCursor(cursor)
        
        # TODO some how call super().keyPressEvent
