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

    def preprocess(self):
        raise NotImplementedError()
    
    def postprocess(self):
        actions = self._menu.actions()
        for a in actions:
            a.setDisabled(False)

    def onShowMenu(self, pos: QPoint):
        self.preprocess()
        self._menu.exec(pos)
        self.postprocess()
