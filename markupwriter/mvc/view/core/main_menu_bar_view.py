#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenuBar,
    QWidget,
)

from markupwriter.gui.menus.mainmenubar import (
    FileMainMenu,
)


class MainMenuBarView(QMenuBar):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.filemenu = FileMainMenu(self)
        
        self.addMenu(self.filemenu)
