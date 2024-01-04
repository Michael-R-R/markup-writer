#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
)

from PyQt6.QtGui import (
    QKeySequence,
)

from markupwriter.util import File
from .base_config import BaseConfig

class HotkeyConfig(BaseConfig):
    INI_PATH: str = None
    navUp: QKeySequence = None
    navDown: QKeySequence  = None
    newItem: QKeySequence  = None

    def init():
        HotkeyConfig.INI_PATH = File.path("./resources/configs/hotkey.ini")
        HotkeyConfig.navUp = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Up)
        HotkeyConfig.navDown = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Down)
        HotkeyConfig.newItem = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_N)

    def reset():
        HotkeyConfig.init()

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HotkeyConfig.navUp
        sOut << HotkeyConfig.navDown
        sOut << HotkeyConfig.newItem
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HotkeyConfig.navUp
        sIn >> HotkeyConfig.navDown
        sIn >> HotkeyConfig.newItem
        return sIn