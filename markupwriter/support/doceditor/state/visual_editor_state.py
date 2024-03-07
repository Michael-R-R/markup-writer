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


class VisualEditorState(s.NvEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(QTextCursor.MoveMode.KeepAnchor, editor, parent)

        prefixes = r"g"
        motions = r"b|e|ge|gg|h|j|k|l|w|0|\$"
        commands = r"d|esc|C-D|C-U|" + motions

        self.countRegex = re.compile(r"[1-9]+")
        self.prefixRegex = re.compile(prefixes)
        self.motionRegex = re.compile(motions)
        self.commandRegex = re.compile(commands)

        self.funcDict = {
            "b": self._b,
            "d": self._d,
            "e": self._e,
            "ge": self._ge,
            "gg": self._gg,
            "h": self._h,
            "j": self._j,
            "k": self._k,
            "l": self._l,
            "w": self._w,
            "0": self._0,
            "$": self._dollar,
            "esc": self._esc,
            "C-D": self._C_D,
            "C-U": self._C_U,
        }

    def enter(self):
        pass

    def exit(self):
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        self.editor.setTextCursor(cursor)

    def reset(self):
        super().reset()
        self.moveMode = QTextCursor.MoveMode.KeepAnchor
        
    def process(self, e: QKeyEvent) -> bool:
        return super().process(e)

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

    def _esc(self):
        self.changedState.emit(s.STATE.normal)
