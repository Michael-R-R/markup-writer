#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

import markupwriter.vdw.view as v


class MainMenuBarWorker(QObject):
    def __init__(
        self,
        mmbv: v.MainMenuBarView,
        parent: QObject | None,
    ) -> None:
        super().__init__(parent)

        self.mmbv = mmbv

    def onNewProject(self):
        fm = self.mmbv.fileMenu
        fm.saveProjAction.setEnabled(True)
        fm.saveProjAsAction.setEnabled(True)
        fm.importMenu.setEnabled(True)
        fm.exportAction.setEnabled(True)
        fm.closeProjAction.setEnabled(True)

    def onOpenProject(self):
        fm = self.mmbv.fileMenu
        fm.saveProjAction.setEnabled(True)
        fm.saveProjAsAction.setEnabled(True)
        fm.importMenu.setEnabled(True)
        fm.exportAction.setEnabled(True)
        fm.closeProjAction.setEnabled(True)

    @pyqtSlot(bool)
    def onDocumentStatusChanged(self, status: bool):
        fm = self.mmbv.fileMenu
        fm.saveDocAction.setEnabled(status)
        
    @pyqtSlot(int)
    def onTabCountChanged(self, count: int):
        dm = self.mmbv.docMenu
        
        status = count > 0
        dm.refreshPreview.setEnabled(status)
        dm.togglePreview.setEnabled(status)
