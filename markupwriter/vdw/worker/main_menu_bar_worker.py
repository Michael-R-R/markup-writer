#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

import markupwriter.vdw.delegate as d


class MainMenuBarWorker(QObject):
    def __init__(
        self,
        mmbd: d.MainMenuBarDelegate,
        parent: QObject | None,
    ) -> None:
        super().__init__(parent)

        self.mmbd = mmbd

    def onNewProject(self):
        fm = self.mmbd.view.fileMenu
        fm.saveProjAction.setEnabled(True)
        fm.saveProjAsAction.setEnabled(True)
        fm.exportAction.setEnabled(True)
        fm.closeProjAction.setEnabled(True)

    def onOpenProject(self):
        fm = self.mmbd.view.fileMenu
        fm.saveProjAction.setEnabled(True)
        fm.saveProjAsAction.setEnabled(True)
        fm.exportAction.setEnabled(True)
        fm.closeProjAction.setEnabled(True)

    @pyqtSlot(bool)
    def onDocumentStatusChanged(self, status: bool):
        fm = self.mmbd.view.fileMenu
        fm.saveDocAction.setEnabled(status)
