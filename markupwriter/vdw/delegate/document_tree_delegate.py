#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
    QPoint,
)

import markupwriter.vdw.view as v
import markupwriter.vdw.worker as w
import markupwriter.gui.menus.doctree as dtm


class DocumentTreeDelegate(QObject):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)
    fileRenamed = pyqtSignal(str, str, str)
    previewRequested = pyqtSignal(str, str)
    dragDropDone = pyqtSignal()
    contextMenuRequested = pyqtSignal(QPoint)

    navUpClicked = pyqtSignal()
    navDownClicked = pyqtSignal()

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
        self.worker = w.DocumentTreeWorker(self.view, self)

        self._setupViewConnections()

    def _setupViewConnections(self):
        tb = self.view.treeBar
        tb.navUpAction.triggered.connect(lambda: self.navUpClicked.emit())
        tb.navDownAction.triggered.connect(lambda: self.navDownClicked.emit())

        tw = self.view.treeWidget
        tw.fileAdded.connect(lambda x: self.fileAdded.emit(x))
        tw.fileRemoved.connect(lambda x, y: self.fileRemoved.emit(x, y))
        tw.fileOpened.connect(lambda x, y: self.fileOpened.emit(x, y))
        tw.fileMoved.connect(lambda x, y: self.fileMoved.emit(x, y))
        tw.fileRenamed.connect(lambda x, y, z: self.fileRenamed.emit(x, y, z))
        tw.filePreviewed.connect(lambda x, y: self.previewRequested.emit(x, y))
        tw.dragDropDone.connect(lambda: self.dragDropDone.emit())
        tw.customContextMenuRequested.connect(
            lambda x: self.contextMenuRequested.emit(x)
        )

        icm = tw.itemContextMenu
        icm.previewAction.triggered.connect(lambda: self.cmPreviewClicked.emit())
        icm.renameAction.triggered.connect(lambda: self.cmRenameClicked.emit())
        icm.toTrashAction.triggered.connect(lambda: self.cmToTrashClicked.emit())
        icm.recoverAction.triggered.connect(lambda: self.cmRecoverClicked.emit())

        tcm = tw.trashContextMenu
        tcm.emptyAction.triggered.connect(lambda: self.cmEmptyTrashClicked.emit())

        im = tb.itemMenuAction.itemMenu
        self._setupItemMenuConnections(im)

        im = tw.treeContextMenu.itemMenu
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
