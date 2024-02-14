#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.vdw.view as v


class DocumentPreviewDelegate(QObject):
    closeTabRequested = pyqtSignal(int)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.DocumentPreviewView(None)

    def _setupViewConnections(self):
        tw = self.view.tabWidget
        tw.tabCloseRequested.connect(lambda x: self.closeTabRequested.emit(x))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
