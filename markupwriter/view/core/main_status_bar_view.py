#!/usr/bin/python

from PyQt6.QtWidgets import (
    QStatusBar,
    QWidget,
)

class MainStatusBarView(QStatusBar):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
