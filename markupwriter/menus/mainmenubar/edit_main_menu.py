#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from PyQt6.QtGui import (
    QAction,
)

class EditMainMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__("Edit", parent)