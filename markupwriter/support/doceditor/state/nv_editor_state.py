#!/usr/bin/python

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


class NvEditorState(s.BaseEditorState):
    def __init__(
        self,
        moveMode: QTextCursor.MoveMode,
        editor: QPlainTextEdit,
        parent: QObject | None,
    ) -> None:
        super().__init__(editor, parent)

        self.buffer = ""
        self.hasPrefix = False
        self.hasOp = False
        self.moveMode = moveMode
        
        self.countRegex = re.compile(r"[1-9]+")
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
        self.hasPrefix = False
        self.hasOp = False
    
    def process(self, e: QKeyEvent) -> bool:
        if e.key() == Qt.Key.Key_Escape:
            if self.buffer != "":
                self.reset()
                return True

        if self.build(e):
            self.evaluate()
            self.reset()

        return True
        
    def build(self, e: QKeyEvent):
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
    