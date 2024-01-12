#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)


class DocumentEditorBar(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.pathLabel = QLabel("", self)

        self.hLayout = QHBoxLayout(self)
        self.hLayout.addStretch()
        self.hLayout.addWidget(self.pathLabel)
        self.hLayout.addStretch()
