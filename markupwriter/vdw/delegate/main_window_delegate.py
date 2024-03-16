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

from . import BaseDelegate

import markupwriter.vdw.view as v
import markupwriter.vdw.worker as w


class MainWindowDelegate(BaseDelegate):
    viewClosing = pyqtSignal()
    
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.view = v.MainWindowView(None)
        self.worker = w.MainWindowWorker(self.view, self)
        
        self.setupConnections()
        
    def setup(self):
        pass
        
    def setupConnections(self):
        self.view.closing.connect(lambda: self.viewClosing.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
