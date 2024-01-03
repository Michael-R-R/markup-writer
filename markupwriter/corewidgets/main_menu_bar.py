#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMenuBar,
    QWidget,
)

from markupwriter.menus.mainmenubar import (
    FileMainMenu,
    EditMainMenu,
)

class MainMenuBar(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.fileMenu = FileMainMenu(self)
        self.editMenu = EditMainMenu(self)

        self.addMenu(self.fileMenu)
        self.addMenu(self.editMenu)