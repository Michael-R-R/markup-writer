#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSignal,
    QDataStream,
    QSize,
)

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)

import markupwriter.gui.widgets as w


class DocumentTreeView(QWidget):
    resized = pyqtSignal(QSize)
    
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.treeBar = w.DocumentTreeBarWidget(self)
        self.treeWidget = w.DocumentTreeWidget(self)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.treeBar, 0, 0)
        self.gLayout.addWidget(self.treeWidget, 1, 0)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        self.resized.emit(e.size())
        return super().resizeEvent(e)
    
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.treeWidget
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.treeWidget
        return sin
