#!/usr/bin/python

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
)

from markupwriter.config import AppConfig


class MainWindowView(QMainWindow):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.resize(AppConfig.mainWindowSize)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = e.size()
        return super().resizeEvent(e)
