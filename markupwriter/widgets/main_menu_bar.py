#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenuBar,
    QWidget,
)

class MainMenuBar(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)