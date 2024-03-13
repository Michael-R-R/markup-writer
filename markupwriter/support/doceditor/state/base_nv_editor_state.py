#!/usr/bin/python

from __future__ import annotations

import re

from PyQt6.QtCore import (
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
    def __init__(self, state: BaseNvEditorState) -> None:
        self.state = state

    def enter(self, key: str):
        raise NotImplementedError()

    def process(self, key: str):
        raise NotImplementedError()


class InitBufferState(BaseBufferState):
    def __init__(self, state: BaseNvEditorState) -> None:
        super().__init__(state)

    def enter(self, key: str):
        self.state.reset()

    def process(self, key: str):
        # Count
        if self.state.countRegex.search(key) is not None:
            self.state.setBufferState(CountBufferState(self.state))
        # Leader
        elif self.state.leaderRegex.search(key) is not None:
            self.state.setBufferState(LeaderBufferState(self.state))
        # Operator
        elif self.state.operRegex.search(key) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Execute
        elif self.state.commandRegex.search(key) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))


class CountBufferState(BaseBufferState):
    def __init__(self, state: BaseNvEditorState) -> None:
        super().__init__(state)

    def enter(self, key: str):
        self.state.buffer += key

    def process(self, key: str):
        # Count
        if key.isnumeric():
            self.state.buffer += key
        # Leader
        elif self.state.leaderRegex.search(key) is not None:
            self.state.setBufferState(LeaderBufferState(self.state))
        # Operator
        elif self.state.operRegex.search(key) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Execute
        elif self.state.commandRegex.search(key) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))
        # Invalid
        else:
            self.state.setBufferState(InitBufferState(self.state))


class LeaderBufferState(BaseBufferState):
    def __init__(self, state: BaseNvEditorState) -> None:
        super().__init__(state)

    def enter(self, key: str):
        self.state.buffer += key

    def process(self, key: str):
        sequence = self.state.prevKey + key

        # Operator
        if self.state.operRegex.search(sequence) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Execute
        elif self.state.commandRegex.search(sequence) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))
        # Invalid
        else:
            self.state.setBufferState(InitBufferState(self.state))


class OperatorBufferState(BaseBufferState):
    def __init__(self, state: BaseNvEditorState) -> None:
        super().__init__(state)

    def enter(self, key: str):
        # Validate if has existing operator
        if self.state.operRegex.search(self.state.buffer) is not None:
            if key == "d":
                self.state.setBufferState(ExecuteBufferState(self.state))
            else:
                self.state.setBufferState(InitBufferState(self.state))
        # Validation passed
        else:
            self.state.buffer += key

    def process(self, key: str):
        # Count
        if self.state.countRegex.search(key) is not None:
            self.state.setBufferState(CountBufferState(self.state))
        # Leader
        elif self.state.leaderRegex.search(key) is not None:
            self.state.setBufferState(LeaderBufferState(self.state))
        # Operator
        elif self.state.operRegex.search(key) is not None:
            self.state.setBufferState(OperatorBufferState(self.state))
        # Execute
        elif self.state.motionRegex.search(key) is not None:
            self.state.setBufferState(ExecuteBufferState(self.state))
        # Invalid
        else:
            self.state.setBufferState(InitBufferState(self.state))


class ExecuteBufferState(BaseBufferState):
    def __init__(self, state: BaseNvEditorState) -> None:
        super().__init__(state)

    def enter(self, key: str):
        state = self.state
        buffer = state.buffer + key

        # --- Validate buffer --- #

        # Parse count
        count = 1
        it = state.countRegex.finditer(buffer)
        for found in it:
            num = int(found.group(0))
            count *= num
            buffer = buffer.replace(found.group(0), "", 1)
            
        # Parse operator
        operator = None
        found = state.operRegex.search(buffer)
        if found is not None:
            operator = found.group(0)
            buffer = buffer.replace(operator, "", 1)
            
        # Parse command
        cmd = None
        found = state.commandRegex.search(buffer)
        if found is not None:
            cmd = found.group(0)
            buffer = buffer.replace(cmd, "", 1)
            
        hasOp = operator is not None
        hasCmd = cmd is not None
        
        # Run cmd with operator
        if hasOp and hasCmd:
            state.moveMode = QTextCursor.MoveMode.KeepAnchor
            
            for _ in range(count):
                state.funcDict[cmd]()
                
            state.operDict[operator]()
        # Run cmd
        elif hasCmd:
            for _ in range(count):
                state.funcDict[cmd]()

        state.setBufferState(InitBufferState(state))

    def process(self, key: str):
        raise NotImplementedError()


class BaseNvEditorState(s.BaseEditorState):
    def __init__(
        self,
        moveMode: QTextCursor.MoveMode,
        editor: QPlainTextEdit,
        parent: QObject | None,
    ) -> None:
        super().__init__(editor, parent)

        self.prevKey = ""
        self.currKey = ""
        self.moveMode = moveMode
        self.bufferState: BaseBufferState = InitBufferState(self)

        self.countRegex = re.compile(r"[1-9][0-9]*")
        self.leaderRegex = re.compile(r"\bnone\b")
        self.operRegex = re.compile(r"\bnone\b")
        self.motionRegex = re.compile(r"\bnone\b")
        self.commandRegex = re.compile(r"\bnone\b")

        self.operDict: dict[str, function] = dict()

    def enter(self):
        raise NotImplementedError()

    def exit(self):
        raise NotImplementedError()

    def reset(self):
        self.buffer = ""
        self.prevKey = ""
        self.currKey = ""

    def process(self, e: QKeyEvent) -> bool:
        key = Key.get(e.modifiers(), e.key())
        if key is None:
            return True
        
        self.prevKey = self.currKey
        self.currKey = key
        self.bufferState.process(self.currKey)

        return True

    def setBufferState(self, state: BaseBufferState):
        self.bufferState = state
        self.bufferState.enter(self.currKey)

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

    def _p(self):
        self.editor.paste()
        self.changedState.emit(s.STATE.normal)

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

    def _y(self):
        self.editor.copy()
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        self.editor.setTextCursor(cursor)
        self.changedState.emit(s.STATE.normal)

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
