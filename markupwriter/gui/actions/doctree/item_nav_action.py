#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.common.config import (
    HotkeyConfig,
)

from markupwriter.common.provider import (
    Icon,
)

class ItemNavUpAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(Icon.UP_ARROW, "Move up", parent)
        hotkey = HotkeyConfig.navUp
        text = hotkey.toString()
        self.setShortcut(hotkey)
        self.setToolTip("Move up ({})".format(text))

class ItemNavDownAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(Icon.DOWN_ARROW, "Move down", parent)
        hotkey = HotkeyConfig.navDown
        text = hotkey.toString()
        self.setShortcut(hotkey)
        self.setToolTip("Move down ({})".format(text))