#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.vdw.view as v
import markupwriter.gui.menus.doctree as dtm


class DocumentTreeDelegate(QObject):
    navUpClicked = pyqtSignal()
    navDownClicked = pyqtSignal()
    filterChanged = pyqtSignal(str)
    
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)
    fileRenamed = pyqtSignal(str, str, str)
    previewRequested = pyqtSignal(str, str)
    dragDropDone = pyqtSignal()

    cmPreviewClicked = pyqtSignal()
    cmRenameClicked = pyqtSignal()
    cmToTrashClicked = pyqtSignal()
    cmRecoverClicked = pyqtSignal()
    cmEmptyTrashClicked = pyqtSignal()

    createNovelClicked = pyqtSignal()
    createFolderClicked = pyqtSignal()
    createTitleClicked = pyqtSignal()
    createChapterClicked = pyqtSignal()
    createSceneClicked = pyqtSignal()
    createSectionClicked = pyqtSignal()
    createFileClicked = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.DocumentTreeView(None)

        self._setupViewConnections()

    def _setupViewConnections(self):
        tb = self.view.treeBar
        tb.navUpAction.triggered.connect(lambda: self.navUpClicked.emit())
        tb.navDownAction.triggered.connect(lambda: self.navDownClicked.emit())
        tb.filterLineEdit.textChanged.connect(lambda x: self.filterChanged.emit(x))

        bt = self.view.treeWidget
        bt.fileAdded.connect(lambda x: self.fileAdded.emit(x))
        bt.fileRemoved.connect(lambda x, y: self.fileRemoved.emit(x, y))
        bt.fileOpened.connect(lambda x, y: self.fileOpened.emit(x, y))
        bt.fileMoved.connect(lambda x, y: self.fileMoved.emit(x, y))
        bt.fileRenamed.connect(lambda x, y, z: self.fileRenamed.emit(x, y, z))
        bt.dragDropDone.connect(lambda: self.dragDropDone.emit())

        icm = bt.itemContextMenu
        icm.previewAction.triggered.connect(lambda: self.cmPreviewClicked.emit())
        icm.renameAction.triggered.connect(lambda: self.cmRenameClicked.emit())
        icm.toTrashAction.triggered.connect(lambda: self.cmToTrashClicked.emit())
        icm.recoverAction.triggered.connect(lambda: self.cmRecoverClicked.emit())

        tcm = bt.trashContextMenu
        tcm.emptyAction.triggered.connect(lambda: self.cmEmptyTrashClicked.emit())

        im = tb.itemMenuAction.itemMenu
        self._setupItemMenuConnections(im)

        im = bt.treeContextMenu.itemMenu
        self._setupItemMenuConnections(im)

        im = icm.itemMenu
        self._setupItemMenuConnections(im)

    def _setupItemMenuConnections(self, im: dtm.ItemMenu):
        im.novelAction.triggered.connect(lambda: self.createNovelClicked.emit())
        im.miscFolderAction.triggered.connect(lambda: self.createFolderClicked.emit())
        im.titleAction.triggered.connect(lambda: self.createTitleClicked.emit())
        im.chapterAction.triggered.connect(lambda: self.createChapterClicked.emit())
        im.sceneAction.triggered.connect(lambda: self.createSceneClicked.emit())
        im.sectionAction.triggered.connect(lambda: self.createSectionClicked.emit())
        im.miscFileAction.triggered.connect(lambda: self.createFileClicked.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
