#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

import markupwriter.controller.core as core


class MainWindow(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.menuBarController = core.MainMenuBarController(self)
        self.centralController = core.CentralWidgetController(self)
        self.statusBarController = core.MainStatusBarController(self)
