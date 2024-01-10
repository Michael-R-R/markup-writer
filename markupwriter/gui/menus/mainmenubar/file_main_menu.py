#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.common.config import (
    HotkeyConfig,
)


class FileMainMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__("File", parent)

        self.newAction = QAction("New...", self)
        self.openAction = QAction("Open...", self)
        self.saveAction = QAction("Save", self)
        self.saveAsAction = QAction("Save As...", self)
        self.closeAction = QAction("Close Project", self)
        self.exitAction = QAction("Exit", self)

        self.addAction(self.newAction)
        self.addSeparator()
        self.addAction(self.openAction)
        self.addSeparator()
        self.addAction(self.saveAction)
        self.addAction(self.saveAsAction)
        self.addSeparator()
        self.addAction(self.closeAction)
        self.addSeparator()
        self.addAction(self.exitAction)
        
        self.openAction.setShortcut(HotkeyConfig.openProject)
        self.saveAction.setShortcut(HotkeyConfig.saveProject)
        self.saveAsAction.setShortcut(HotkeyConfig.saveAsProject)
        self.closeAction.setShortcut(HotkeyConfig.closeProject)
        self.exitAction.setShortcut(HotkeyConfig.exitApplication)
