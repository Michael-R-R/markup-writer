#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.mv.model as m
import markupwriter.mv.view as v
import markupwriter.support.doctree.item as dti


# TODO rework signals for add item menu
class DocumentTreeDelegate(QObject):
    navUpTriggered = pyqtSignal()
    navDownTriggered = pyqtSignal()
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)
    previewTriggered = pyqtSignal()
    renameTriggered = pyqtSignal()
    toTrashTriggered = pyqtSignal()
    recoverTriggered = pyqtSignal()
    emptyTrashTriggered = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = m.DocumentTreeModel(self)
        self.view = v.DocumentTreeView(None)

        self._setupViewConnections()
        
    def setEnabledTreeBarActions(self, isEnabled: bool):
        tb = self.view.treeBar
        tb.navUpAction.setEnabled(isEnabled)
        tb.navDownAction.setEnabled(isEnabled)
        tb.addItemAction.setEnabled(isEnabled)
    
    def setEnabledTreeActions(self, isEnabled: bool):
        tcm = self.view.treeWidget.treeContextMenu
        tcm.addItemMenu.setEnabled(isEnabled)
    
    def createRootFolders(self):
        tw = self.view.treeWidget
        tw.add(dti.PlotFolderItem())
        tw.add(dti.TimelineFolderItem())
        tw.add(dti.CharsFolderItem())
        tw.add(dti.LocFolderItem())
        tw.add(dti.ObjFolderItem())
        tw.add(dti.TrashFolderItem())

    def _setupViewConnections(self):
        tb = self.view.treeBar
        tb.navUpAction.triggered.connect(lambda: self.navUpTriggered.emit())
        tb.navDownAction.triggered.connect(lambda: self.navDownTriggered.emit())

        tw = self.view.treeWidget
        tw.fileAdded.connect(lambda x: self.fileAdded.emit(x))
        tw.fileRemoved.connect(lambda x, y: self.fileRemoved.emit(x, y))
        tw.fileOpened.connect(lambda x, y: self.fileOpened.emit(x, y))
        tw.fileMoved.connect(lambda x, y: self.fileMoved.emit(x, y))

        icm = tw.itemContextMenu
        icm.previewAction.triggered.connect(lambda: self.previewTriggered.emit())
        icm.renameAction.triggered.connect(lambda: self.renameTriggered.emit())
        icm.toTrashAction.triggered.connect(lambda: self.toTrashTriggered.emit())
        icm.recoverAction.triggered.connect(lambda: self.recoverTriggered.emit())

        tcm = tw.trashContextMenu
        tcm.emptyAction.triggered.connect(lambda: self.emptyTrashTriggered.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.model
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.model
        sin >> self.view
        return sin
