#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
    QPoint,
)

import markupwriter.gui.widgets as w
import markupwriter.vdw.delegate as d


class MainMenuBarWorker(QObject):
    def __init__(
        self,
        mmbd: d.MainMenuBarDelegate,
        dtd: d.DocumentTreeDelegate,
        ded: d.DocumentEditorDelegate,
        parent: QObject | None,
    ) -> None:
        super().__init__(parent)

        self.dtd = dtd
        self.ded = ded
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
        
    @pyqtSlot()
    def onTelescopeTriggered(self):
        tw = self.dtd.view.treeWidget
        parent = self.mmbd.view.parentWidget()
        telescope = w.TelescopeWidget(tw, parent)
        telescope.resize(800, 400)
        telescope.show()
        pos = telescope.rect().center() / 2
        telescope.move(parent.rect().center() - pos)
