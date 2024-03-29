#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
)

from PyQt6.QtWidgets import (
    QWidget,
    QSplitter,
    QGridLayout,
    QSizePolicy,
)


class CentralWidgetView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.lhSplitter = QSplitter(Qt.Orientation.Horizontal)
        self.rhSplitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.lhSplitter.addWidget(self.rhSplitter)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.lhSplitter, 0, 0)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
        