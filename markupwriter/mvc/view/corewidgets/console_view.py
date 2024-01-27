#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent
)

from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QGridLayout,
)

from markupwriter.config import AppConfig


class ConsoleView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        self.tabwidget = QTabWidget(self)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.tabwidget, 0, 0)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.consoleSize = e.size()
        return super().resizeEvent(e)
