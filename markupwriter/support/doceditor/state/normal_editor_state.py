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

from markupwriter.common.provider import Key

import markupwriter.support.doceditor.state as s


class NormalEditorState(s.BaseEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(editor, parent)

        prefixes = r"g"
        operators = r"d"
        motions = r"dd|gg|h|j|k|l|w|0|\$"
        commands = r"i|u|v|x|" + motions

        self.countRegex = re.compile(r"[1-9]+")
        self.prefixRegex = re.compile(prefixes)
        self.opRegex = re.compile(operators)
        self.motionRegex = re.compile(motions)
        self.commandRegex = re.compile(commands)

        self.buffer = ""
        self.hasPrefix = False
        self.hasOp = False
        self.moveMode = QTextCursor.MoveMode.MoveAnchor

        self.funcDict = {
            "dd": self._dd,
            "gg": self._gg,
            "h": self._h,
            "i": self._i,
            "j": self._j,
            "k": self._k,
            "l": self._l,
            "u": self._u,
            "v": self._v,
            "w": self._w,
            "x": self._x,
            "0": self._0,
            "$": self._dollar,
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

    def build(self, e: QKeyEvent) -> bool:
        # Ignore modifier keys
        isShift = Qt.Key.Key_Shift == e.key()
        isCtrl = Qt.Key.Key_Control == e.key()
        isAlt = Qt.Key.Key_Alt == e.key()
        if isShift or isCtrl or isAlt:
            return False
        
        # Get the converted key.
        ckey: str = Key.get(e.modifiers(), e.key())
        if ckey is None:
            self.reset()
            return False

        # Build the buffer.
        self.buffer += ckey

        # Found count. Continue building the buffer.
        countFound = self.countRegex.search(ckey)
        if countFound is not None:
            return False

        # Previous ckey was a prefix. Check if we now
        # have a valid operator or command to process.
        if self.hasPrefix:
            hasOp = self.opRegex.search(self.buffer) is not None
            hasCmd = self.commandRegex.search(self.buffer) is not None
            if not (hasOp or hasCmd):
                self.reset()
                return False
            self.hasPrefix = False
        # Check if this ckey is a prefix to a operator
        # or command.
        else:
            prefixFound = self.prefixRegex.search(ckey)
            if prefixFound is not None:
                self.hasPrefix = True
                return False
            
        # A command was entered after an operator,
        # so process it.
        if self.hasOp:
            # Make sure we aren't processing a prefixed
            # command.
            if not self.hasPrefix:
                return True

        # Check if we have a valid operator.
        opFound = self.opRegex.search(self.buffer)
        if opFound is not None:
            self.hasOp = True
            return False

        # Check to see if the command is valid,
        # if not then reset the buffer.
        cmdFound = self.commandRegex.search(self.buffer)
        if cmdFound is None:
            self.reset()
            return False

        return True

    def evaluate(self):
        # Parse the count
        count = 1
        it = self.countRegex.finditer(self.buffer)
        for found in it:
            num = int(found.group(0))
            count *= num
            self.buffer = self.buffer.replace(found.group(0), "", 1)

        # Parse the command
        cmd = None
        found = self.commandRegex.search(self.buffer)
        if found is not None:
            cmd = found.group(0)
        else:
            return

        # Parse the operator
        op = None
        if self.hasOp:
            found = self.opRegex.search(self.buffer)
            op = found.group(0)
            
            # Make sure we are operating on a 
            # motion command.
            found = self.motionRegex.search(cmd)
            if found is None:
                return
            
            self.moveMode = QTextCursor.MoveMode.KeepAnchor

        for _ in range(count):
            self.funcDict[cmd]()

        if op is not None:
            self.opDict[op]()

    def reset(self):
        self.buffer = ""
        self.hasPrefix = False
        self.hasOp = False
        self.moveMode = QTextCursor.MoveMode.MoveAnchor

    def _a(self):
        self.changedState.emit(s.STATE.append)

    def _dd(self):
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.deleteChar()
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)

    def _gg(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.movePosition(QTextCursor.MoveOperation.Start, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _h(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Left, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _i(self):
        self.changedState.emit(s.STATE.insert)

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

    def _u(self):
        self.editor.undo()

    def _v(self):
        self.changedState.emit(s.STATE.visual)

    def _w(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.NextWord, self.moveMode)
        self.editor.setTextCursor(cursor)

    def _x(self):
        cursor = self.editor.textCursor()
        cursor.deleteChar()
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
