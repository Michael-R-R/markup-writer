#!/usr/bin/python

from __future__ import annotations

import re

from PyQt6.QtCore import (
    Qt,
    QObject,
)

from PyQt6.QtGui import (
    QKeyEvent,
    QTextCursor,
    QTextDocument,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
)

from markupwriter.common.provider import Key

import markupwriter.support.doceditor.state as s


class BaseBufferState(object):
    def __init__(self, state: NvEditorState) -> None:
        self.state = state

    def enter(self, ckey: str):
        raise NotImplementedError()

    def process(self, ckey: str):
        raise NotImplementedError()


class InitBufferState(BaseBufferState):
    def __init__(self, state: NvEditorState) -> None:
        super().__init__(state)

    def enter(self, ckey: str):
        self.state.reset()

    def process(self, ckey: str):
        # Count
        if self.state.countRegex.search(ckey) is not None:
            self.state.setBufferState(CountBufferState(self.state))
        # Prefix
        elif self.state.prefixRegex.search(ckey) is not None:
            self.state.setBufferState(PrefixBufferState(self.state))
        # Operator
        elif self.state.opRegex.search(ckey) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Execute
        elif self.state.commandRegex.search(ckey) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))


class CountBufferState(BaseBufferState):
    def __init__(self, state: NvEditorState) -> None:
        super().__init__(state)

    def enter(self, ckey: str):
        self.state.buffer += ckey

    def process(self, ckey: str):
        # Count
        if ckey.isnumeric():
            self.state.setBufferState(CountBufferState(self.state))
        # Prefix
        elif self.state.prefixRegex.search(ckey) is not None:
            self.state.setBufferState(PrefixBufferState(self.state))
        # Operator
        elif self.state.opRegex.search(ckey) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Execute
        elif self.state.commandRegex.search(ckey) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))
        # Invalid
        else:
            self.state.setBufferState(InitBufferState(self.state))


class PrefixBufferState(BaseBufferState):
    def __init__(self, state: NvEditorState) -> None:
        super().__init__(state)

    def enter(self, ckey: str):
        self.state.buffer += ckey

    def process(self, ckey: str):
        sequence = self.state.prevCKey + ckey

        # Operator
        if self.state.opRegex.search(sequence) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Command
        elif self.state.commandRegex.search(sequence) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))
        # Invalid
        else:
            self.state.setBufferState(InitBufferState(self.state))


class OperatorBufferState(BaseBufferState):
    def __init__(self, state: NvEditorState) -> None:
        super().__init__(state)

    def enter(self, ckey: str):
        # Validate if has existing operator
        if self.state.opRegex.search(self.state.buffer) is not None:
            if ckey == "d":
                self.state.setBufferState(ExecuteBufferState(self.state))
            else:
                self.state.setBufferState(InitBufferState(self.state))
        # Validation passed
        else:
            self.state.buffer += ckey

    def process(self, ckey: str):
        # Count
        if self.state.countRegex.search(ckey) is not None:
            self.state.setBufferState(CountBufferState(self.state))
        # Prefix
        elif self.state.prefixRegex.search(ckey) is not None:
            self.state.setBufferState(PrefixBufferState(self.state))
        # Operator
        elif self.state.opRegex.search(ckey) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Execute
        elif self.state.motionRegex.search(ckey) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))
        # Invalid
        else:
            self.state.setBufferState(InitBufferState(self.state))


class ExecuteBufferState(BaseBufferState):
    def __init__(self, state: NvEditorState) -> None:
        super().__init__(state)

    def enter(self, ckey: str):
        state = self.state
        state.buffer += ckey

        # --- Validate sequence --- #

        # Parse count
        count = 1
        it = state.countRegex.finditer(state.buffer)
        for found in it:
            num = int(found.group(0))
            count *= num
            state.buffer = state.buffer.replace(found.group(0), "", 1)
            
        # Parse operator
        operator = None
        found = state.opRegex.search(state.buffer)
        if found is not None:
            operator = found.group(0)
            state.buffer = state.buffer.replace(operator, "", 1)
            
        # Parse command
        cmd = None
        found = state.commandRegex.search(state.buffer)
        if found is not None:
            cmd = found.group(0)
            state.buffer = state.buffer.replace(cmd, "", 1)
            
        hasOp = operator is not None
        hasCmd = cmd is not None
        
        # Run cmd with operator
        if hasOp and hasCmd:
            state.moveMode = QTextCursor.MoveMode.KeepAnchor
            
            for _ in range(count):
                state.funcDict[cmd]()
                
            state.opDict[operator]()
        # Run cmd
        elif hasCmd:
            for _ in range(count):
                state.funcDict[cmd]()

        self.state.setBufferState(InitBufferState(self.state))

    def process(self, ckey: str):
        raise NotImplementedError()


