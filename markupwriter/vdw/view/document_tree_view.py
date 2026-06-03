#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QFrame,
)

from markupwriter.config import AppConfig
from markupwriter.common.provider import Style

import markupwriter.gui.widgets as w


class DocumentTreeView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.treeBar = w.DocumentTreeBarWidget(self)
        self.treeWidget = w.DocumentTreeWidget(self)

        self.borderFrame = QFrame(self)
        self.borderFrame.setFrameShape(QFrame.Shape.Box)
        self.borderFrame.setFrameShadow(QFrame.Shadow.Plain)
        
        self.gLayout = QGridLayout(self.borderFrame)
        self.gLayout.addWidget(self.treeBar, 0, 0)
        self.gLayout.addWidget(self.treeWidget, 1, 0)
        
        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.borderFrame, 0, 0)
        
        self.setStyleSheet(Style.TREE_VIEW)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeSize = e.size()
        
        return super().resizeEvent(e)
    
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.treeWidget
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.treeWidget
        return sin
