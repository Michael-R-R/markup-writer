#!/usr/bin/python

import re

from PyQt6.QtCore import (
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


class VisualEditorState(s.BaseNvEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(QTextCursor.MoveMode.KeepAnchor, editor, parent)

        leaders = r"g"
        specialMotion = r"\$"
        motions = r"b|e|ge|gg|h|j|k|l|w|0"
        commands = r"d|p|y|esc|C-D|C-U|" + motions

        self.leaderRegex = re.compile(leaders)
        self.motionRegex = re.compile(
            "\\b({})\\b|\\B({})\\B".format(motions, specialMotion)
        )
        self.commandRegex = re.compile(
            "\\b({})\\b|\\B({})\\B".format(commands, specialMotion)
        )

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
            "p": self._p,
            "w": self._w,
            "y": self._y,
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
        self.editor.copy()
        
        cursor = self.editor.textCursor()

        cursor.beginEditBlock()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        else:
            cursor.deleteChar()
        cursor.endEditBlock()

        self.editor.setTextCursor(cursor)
        self.changedState.emit(s.STATE.normal)

    def _esc(self):
        self.changedState.emit(s.STATE.normal)
