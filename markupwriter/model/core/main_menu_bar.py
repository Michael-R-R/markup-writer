#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.gui.menus.mainmenubar import (
    FileMainMenu,
    EditMainMenu,
)

class MainMenuBar(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.filemenu = FileMainMenu(None)
        self.editmenu = EditMainMenu(None)
