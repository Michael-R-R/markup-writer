#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QMainWindow,
)

from markupwriter.config import AppConfig
from markupwriter.widgets import MainMenuBar
from .central_widget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.mainWindowSize)
        self.setMenuBar(MainMenuBar(self))
        self.setCentralWidget(CentralWidget(self))
        self.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = a0.size()
        return super().resizeEvent(a0)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn
        