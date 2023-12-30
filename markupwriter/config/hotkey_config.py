#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
)

from PyQt6.QtGui import (
    QKeySequence,
)

class HotkeyConfig(object):
    INI_PATH = "./resources/configs/hotkey.ini"
    navUp = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Up)
    navDown = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Down)
    newItem = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_N)

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