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

    def preprocess(self, args: list[object] | None):
        raise NotImplementedError()
    
    def postprocess(self, args: list[object] | None):
        raise NotImplementedError()

    def onShowMenu(self,
                   pos: QPoint,
                   args: list[object] | None = None):
        self.preprocess(args)
        self._menu.exec(pos)
        self.postprocess(args)
