#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

class DocMainMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__("Document", parent)
        
        self.toggleSpell = QAction("Spell Check", self)
        self.toggleSpell.setCheckable(True)
        self.toggleSpell.setChecked(True)
        
        self.addAction(self.toggleSpell)
        self.addSeparator()
