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

        self.funcDict: dict[str, function] = dict()

        self.nConvertDict: dict[Qt.Key, str] = {
            Qt.Key.Key_H: "h",
            Qt.Key.Key_J: "j",
            Qt.Key.Key_K: "k",
            Qt.Key.Key_L: "l",
            Qt.Key.Key_D: "d",
            Qt.Key.Key_U: "u",
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
        raise NotImplementedError()

    def fetchKey(self, mod: Qt.KeyboardModifier, key: Qt.Key) -> str:
        ckey = ""

        match mod:
            case Qt.KeyboardModifier.NoModifier:
                if key in self.nConvertDict:
                    ckey = self.nConvertDict[key]
            case Qt.KeyboardModifier.ShiftModifier:
                if key in self.sConvertDict:
                    ckey = self.sConvertDict[key]
            case Qt.KeyboardModifier.ControlModifier:
                if key in self.cConvertDict:
                    ckey = self.cConvertDict[key]

        return ckey
