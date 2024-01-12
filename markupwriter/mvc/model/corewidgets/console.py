#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)


class Console(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
