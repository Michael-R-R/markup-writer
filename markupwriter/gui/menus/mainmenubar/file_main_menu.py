#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.config import (
    AppConfig,
    HotkeyConfig,
)


class FileMainMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__("File", parent)

        self.openedRecentlyActionList = []

        self.newProjAction = QAction("New Project...", self)
        self.openProjAction = QAction("Open Project", self)
        self.openRecentMenu = QMenu("Open Recent...", self)
        self.saveDocAction = QAction("Save Document", self)
        self.saveProjAction = QAction("Save Project", self)
        self.saveProjAsAction = QAction("Save Project As...", self)
        self.importTxtAction = QAction("Text", self)
        self.exportAction = QAction("Export...", self)
        self.closeProjAction = QAction("Close Project", self)
        self.exitAction = QAction("Exit", self)
        
        self.importMenu = QMenu("Import...", self)
        self.importMenu.addAction(self.importTxtAction)

        self.addAction(self.newProjAction)
        self.addSeparator()
        self.addAction(self.openProjAction)
        self.addMenu(self.openRecentMenu)
        self.addSeparator()
        self.addAction(self.saveDocAction)
        self.addSeparator()
        self.addAction(self.saveProjAction)
        self.addAction(self.saveProjAsAction)
        self.addSeparator()
        self.addMenu(self.importMenu)
        self.addAction(self.exportAction)
        self.addSeparator()
        self.addAction(self.closeProjAction)
        self.addSeparator()
        self.addAction(self.exitAction)

        self.openProjAction.setShortcut(HotkeyConfig.openProject)
        self.saveDocAction.setShortcut(HotkeyConfig.saveDocument)
        self.saveProjAction.setShortcut(HotkeyConfig.saveProject)
        self.saveProjAsAction.setShortcut(HotkeyConfig.saveAsProject)
        self.closeProjAction.setShortcut(HotkeyConfig.closeProject)
        self.exitAction.setShortcut(HotkeyConfig.exitApplication)
        
        self.openRecentMenu.setEnabled(len(AppConfig.openedRecently) > 0)
        self.saveDocAction.setEnabled(False)
        self.saveProjAction.setEnabled(False)
        self.saveProjAsAction.setEnabled(False)
        self.importMenu.setEnabled(False)
        self.exportAction.setEnabled(False)
        self.closeProjAction.setEnabled(False)

        for path in AppConfig.openedRecently:
            action = QAction(path, self)
            self.openedRecentlyActionList.append(action)
            self.openRecentMenu.addAction(action)
