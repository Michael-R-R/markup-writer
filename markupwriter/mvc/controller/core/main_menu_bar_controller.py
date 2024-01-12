#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.mvc.model.core import (
    MainMenuBar,
)

from markupwriter.mvc.view.core import (
    MainMenuBarView,
)


class MainMenuBarController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = MainMenuBar(self)
        self.view = MainMenuBarView(None)
        
    def setup(self):
        self.setActionStates(False)
        
    def setActionStates(self, isEnabled: bool):
        # --- File menu --- #
        fileMenu = self.view.filemenu
        fileMenu.saveAction.setEnabled(isEnabled)
        fileMenu.saveAsAction.setEnabled(isEnabled)
        fileMenu.closeAction.setEnabled(isEnabled)
