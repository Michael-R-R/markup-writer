#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)


class Key(object):
    _normDict: dict[Qt.Key, str] = {
        Qt.Key.Key_A: "a",
        Qt.Key.Key_D: "d",
        Qt.Key.Key_G: "g",
        Qt.Key.Key_H: "h",
        Qt.Key.Key_I: "i",
        Qt.Key.Key_J: "j",
        Qt.Key.Key_K: "k",
        Qt.Key.Key_L: "l",
        Qt.Key.Key_U: "u",
        Qt.Key.Key_V: "v",
        Qt.Key.Key_W: "w",
        Qt.Key.Key_X: "x",
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
        Qt.Key.Key_Escape: "esc",
    }

    _shiftDict: dict[Qt.Key, str] = {
        Qt.Key.Key_F: "F",
        Qt.Key.Key_U: "U",
        Qt.Key.Key_ParenLeft: "(",
        Qt.Key.Key_Dollar: "$",
    }

    _ctrlDict: dict[Qt.Key, str] = {
        Qt.Key.Key_U: "C-U",
    }
    
    def get(mod: Qt.KeyboardModifier, key: Qt.Key) -> str | None:
        ckey = None

        match mod:
            case Qt.KeyboardModifier.NoModifier:
                if key in Key._normDict:
                    ckey = Key._normDict[key]
            case Qt.KeyboardModifier.ShiftModifier:
                if key in Key._shiftDict:
                    ckey = Key._shiftDict[key]
            case Qt.KeyboardModifier.ControlModifier:
                if key in Key._ctrlDict:
                    ckey = Key._ctrlDict[key]

        return ckey

        