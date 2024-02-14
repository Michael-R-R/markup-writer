#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.vdw.view as v


class MainMenuBarDelegate(QObject):
    fmNewTriggered = pyqtSignal()
    fmOpenTriggered = pyqtSignal()
    fmSaveDocTriggered = pyqtSignal()
    fmSaveTriggered = pyqtSignal()
    fmSaveAsTriggered = pyqtSignal()
    fmExportTriggered = pyqtSignal()
    fmCloseTriggered = pyqtSignal()
    fmExitTriggered = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.MainMenuBarView(None)

        self._setupFileMenuConnections()

    def setEnableSaveDocAction(self, isEnabled: bool):
        self.view.fileMenu.saveDocAction.setEnabled(isEnabled)

    def setEnableSaveAction(self, isEnabled: bool):
        self.view.fileMenu.saveProjAction.setEnabled(isEnabled)

    def setEnableSaveAsAction(self, isEnabled: bool):
        self.view.fileMenu.saveProjAsAction.setEnabled(isEnabled)

    def setEnableExportAction(self, isEnabled: bool):
        self.view.fileMenu.exportAction.setEnabled(isEnabled)

    def setEnableCloseAction(self, isEnabled: bool):
        self.view.fileMenu.closeProjAction.setEnabled(isEnabled)

    def _setupFileMenuConnections(self):
        fm = self.view.fileMenu
        fm.newProjAction.triggered.connect(lambda: self.fmNewTriggered.emit())
        fm.openProjAction.triggered.connect(lambda: self.fmOpenTriggered.emit())
        fm.saveDocAction.triggered.connect(lambda: self.fmSaveDocTriggered.emit())
        fm.saveProjAction.triggered.connect(lambda: self.fmSaveTriggered.emit())
        fm.saveProjAsAction.triggered.connect(lambda: self.fmSaveAsTriggered.emit())
        fm.exportAction.triggered.connect(lambda: self.fmExportTriggered.emit())
        fm.closeProjAction.triggered.connect(lambda: self.fmCloseTriggered.emit())
        fm.exitAction.triggered.connect(lambda: self.fmExitTriggered.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
