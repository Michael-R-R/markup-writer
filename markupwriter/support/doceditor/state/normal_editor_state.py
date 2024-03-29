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


class NormalEditorState(s.BaseNvEditorState):
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(QTextCursor.MoveMode.MoveAnchor, editor, parent)

        leaders = r"g"
        operators = r"d"
        specialMotion = r"\$"
        motions = r"b|d|e|ge|gg|h|j|k|l|w|0"
        commands = r"a|i|p|u|v|x|y|C-D|C-R|C-U|" + motions

        self.leaderRegex = re.compile(leaders)
        self.operRegex = re.compile(operators)
        self.motionRegex = re.compile(
            "\\b({})\\b|\\B({})\\B".format(motions, specialMotion)
        )
        self.commandRegex = re.compile(
            "\\b({})\\b|\\B({})\\B".format(commands, specialMotion)
        )

        self.funcDict = {
            "a": self._a,
            "b": self._b,
            "d": self._d,
            "e": self._e,
            "ge": self._ge,
            "gg": self._gg,
            "h": self._h,
            "i": self._i,
            "j": self._j,
            "k": self._k,
            "l": self._l,
            "p": self._p,
            "u": self._u,
            "v": self._v,
            "w": self._w,
            "x": self._x,
            "y": self._y,
            "0": self._0,
            "$": self._dollar,
            "C-D": self._C_D,
            "C-R": self._C_R,
            "C-U": self._C_U,
        }

        self.operDict = {
            "d": self._d_op,
        }

    def enter(self):
        pass

    def exit(self):
        pass

    def reset(self):
        super().reset()
        self.moveMode = QTextCursor.MoveMode.MoveAnchor

    def process(self, e: QKeyEvent) -> bool:
        return super().process(e)

    def _a(self):
        self.changedState.emit(s.STATE.append)

    def _d(self):
        cursor = self.editor.textCursor()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.deleteChar()
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)

    def _i(self):
        self.changedState.emit(s.STATE.insert)

    def _u(self):
        self.editor.undo()

    def _v(self):
        self.changedState.emit(s.STATE.visual)
        
    def _C_R(self):
        self.editor.redo()

    def _d_op(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)
