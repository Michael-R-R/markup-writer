#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

from . import BaseDelegate

import markupwriter.vdw.view as v
import markupwriter.vdw.worker as w


class DocumentPreviewDelegate(BaseDelegate):
    showViewRequested = pyqtSignal()
    closeTabRequested = pyqtSignal(int)
    tabCountChanged = pyqtSignal(int)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.DocumentPreviewView(None)
        self.worker = w.DocumentPreviewWorker(self.view, self)
        
        self.setupConnections()
        
    def setup(self):
        pass

    def setupConnections(self):
        tw = self.view.tabWidget
        tw.tabCloseRequested.connect(lambda x: self.closeTabRequested.emit(x))
        tw.countChanged.connect(lambda x: self.tabCountChanged.emit(x))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
