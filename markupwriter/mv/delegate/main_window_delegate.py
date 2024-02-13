#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
    QSize,
)

from PyQt6.QtWidgets import (
    QWidget,
    QMenuBar,
)

from markupwriter.common.provider import Style

import markupwriter.mv.model as m
import markupwriter.mv.view as v


class MainWindowDelegate(QObject):
    viewClosing = pyqtSignal()
    viewResized = pyqtSignal(QSize)
    
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        self.model = m.MainWindowModel(self)
        self.view = v.MainWindowView(None)
        
        self.view.closing.connect(lambda: self.viewClosing.emit())
        self.view.resized.connect(lambda x: self.viewResized.emit(x))
        
    def showMainView(self):
        self.view.setStyleSheet(Style.MAIN_WINDOW)
        self.view.show()
        
    def setMenuBar(self, menuBar: QMenuBar):
        self.view.setMenuBar(menuBar)
        
    def setCentralWidget(self, widget: QWidget):
        self.view.setCentralWidget(widget)
        
    def setViewTitle(self, title: str | None):
        self.view.setWindowTitle(title)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.model
        sout << self.view
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.model
        sin >> self.view
        return sin
