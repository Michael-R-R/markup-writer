#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QSizePolicy,
)

class CentralWidgetView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.vLayout = QVBoxLayout(self)
        self.lhSplitter = QSplitter(Qt.Orientation.Horizontal)
        self.rhSplitter = QSplitter(Qt.Orientation.Horizontal)
        self.rvSplitter = QSplitter(Qt.Orientation.Vertical)

        self.lhSplitter.addWidget(self.rvSplitter)
        self.rvSplitter.addWidget(self.rhSplitter)
        self.vLayout.addWidget(self.lhSplitter)
