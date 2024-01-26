#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
)


class DocumentEditorBarWidget(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.pathLabel = QLabel("", self)
        
        self.mLayout = QGridLayout(self)
        self.mLayout.addWidget(self.pathLabel, 0, 1, Qt.AlignmentFlag.AlignHCenter)
        
        self.mLayout.setColumnStretch(0, 0)
        self.mLayout.setColumnStretch(2, 0)
        
    def reset(self):
        self.pathLabel.clear()
        
    def addPath(self, path: str):
        self.pathLabel.setText(path)
