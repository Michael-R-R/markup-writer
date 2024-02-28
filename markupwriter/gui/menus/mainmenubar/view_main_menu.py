#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from markupwriter.config import HotkeyConfig


class ViewMainMenu(QMenu):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__("View", parent)
        
        self.telecopeAction = QAction("Telescope", self)
        self.telecopeAction.setShortcut(HotkeyConfig.telescope)
        
        self.addAction(self.telecopeAction)