class NvEditorState(s.BaseEditorState):
    def __init__(
        self,
        moveMode: QTextCursor.MoveMode,
        editor: QPlainTextEdit,
        parent: QObject | None,
    ) -> None:
        super().__init__(editor, parent)

        self.buffer = ""
        self.prevCKey = ""
        self.currCKey = ""
        self.moveMode = moveMode
        self.bufferState: BaseBufferState = InitBufferState(self)

        self.countRegex = re.compile(r"[1-9][0-9]*")
        self.prefixRegex = re.compile(r"\bnone\b")
        self.opRegex = re.compile(r"\bnone\b")
        self.motionRegex = re.compile(r"\bnone\b")
        self.commandRegex = re.compile(r"\bnone\b")

        self.opDict: dict[str, function] = dict()

    def enter(self):
        raise NotImplementedError()

    def exit(self):
        raise NotImplementedError()

    def reset(self):
        self.buffer = ""
        self.prevCKey = ""
        self.currCKey = ""

    def process(self, e: QKeyEvent) -> bool:
        # Ignore modifier keys
        isShift = Qt.Key.Key_Shift == e.key()
        isCtrl = Qt.Key.Key_Control == e.key()
        isAlt = Qt.Key.Key_Alt == e.key()
        if isShift or isCtrl or isAlt:
            return True
        
        key = Key.get(e.modifiers(), e.key())
        if key is None:
            return True
        
        self.prevCKey = self.currCKey
        self.currCKey = key
        self.bufferState.process(self.currCKey)
        print("IP:", self.buffer)

        return True

    def setBufferState(self, state: BaseBufferState):
        self.bufferState = state
        self.bufferState.enter(self.currCKey)

    def _b(self):
        doc = self.editor.document()
        cursor = self.editor.textCursor()
        flag = QTextDocument.FindFlag.FindBackward
        cursor.movePosition(QTextCursor.MoveOperation.Left, self.moveMode)

        newCursor = doc.find(" ", cursor.position(), flag)
        newCursor.movePosition(QTextCursor.MoveOperation.Right)
        cursor.setPosition(newCursor.position(), self.moveMode)

        self.editor.setTextCursor(cursor)

    def _e(self):
        doc = self.editor.document()
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Right, self.moveMode)

        newCursor = doc.find(" ", cursor.position())
        newCursor.movePosition(QTextCursor.MoveOperation.Left)
        cursor.setPosition(newCursor.position(), self.moveMode)

        self.editor.setTextCursor(cursor)

    def _ge(self):
        doc = self.editor.document()
        cursor = self.editor.textCursor()
        flag = QTextDocument.FindFlag.FindBackward

        newCursor = doc.find(" ", cursor.position(), flag)
        newCursor.movePosition(QTextCursor.MoveOperation.Left)
        cursor.setPosition(newCursor.position(), self.moveMode)

        self.editor.setTextCursor(cursor)

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

    def _w(self):
        doc = self.editor.document()
        cursor = self.editor.textCursor()

        newCursor = doc.find(" ", cursor.position())
        newCursor.movePosition(QTextCursor.MoveOperation.Right)
        cursor.setPosition(newCursor.position(), self.moveMode)

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

    def _C_D(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Down, self.moveMode, 25)
        self.editor.setTextCursor(cursor)

    def _C_U(self):
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Up, self.moveMode, 25)
        self.editor.setTextCursor(cursor)
