#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

class PreviewPopupWidget(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(QLabel("I am a test", self))
