#!/usr/bin/python

from PyQt6.QtCore import (
    QPoint,
)

from PyQt6.QtWidgets import (
    QMenu,
)

class BaseContextMenu(object):
    def __init__(self) -> None:
        self._menu = QMenu()

    def onShowMenu(self, pos: QPoint):
        self._menu.exec(pos)
