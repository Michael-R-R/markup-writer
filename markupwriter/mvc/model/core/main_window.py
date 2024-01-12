#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
)

import markupwriter.mvc.controller.core as core


class MainWindow(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.menuBarController = core.MainMenuBarController(self)
        self.centralController = core.CentralWidgetController(self)
        self.statusBarController = core.MainStatusBarController(self)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.centralController
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.centralController
        return sin
