#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
)

from PyQt6.QtWidgets import (
    QWidget,
)

from . import BaseDelegate

from markupwriter.config import AppConfig

import markupwriter.vdw.view as v
import markupwriter.vdw.worker as w


class CentralWidgetDelegate(BaseDelegate):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.view = v.CentralWidgetView(None)
        self.worker = w.CentralWidgetWorker(self.view, self)
        
        self.setupConnections()
        
    def setup(self):
        dts = AppConfig.docTreeSize
        des = AppConfig.docEditorSize
        dps = AppConfig.docPreviewSize
        self.worker.setSizesLHS([dts.width(), des.width() + dps.width()])
        self.worker.setSizesRHS([des.width(), dps.width()])
        
    def setupConnections(self):
        pass
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
