#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from markupwriter.config import HotkeyConfig


class DocMainMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__("Document", parent)

        self.toggleSpell = QAction("Spell Check", self)
        self.toggleSpell.setCheckable(True)
        self.toggleSpell.setChecked(True)

        self.refreshPreview = QAction("Refresh Preview", self)
        self.refreshPreview.setShortcut(HotkeyConfig.refreshPreview)
        
        self.togglePreview = QAction("Toggle Preview", self)
        self.togglePreview.setShortcut(HotkeyConfig.togglePreview)

        self.addAction(self.toggleSpell)
        self.addSeparator()
        self.addAction(self.refreshPreview)
        self.addAction(self.togglePreview)
        self.addSeparator()
