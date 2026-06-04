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
        mms = AppConfig.mainWindowSize
        dts = int(mms.width() * 0.05)
        des = int(mms.width() * 0.70)
        dps = int(mms.width() * 0.25)
        self.worker.setSizesLHS([dts, des])
        self.worker.setSizesRHS([des, dps])
        
    def setupConnections(self):
        pass
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
