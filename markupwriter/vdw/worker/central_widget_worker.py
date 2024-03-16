#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from PyQt6.QtWidgets import (
    QWidget,
)

import markupwriter.vdw.view as v


class CentralWidgetWorker(QObject):
    def __init__(self, cwv: v.CentralWidgetView, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.cwv = cwv

    def insertWidgetLHS(self, i: int, widget: QWidget):
        self.cwv.lhSplitter.insertWidget(i, widget)
        
    def insertWidgetRHS(self, i: int, widget: QWidget):
        self.cwv.rhSplitter.insertWidget(i, widget)
        
    def addWidgetLHS(self, widget: QWidget):
        self.cwv.lhSplitter.addWidget(widget)
        
    def addWidgetRHS(self, widget: QWidget):
        self.cwv.rhSplitter.addWidget(widget)
        
    def setSizesLHS(self, sizes: list[int]):
        self.cwv.lhSplitter.setSizes(sizes)
        
    def setSizesRHS(self, sizes: list[int]):
        self.cwv.rhSplitter.setSizes(sizes)
