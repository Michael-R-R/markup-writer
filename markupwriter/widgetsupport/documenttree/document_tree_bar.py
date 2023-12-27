#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)

class DocumentTreeBar(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        hLayout = QHBoxLayout(self)
        hLayout.addWidget(QLabel("<b>Project Content<b>", self))