#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent
)

from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
)

from markupwriter.config import AppConfig


class ConsoleView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        tabwidget = QTabWidget(self)
        self.tabwidget = tabwidget
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.tabwidget)
        self.vLayout = vLayout

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.consoleSize = e.size()
        return super().resizeEvent(e)
