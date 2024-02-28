#!/usr/bin/python

import os

from PyQt6.QtCore import (
    Qt,
    QDataStream,
)

from PyQt6.QtGui import (
    QKeySequence,
)

from .base_config import BaseConfig


class HotkeyConfig(BaseConfig):
    INI_PATH: str = None
    openProject: QKeySequence = None
    saveDocument: QKeySequence = None
    saveProject: QKeySequence = None
    saveAsProject: QKeySequence = None
    closeProject: QKeySequence = None
    exitApplication: QKeySequence = None
    telescope: QKeySequence = None
    navUp: QKeySequence = None
    navDown: QKeySequence = None
    rename: QKeySequence = None

    def init(wd: str):
        HotkeyConfig.INI_PATH = os.path.join(wd, "resources/configs/hotkey.ini")
        HotkeyConfig.openProject = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_O)
        HotkeyConfig.saveDocument = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_S)
        HotkeyConfig.saveProject = QKeySequence(
            Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_S
        )
        HotkeyConfig.saveAsProject = QKeySequence(
            Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_A
        )
        HotkeyConfig.closeProject = QKeySequence(
            Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_O
        )
        HotkeyConfig.exitApplication = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Q)
        HotkeyConfig.telescope = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_P)
        HotkeyConfig.navUp = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Up)
        HotkeyConfig.navDown = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Down)
        HotkeyConfig.rename = QKeySequence(Qt.Key.Key_F2)

    def reset(wd: str):
        HotkeyConfig.init(wd)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HotkeyConfig.openProject
        sOut << HotkeyConfig.saveDocument
        sOut << HotkeyConfig.saveProject
        sOut << HotkeyConfig.saveAsProject
        sOut << HotkeyConfig.closeProject
        sOut << HotkeyConfig.exitApplication
        sOut << HotkeyConfig.telescope
        sOut << HotkeyConfig.navUp
        sOut << HotkeyConfig.navDown
        sOut << HotkeyConfig.rename
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HotkeyConfig.openProject
        sIn >> HotkeyConfig.saveDocument
        sIn >> HotkeyConfig.saveProject
        sIn >> HotkeyConfig.saveAsProject
        sIn >> HotkeyConfig.closeProject
        sIn >> HotkeyConfig.exitApplication
        sIn >> HotkeyConfig.telescope
        sIn >> HotkeyConfig.navUp
        sIn >> HotkeyConfig.navDown
        sIn >> HotkeyConfig.rename
        return sIn
