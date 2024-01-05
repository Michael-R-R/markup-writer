#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from PyQt6.QtGui import (
    QAction,
)

class FileMainMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__("File", parent)

        self.newAction = QAction("New", self)
        self.openAction = QAction("Open", self)
        self.saveAction = QAction("Save", self)
        self.saveAsAction = QAction("Save as", self)

        self.addAction(self.newAction)
        self.addSeparator()
        self.addAction(self.openAction)
        self.addAction(self.saveAction)
        self.addAction(self.saveAsAction)