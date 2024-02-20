#!/usr/bin/python

from PyQt6.QtCore import (
    QEvent,
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
)


class FilterLineEdit(QLineEdit):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.setWindowFlag(Qt.WindowType.Popup)
        self.setPlaceholderText("Filter items...")
        
    def leaveEvent(self, a0: QEvent | None) -> None:
        self.close()
        return super().leaveEvent(a0)
