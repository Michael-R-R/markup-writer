#!/usr/bin/python

from PyQt6.QtCore import QObject

import markupwriter.mv.delegate as d


class Core(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.mwd = d.MainWindowDelegate(self)
        self.cwd = d.CentralWidgetDelegate(self)
        
    def run(self):
        self.mwd.showMainView()
        
    def _setup(self):
        self.mwd.setCentralWidget(self.cwd.view)