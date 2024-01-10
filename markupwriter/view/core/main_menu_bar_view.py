#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenuBar,
    QWidget,
)

class MainMenuBarView(QMenuBar):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
