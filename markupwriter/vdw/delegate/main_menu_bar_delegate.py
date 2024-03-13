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
    fmImportTxtTriggered = pyqtSignal()
    fmExportTriggered = pyqtSignal()
    fmCloseTriggered = pyqtSignal()
    fmExitTriggered = pyqtSignal()

    dmSpellToggled = pyqtSignal(bool)
    dmRefreshPreview = pyqtSignal()
    dmTogglePreview = pyqtSignal()

    vmDocTreeTriggered = pyqtSignal()
    vmDocEditorTriggered = pyqtSignal()
    vmDocPreviewTriggered = pyqtSignal()
    vmTelescopeTriggered = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.MainMenuBarView(None)

        self._setupFileMenuConnections()

    def _setupFileMenuConnections(self):
        fm = self.view.fileMenu
        fm.newProjAction.triggered.connect(lambda: self.fmNewTriggered.emit())
        fm.openProjAction.triggered.connect(lambda: self.fmOpenTriggered.emit())
        fm.saveDocAction.triggered.connect(lambda: self.fmSaveDocTriggered.emit())
        fm.saveProjAction.triggered.connect(lambda: self.fmSaveTriggered.emit())
        fm.saveProjAsAction.triggered.connect(lambda: self.fmSaveAsTriggered.emit())
        fm.importTxtAction.triggered.connect(lambda: self.fmImportTxtTriggered.emit())
        fm.exportAction.triggered.connect(lambda: self.fmExportTriggered.emit())
        fm.closeProjAction.triggered.connect(lambda: self.fmCloseTriggered.emit())
        fm.exitAction.triggered.connect(lambda: self.fmExitTriggered.emit())

        dm = self.view.docMenu
        dm.toggleSpell.toggled.connect(lambda x: self.dmSpellToggled.emit(x))
        dm.refreshPreview.triggered.connect(lambda: self.dmRefreshPreview.emit())
        dm.togglePreview.triggered.connect(lambda: self.dmTogglePreview.emit())

        vm = self.view.viewMenu
        vm.treeAction.triggered.connect(lambda: self.vmDocTreeTriggered.emit())
        vm.editorAction.triggered.connect(lambda: self.vmDocEditorTriggered.emit())
        vm.previewAction.triggered.connect(lambda: self.vmDocPreviewTriggered.emit())
        vm.telecopeAction.triggered.connect(lambda: self.vmTelescopeTriggered.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
