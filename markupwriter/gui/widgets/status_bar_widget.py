#!/usr/bin/python

from PyQt6.QtCore import (
    Qt, 
)

from PyQt6.QtWidgets import (
    QStatusBar,
    QWidget,
    QLabel,
)

class StatusBarWidget(QStatusBar):
    def __init__(self, normMsg: str, permMsg: str, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.normLabel = QLabel(normMsg, self)
        self.permLabel = QLabel(permMsg, self)

        self.permLabel.setStyleSheet("background-color: transparent;")

        self.addWidget(self.normLabel)
        self.addPermanentWidget(self.permLabel)
        self.setSizeGripEnabled(False)
