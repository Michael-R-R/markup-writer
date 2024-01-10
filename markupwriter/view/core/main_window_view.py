#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
)

class MainWindowView(QMainWindow):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
