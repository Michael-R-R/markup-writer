#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.mv.model as m
import markupwriter.mv.view as v


class DocumentPreviewDelegate(QObject):
    closeTabRequested = pyqtSignal(int)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = m.DocumentPreviewModel(self)
        self.view = v.DocumentPreviewView(None)

    def _setupViewConnections(self):
        tw = self.view.tabWidget
        tw.tabCloseRequested.connect(lambda x: self.closeTabRequested.emit(x))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.model
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.model
        sin >> self.view
        return sin
