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
        
        self.commands = {
            "h": self._h,
            "j": self._j,
            "k": self._k,
            "l": self._l,
        }

    def enter(self):
        pass

    def exit(self):
        pass

    def process(self, e: QKeyEvent) -> bool:
        if e.key() == Qt.Key.Key_Escape:
            self.reset()
            return True
        
        if self.check(e):
            self.evaluate()
            self.reset()
        
        return True
    
    def check(self, e: QKeyEvent) -> bool:
        key = e.key()
        ckey = ""
        
        match e.modifiers():
            case Qt.KeyboardModifier.NoModifier:
                if key in self.nConvertDict:
                    ckey = self.nConvertDict[key]
            case Qt.KeyboardModifier.ShiftModifier:
                if key in self.sConvertDict:
                    ckey = self.sConvertDict[key]
            case Qt.KeyboardModifier.ControlModifier:
                if key in self.cConvertDict:
                    ckey = self.cConvertDict[key]
                
        self.buffer += ckey
        
        return self.hasCommand()
    
    def evaluate(self):
        # parse count(s)
        count = self.evalCount()
        
        # parse command
        command = self.evalCommand()
        
        # parse operators
        operator = self.evalOperator()
        
        if command in self.commands:
            for _ in range(count):
                self.commands[command]()
        
        print(count, operator, command)

    def _I(self):
        self.changedState.emit(s.STATE.insert)

    def _V(self):
        self.changedState.emit(s.STATE.visual)

    def _h(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        self.editor.setTextCursor(cursor)

    def _j(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Down)
        self.editor.setTextCursor(cursor)

    def _k(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Up)
        self.editor.setTextCursor(cursor)

    def _l(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Right)
        self.editor.setTextCursor(cursor)

    def _X(self):
        cursor = self.editor.textCursor()
        cursor.deleteChar()
        self.editor.setTextCursor(cursor)

    def _A(self):
        self.changedState.emit(s.STATE.append)

    def _D(self):
        self.operator = Qt.Key.Key_D

    def _U(self):
        self.editor.undo()

    def _W(self, mode = QTextCursor.MoveMode.MoveAnchor):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.NextWord, mode)
        self.editor.setTextCursor(cursor)
        
    def _0(self, mode = QTextCursor.MoveMode.MoveAnchor):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, mode)
        self.editor.setTextCursor(cursor)
        
    def _shift4(self, mode = QTextCursor.MoveMode.MoveAnchor):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, mode)
        self.editor.setTextCursor(cursor)

    def _D_Operator(self, key: Qt.Key):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)
