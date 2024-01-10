#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
)


class ConsoleView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        
        tabwidget = QTabWidget(self)
        self.tabwidget = tabwidget
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.tabwidget)
        self.vLayout = vLayout

