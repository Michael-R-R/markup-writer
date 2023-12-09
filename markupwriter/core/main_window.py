#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QMainWindow,
)

from markupwriter.config.config_app import (
    Config
)

from markupwriter.widgets.main_menu_bar import MainMenuBar;
from .central_widget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle(Config.APP_NAME)
        self.setMenuBar(MainMenuBar(self))
        self.setCentralWidget(CentralWidget(self))

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn
        