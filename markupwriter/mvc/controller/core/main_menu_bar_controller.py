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
    exportClicked = pyqtSignal()
    closeProjClicked = pyqtSignal()
    exitClicked = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = MainMenuBar(self)
        self.view = MainMenuBarView(None)

    def setup(self):
        # --- Main menu slots --- #
        fm = self.view.filemenu
        fm.newProjAction.triggered.connect(lambda: self.newProjClicked.emit())
        fm.openProjAction.triggered.connect(lambda: self.openProjClicked.emit())
        fm.saveDocAction.triggered.connect(lambda: self.saveDocClicked.emit())
        fm.saveProjAction.triggered.connect(lambda: self.saveProjClicked.emit())
        fm.saveProjAsAction.triggered.connect(lambda: self.saveProjAsClicked.emit())
        fm.exportAction.triggered.connect(lambda: self.exportClicked.emit())
        fm.closeProjAction.triggered.connect(lambda: self.closeProjClicked.emit())
        fm.exitAction.triggered.connect(lambda: self.exitClicked.emit())
         
    def setEnableSaveDocAction(self, isEnabled: bool):
        self.view.filemenu.saveDocAction.setEnabled(isEnabled)
        
    def setEnableSaveAction(self, isEnabled: bool):
        self.view.filemenu.saveProjAction.setEnabled(isEnabled)
         
    def setEnableSaveAsAction(self, isEnabled: bool):
        self.view.filemenu.saveProjAsAction.setEnabled(isEnabled)
         
    def setEnableExportAction(self, isEnabled: bool):
        self.view.filemenu.exportAction.setEnabled(isEnabled)
         
    def setEnableCloseAction(self, isEnabled: bool):
        self.view.filemenu.closeProjAction.setEnabled(isEnabled)
