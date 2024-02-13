#!/usr/bin/python

from PyQt6.QtCore import QObject

import markupwriter.mv.delegate as d


class Core(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.mwd = d.MainWindowDelegate(self)
        self.mmbd = d.MainMenuBarDelegate(self)
        self.cwd = d.CentralWidgetDelegate(self)
        self.dtd = d.DocumentTreeDelegate(self)
        self.ded = d.DocumentEditorDelegate(self)
        self.dpd = d.DocumentPreviewDelegate(self)
        
        self._setup()
        
    def run(self):
        self.mwd.showMainView()
        
    def _setup(self):
        self.mwd.setMenuBar(self.mmbd.view)
        self.mwd.setCentralWidget(self.cwd.view)
        
        self.cwd.insertWidgetLHS(0, self.dtd.view)
        self.cwd.insertWidgetRHS(0, self.ded.view)
        self.cwd.addWidgetRHS(self.dpd.view)
