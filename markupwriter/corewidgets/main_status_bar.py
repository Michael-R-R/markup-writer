#!/usr/bin/python

from PyQt6.QtWidgets import (
    QStatusBar,
    QWidget,
)


class MainStatusBar(QStatusBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
