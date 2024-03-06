#!/usr/bin/python

from enum import auto, Enum

from PyQt6.QtCore import (
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

    def enter(self):
        raise NotImplementedError()

    def exit(self):
        raise NotImplementedError()

    def process(self, e: QKeyEvent) -> bool:
        raise NotImplementedError()
