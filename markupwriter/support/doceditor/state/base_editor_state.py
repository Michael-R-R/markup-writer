#!/usr/bin/python

import re

from enum import auto, Enum

from PyQt6.QtCore import (
    Qt,
    QObject,
    pyqtSignal,
)

from PyQt6.QtGui import (
    QKeyEvent,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
)


class STATE(Enum):
    normal = auto(),
    insert = auto(),
    append = auto(),
    visual = auto(),


class BaseEditorState(QObject):
    changedState = pyqtSignal(STATE)
    
    def __init__(self, editor: QPlainTextEdit, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.editor = editor
        
        self.buffer: str = ""
        
        self.operators: dict[str, function] = dict()
        self.commands: dict[str, function] = dict()
        
        self.countRegex = re.compile(r"[0-9]+")
        self.commandRegex = re.compile(r"h|j|k|l|dd")
        self.operatorRegex = re.compile(r"d|")
        
        self.nConvertDict: dict[Qt.Key, str] = {
            Qt.Key.Key_H: "h",
            Qt.Key.Key_J: "j",
            Qt.Key.Key_K: "k",
            Qt.Key.Key_L: "l",
            Qt.Key.Key_D: "d",
            Qt.Key.Key_0: "0",
            Qt.Key.Key_1: "1",
            Qt.Key.Key_2: "2",
            Qt.Key.Key_3: "3",
            Qt.Key.Key_4: "4",
            Qt.Key.Key_5: "5",
            Qt.Key.Key_6: "6",
            Qt.Key.Key_7: "7",
            Qt.Key.Key_8: "8",
            Qt.Key.Key_9: "9",
        }
        
        self.sConvertDict: dict[Qt.Key, str] = {
            Qt.Key.Key_F: "F",
        }
        
        self.cConvertDict: dict[Qt.Key, str] = {
            Qt.Key.Key_U: "C-U",
        }
        
    def enter(self):
        raise NotImplementedError()
    
    def exit(self):
        raise NotImplementedError()
    
    def process(self, e: QKeyEvent) -> bool:
        pass
    
    def reset(self):
        self.buffer: str = ""
        
    def hasCommand(self):
        found = self.commandRegex.search(self.buffer)
        return found is not None
    
    def evalCount(self) -> int:
        count = 1
        
        it = self.countRegex.finditer(self.buffer)
        for found in it:
            num = int(found.group(0))
            count *= num
            self.buffer = self.buffer[found.end():]
        
        return count
    
    def evalCommand(self) -> str:
        command = ""
        
        found = self.commandRegex.search(self.buffer)
        if found is None:
            return command
        
        command = found.group(0)
        self.buffer = self.buffer[found.end():]
        
        return command
    
    def evalOperator(self):
        operator = ""
        
        found = self.operatorRegex.search(self.buffer)
        if found is None:
            return operator
        
        operator = found.group(0)
        self.buffer = self.buffer[found.end():]
        
        return operator
