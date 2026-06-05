#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QResizeEvent
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QFrame,
)

from markupwriter.config import AppConfig
from markupwriter.common.provider import Style

import markupwriter.gui.widgets as w


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.tabWidget = w.PreviewTabWidget(self)
        
        self.borderFrame = QFrame(self)
        self.borderFrame.setObjectName("borderFrame")
        self.borderFrame.setFrameShape(QFrame.Shape.Box)
        self.borderFrame.setFrameShadow(QFrame.Shadow.Plain)

        self.gLayout = QGridLayout(self.borderFrame)
        self.gLayout.addWidget(self.tabWidget, 0, 0)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.borderFrame, 0, 0)
        
        self.setStyleSheet(Style.PREVIEW_VIEW)
    
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        
        return super().resizeEvent(e)
    
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.tabWidget
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.tabWidget
        return sin
