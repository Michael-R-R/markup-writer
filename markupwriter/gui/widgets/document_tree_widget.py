#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
    pyqtSignal,
    QDataStream,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)

import markupwriter.support.doctree as dt
import markupwriter.support.doctree.item as ti


class DocumentTreeWidget(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.baseTree = dt.CustomTreeWidget(self)
        self.filterTree = None
        self.currentTree = self.baseTree
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.currentTree)
        
    def filterItems(self, text: str):
        if text == "":
            self.gLayout.removeWidget(self.currentTree)
            self.currentTree = self.baseTree
            self.filterTree = None
            self.gLayout.addWidget(self.currentTree)
            return
        
        regex = re.compile(text)
        self.filterTree = dt.CustomTreeWidget(self)
        for i in range(self.baseTree.topLevelItemCount()):
            item = self.baseTree.topLevelItem(i)
            w: ti.BaseTreeItem = self.baseTree.itemWidget(item, 0)
            found = regex.search(w.title())
            if found is not None:
                self.filterTree.add(w.deepcopy())
                
        self.gLayout.removeWidget(self.currentTree)
        self.currentTree = self.filterTree
        self.gLayout.addWidget(self.currentTree)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.baseTree
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.baseTree
        return sin
