#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QMainWindow,
)

from markupwriter.config import AppConfig

from .central_widget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.mainWindowSize)
        self.setContentsMargins(0, 0, 0, 0)

        self._centralWidget = CentralWidget(self)

        self.setMenuBar(self._centralWidget.mainMenuBar)
        self.setCentralWidget(self._centralWidget)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = a0.size()
        return super().resizeEvent(a0)
        