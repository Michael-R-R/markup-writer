#!/usr/bin/python

import re

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

        self.countRegex = re.compile(r"[0-9]+")
        self.opRegex = re.compile(r"d")
        self.motionRegex = re.compile(r"(h|j|k|l|d)")
        self.commandRegex = re.compile(r"(h|j|k|l|d|u)")

        self.buffer = ""
        self.hasOp = False
        self.moveMode = QTextCursor.MoveMode.MoveAnchor
        
        self.funcDict = {
            "h": self._h,
            "j": self._j,
            "k": self._k,
            "l": self._l,
            "d": self._d,
            "u": self._u,
        }
        
        self.opDict = {
            "d": self._d_op,
        }

    def enter(self):
        pass

    def exit(self):
        pass

    def process(self, e: QKeyEvent) -> bool:
        if e.key() == Qt.Key.Key_Escape:
            self.reset()
            return True

        if self.build(e):
            self.evaluate()
            self.reset()

        return True

    def reset(self):
        self.buffer = ""
        self.hasOp = False
        self.moveMode = QTextCursor.MoveMode.MoveAnchor

    def build(self, e: QKeyEvent) -> bool:
        ckey = self.fetchKey(e.modifiers(), e.key())
        self.buffer += ckey

        if ckey.isnumeric():
            return False

        if self.hasOp:
            return True

        found = self.opRegex.search(ckey)
        self.hasOp = found is not None
        if self.hasOp:
            return False

        found = self.commandRegex.search(ckey)
        isCommand = found is not None

        return isCommand

    def evaluate(self):
        count = 1
        it = self.countRegex.finditer(self.buffer)
        for found in it:
            num = int(found.group(0))
            count *= num
            self.buffer = self.buffer.replace(found.group(0), "", 1)

        op = None
        found = self.opRegex.search(self.buffer)
        if found is not None:
            op = found.group(0)
            self.buffer = self.buffer.replace(found.group(0), "", 1)
            
        cmd = None
        found = self.commandRegex.search(self.buffer)
        if found is not None:
            cmd = found.group(0)
            self.buffer = self.buffer.replace(found.group(0), "", 1)
        else:
            return

        if self.hasOp:
            found = self.motionRegex.search(cmd)
            if found is None:
                return
            self.moveMode = QTextCursor.MoveMode.KeepAnchor
        
        for _ in range(count):
            self.funcDict[cmd]()
            
        if op is not None:
            self.opDict[op]()

    def _i(self):
        self.changedState.emit(s.STATE.insert)

    def _v(self):
        self.changedState.emit(s.STATE.visual)

    def _h(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Left, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _j(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Down, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _k(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Up, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _l(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Right, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _d(self):
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.deleteChar()
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)

    def _x(self):
        cursor = self.editor.textCursor()
        cursor.deleteChar()
        self.editor.setTextCursor(cursor)

    def _a(self):
        self.changedState.emit(s.STATE.append)

    def _u(self):
        self.editor.undo()

    def _w(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.NextWord, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _0(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _dollar(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, self.moveMode)
        self.editor.setTextCursor(cursor)
        
    def _d_op(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)
