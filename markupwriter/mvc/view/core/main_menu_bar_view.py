#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenuBar,
    QWidget,
)

from markupwriter.gui.menus.mainmenubar import (
    FileMainMenu,
    EditMainMenu,
)


class MainMenuBarView(QMenuBar):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.filemenu = FileMainMenu(self)
        self.editmenu = EditMainMenu(self)
        
        self.addMenu(self.filemenu)
        self.addMenu(self.editmenu)
