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

        self.newProjAction = QAction("New", self)
        self.openProjAction = QAction("Open", self)
        self.saveProjAction = QAction("Save", self)
        self.saveAsProjAction = QAction("Save as", self)

        self.addAction(self.newProjAction)
        self.addSeparator()
        self.addAction(self.openProjAction)
        self.addAction(self.saveProjAction)
        self.addAction(self.saveAsProjAction)