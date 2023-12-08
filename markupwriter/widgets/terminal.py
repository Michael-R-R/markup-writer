#!/usr/bin/python

from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget,
)

class Terminal(QTabWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)