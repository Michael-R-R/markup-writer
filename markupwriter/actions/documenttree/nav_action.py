#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QObject,
)

from PyQt6.QtGui import (
    QAction,
    QKeySequence,
)

from markupwriter.config import (
    HotkeyConfig,
)

from markupwriter.support.iconprovider import (
    Icon,
)

class NavUpAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(Icon.UP_ARROW, "Move up", parent)
        key = HotkeyConfig.navUp
        text = key.toString()
        self.setShortcut(key)
        self.setToolTip("Move up ({})".format(text))

class NavDownAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(Icon.DOWN_ARROW, "Move down", parent)
        key = HotkeyConfig.navDown
        text = key.toString()
        self.setShortcut(key)
        self.setToolTip("Move down ({})".format(text))