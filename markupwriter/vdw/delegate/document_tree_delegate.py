#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.vdw.view as v
import markupwriter.gui.menus.doctree as dtm


class DocumentTreeDelegate(QObject):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)
    fileRenamed = pyqtSignal(str, str, str)
    dragDropDone = pyqtSignal()
    
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

        self.view = v.DocumentTreeView(None)

        self._setupViewConnections()

    def _setupViewConnections(self):
        tb = self.view.treeBar
        tb.navUpAction.triggered.connect(lambda: self.navedUpItem.emit())
        tb.navDownAction.triggered.connect(lambda: self.navedDownItem.emit())
        
        tw = self.view.treeWidget
        tw.fileAdded.connect(lambda x: self.fileAdded.emit(x))
        tw.fileRemoved.connect(lambda x, y: self.fileRemoved.emit(x, y))
        tw.fileOpened.connect(lambda x, y: self.fileOpened.emit(x, y))
        tw.fileMoved.connect(lambda x, y: self.fileMoved.emit(x, y))
        tw.fileRenamed.connect(lambda x, y, z: self.fileRenamed.emit(x, y, z))
        tw.dragDropDone.connect(lambda: self.dragDropDone.emit())
        
        icm = tw.itemContextMenu
        icm.previewAction.triggered.connect(lambda: self.previewedItem.emit())
        icm.renameAction.triggered.connect(lambda: self.renamedItem.emit())
        icm.toTrashAction.triggered.connect(lambda: self.trashedItem.emit())
        icm.recoverAction.triggered.connect(lambda: self.recoveredItem.emit())
        
        tcm = tw.trashContextMenu
        tcm.emptyAction.triggered.connect(lambda: self.emptiedTrash.emit())
        
        im = tb.itemMenuAction.itemMenu
        self._setupItemMenuConnections(im)
        
        im = tw.treeContextMenu.itemMenu
        self._setupItemMenuConnections(im)
        
        im = icm.itemMenu
        self._setupItemMenuConnections(im)
        
    def _setupItemMenuConnections(self, im: dtm.ItemMenu):
        im.novelAction.triggered.connect(lambda: self.createdNovel.emit())
        im.miscFolderAction.triggered.connect(lambda: self.createdMiscFolder.emit())
        im.titleAction.triggered.connect(lambda: self.createdTitle.emit())
        im.chapterAction.triggered.connect(lambda: self.createdChapter.emit())
        im.sceneAction.triggered.connect(lambda: self.createdScene.emit())
        im.sectionAction.triggered.connect(lambda: self.createdSection.emit())
        im.miscFileAction.triggered.connect(lambda: self.createdMiscFile.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
