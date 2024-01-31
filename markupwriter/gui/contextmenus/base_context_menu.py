#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QPoint,
)

from PyQt6.QtWidgets import (
    QWidget,
    QMenu,
)


class BaseContextMenu(QObject):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self._menu = QMenu(parent)

    def preprocess(self, args: list[object] | None):
        raise NotImplementedError()

    def postprocess(self, args: list[object] | None):
        raise NotImplementedError()

    def onShowMenu(self, pos: QPoint, args: list[object] | None = None):
        self.preprocess(args)
        self._menu.exec(pos)
        self.postprocess(args)
