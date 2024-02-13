#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

from PyQt6.QtWidgets import (
    QWidget,
)

import markupwriter.mv.model as m
import markupwriter.mv.view as v


class CentralWidgetDelegate(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.model = m.CentralWidgetModel(self)
        self.view = v.CentralWidgetView(None)
        
    def insertWidgetLHS(self, i: int, widget: QWidget):
        self.view.lhSplitter.insertWidget(i, widget)
        
    def insertWidgetRHS(self, i: int, widget: QWidget):
        self.view.rhSplitter.insertWidget(i, widget)
        
    def addWidgetLHS(self, widget: QWidget):
        self.view.lhSplitter.addWidget(widget)
        
    def addWidgetRHS(self, widget: QWidget):
        self.view.rhSplitter.addWidget(widget)
        
    def setSizesLHS(self, sizes: list[int]):
        self.view.lhSplitter.setSizes(sizes)
        
    def setSizesRHS(self, sizes: list[int]):
        self.view.rhSplitter.setSizes(sizes)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.model
        sout << self.view
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.model
        sin >> self.view
        return sin
