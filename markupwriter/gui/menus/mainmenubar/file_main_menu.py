#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.config import (
    HotkeyConfig,
)


class FileMainMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__("File", parent)

        self.newProjectAction = QAction("New Project...", self)
        self.openProjectAction = QAction("Open Project...", self)
        self.saveDocumentAction = QAction("Save Document", self)
        self.saveProjectAction = QAction("Save Project", self)
        self.saveProjectAsAction = QAction("Save Project As...", self)
        self.closeProjectAction = QAction("Close Project", self)
        self.exitAction = QAction("Exit", self)

        self.addAction(self.newProjectAction)
        self.addSeparator()
        self.addAction(self.openProjectAction)
        self.addSeparator()
        self.addAction(self.saveDocumentAction)
        self.addSeparator()
        self.addAction(self.saveProjectAction)
        self.addAction(self.saveProjectAsAction)
        self.addSeparator()
        self.addAction(self.closeProjectAction)
        self.addSeparator()
        self.addAction(self.exitAction)

        self.openProjectAction.setShortcut(HotkeyConfig.openProject)
        self.saveDocumentAction.setShortcut(HotkeyConfig.saveDocument)
        self.saveProjectAction.setShortcut(HotkeyConfig.saveProject)
        self.saveProjectAsAction.setShortcut(HotkeyConfig.saveAsProject)
        self.closeProjectAction.setShortcut(HotkeyConfig.closeProject)
        self.exitAction.setShortcut(HotkeyConfig.exitApplication)
