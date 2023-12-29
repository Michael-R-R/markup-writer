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

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HotkeyConfig.navUp
        sOut << HotkeyConfig.navDown
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HotkeyConfig.navUp
        sIn >> HotkeyConfig.navDown
        return sIn