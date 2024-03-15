#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

from PyQt6.QtWidgets import (
    QWidget,
    QMenuBar,
)

import markupwriter.vdw.view as v
import markupwriter.vdw.worker as w


class MainWindowDelegate(QObject):
    viewClosing = pyqtSignal()
    
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.view = v.MainWindowView(None)
        self.worker = w.MainWindowWorker(self.view, self)
        
        self._setupViewConnections()
        
    def showMainView(self):
        self.view.show()
        
    def setWindowTitle(self, title: str | None):
        self.view.setWindowTitle(title)
        
    def setMenuBar(self, menuBar: QMenuBar):
        self.view.setMenuBar(menuBar)
        
    def setCentralWidget(self, widget: QWidget):
        self.view.setCentralWidget(widget)
        
    def _setupViewConnections(self):
        self.view.closing.connect(lambda: self.viewClosing.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
