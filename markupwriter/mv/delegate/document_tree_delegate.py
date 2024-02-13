#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.mv.model as m
import markupwriter.mv.view as v
import markupwriter.support.doctree.item as dti


class DocumentTreeDelegate(QObject):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)
    
    navedUpItem = pyqtSignal()
    navedDownItem = pyqtSignal()
    previewedItem = pyqtSignal()
    renamedItem = pyqtSignal()
    trashedItem = pyqtSignal()
    recoveredItem = pyqtSignal()
    emptiedTrash = pyqtSignal()
    
    createdNovel = pyqtSignal()
    createdMiscFolder = pyqtSignal()
    createdTitle = pyqtSignal()
    createdChapter = pyqtSignal()
    createdScene = pyqtSignal()
    createdSection = pyqtSignal()
    createdMiscFile = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = m.DocumentTreeModel(self)
        self.view = v.DocumentTreeView(None)

        self._setupViewConnections()
        
    def setEnabledTreeBarActions(self, isEnabled: bool):
        tb = self.view.treeBar
        tb.navUpAction.setEnabled(isEnabled)
        tb.navDownAction.setEnabled(isEnabled)
        tb.itemMenuAction.setEnabled(isEnabled)
    
    def setEnabledTreeActions(self, isEnabled: bool):
        tcm = self.view.treeWidget.treeContextMenu
        tcm.itemMenu.setEnabled(isEnabled)
    
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
        tb.navUpAction.triggered.connect(lambda: self.navedUpItem.emit())
        tb.navDownAction.triggered.connect(lambda: self.navedDownItem.emit())
        
        im = tb.itemMenuAction.itemMenu
        im.novelAction.triggered.connect(lambda: self.createdNovel.emit())
        im.miscFolderAction.triggered.connect(lambda: self.createdMiscFolder.emit())
        im.titleAction.triggered.connect(lambda: self.createdTitle.emit())
        im.chapterAction.triggered.connect(lambda: self.createdChapter.emit())
        im.sceneAction.triggered.connect(lambda: self.createdScene.emit())
        im.sectionAction.triggered.connect(lambda: self.createdSection.emit())
        im.miscFileAction.triggered.connect(lambda: self.createdMiscFile.emit())

        tw = self.view.treeWidget
        tw.fileAdded.connect(lambda x: self.fileAdded.emit(x))
        tw.fileRemoved.connect(lambda x, y: self.fileRemoved.emit(x, y))
        tw.fileOpened.connect(lambda x, y: self.fileOpened.emit(x, y))
        tw.fileMoved.connect(lambda x, y: self.fileMoved.emit(x, y))
        
        im = tw.treeContextMenu.itemMenu
        im.novelAction.triggered.connect(lambda: self.createdNovel.emit())
        im.miscFolderAction.triggered.connect(lambda: self.createdMiscFolder.emit())
        im.titleAction.triggered.connect(lambda: self.createdTitle.emit())
        im.chapterAction.triggered.connect(lambda: self.createdChapter.emit())
        im.sceneAction.triggered.connect(lambda: self.createdScene.emit())
        im.sectionAction.triggered.connect(lambda: self.createdSection.emit())
        im.miscFileAction.triggered.connect(lambda: self.createdMiscFile.emit())

        icm = tw.itemContextMenu
        icm.previewAction.triggered.connect(lambda: self.previewedItem.emit())
        icm.renameAction.triggered.connect(lambda: self.renamedItem.emit())
        icm.toTrashAction.triggered.connect(lambda: self.trashedItem.emit())
        icm.recoverAction.triggered.connect(lambda: self.recoveredItem.emit())

        tcm = tw.trashContextMenu
        tcm.emptyAction.triggered.connect(lambda: self.emptiedTrash.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.model
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.model
        sin >> self.view
        return sin
