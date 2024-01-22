#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
)

from markupwriter.mvc.model.core import (
    MainMenuBar,
)

from markupwriter.mvc.view.core import (
    MainMenuBarView,
)


class MainMenuBarController(QObject):
    newProjClicked = pyqtSignal()
    openProjClicked = pyqtSignal()
    saveDocClicked = pyqtSignal()
    saveProjClicked = pyqtSignal()
    saveProjAsClicked = pyqtSignal()
    closeProjClicked = pyqtSignal()
    exitClicked = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = MainMenuBar(self)
        self.view = MainMenuBarView(None)

    def setup(self):
        self.setActionStates(False)

        # --- Main menu slots --- #
        fm = self.view.filemenu
        fm.newProjAction.triggered.connect(lambda: self.newProjClicked.emit())
        fm.openProjAction.triggered.connect(lambda: self.openProjClicked.emit())
        fm.saveDocumentAction.triggered.connect(lambda: self.saveDocClicked.emit())
        fm.saveProjAction.triggered.connect(lambda: self.saveProjClicked.emit())
        fm.saveProjectAsAction.triggered.connect(lambda: self.saveProjAsClicked.emit())
        fm.closeProjectAction.triggered.connect(lambda: self.closeProjClicked.emit())
        fm.exitAction.triggered.connect(lambda: self.exitClicked.emit())

    def setActionStates(self, isEnabled: bool):
        # --- File menu --- #
        fileMenu = self.view.filemenu
        fileMenu.saveProjAction.setEnabled(isEnabled)
        fileMenu.saveProjectAsAction.setEnabled(isEnabled)
        fileMenu.closeProjectAction.setEnabled(isEnabled)
