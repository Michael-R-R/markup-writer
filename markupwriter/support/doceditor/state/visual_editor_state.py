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


class VisualEditorState(s.BaseEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(editor, parent)

        prefixes = r"g"
        commands = r"d|gg|h|j|k|l|esc"

        self.countRegex = re.compile(r"[1-9]+")
        self.prefixRegex = re.compile(prefixes)
        self.commandRegex = re.compile(commands)

        self.buffer = ""
        self.hasPrefix = False
        self.moveMode = QTextCursor.MoveMode.KeepAnchor

        self.funcDict = {
            "d": self._d,
            "gg": self._gg,
            "h": self._h,
            "j": self._j,
            "k": self._k,
            "l": self._l,
            "esc": self._esc,
        }

    def enter(self):
        pass

    def exit(self):
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        self.editor.setTextCursor(cursor)

    def process(self, e: QKeyEvent) -> bool:
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
            hasCmd = self.commandRegex.search(self.buffer) is not None
            if not hasCmd:
                self.reset()
                return False
            return True
        # Check if this ckey is a prefix to a command.
        else:
            prefixFound = self.prefixRegex.search(ckey)
            if prefixFound is not None:
                self.hasPrefix = True
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
        
        for _ in range(count):
            self.funcDict[cmd]()

    def reset(self):
        self.buffer = ""
        self.hasPrefix = False
        self.moveMode = QTextCursor.MoveMode.KeepAnchor

    def _d(self):
        cursor = self.editor.textCursor()

        cursor.beginEditBlock()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        else:
            cursor.deleteChar()
        cursor.endEditBlock()

        self.editor.setTextCursor(cursor)
        self.changedState.emit(s.STATE.normal)

    def _gg(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start, self.moveMode)
        self.editor.setTextCursor(cursor)

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

    def _esc(self):
        self.changedState.emit(s.STATE.normal)
