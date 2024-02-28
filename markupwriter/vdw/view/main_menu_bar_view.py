#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QMenuBar,
    QWidget,
)

from markupwriter.gui.menus.mainmenubar import (
    FileMainMenu,
    DocMainMenu,
    ViewMainMenu,
)

class MainMenuBarView(QMenuBar):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.fileMenu = FileMainMenu(self)
        self.docMenu = DocMainMenu(self)
        self.viewMenu = ViewMainMenu(self)
        
        self.addMenu(self.fileMenu)
        self.addMenu(self.docMenu)
        self.addMenu(self.viewMenu)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
