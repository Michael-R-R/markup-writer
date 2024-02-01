#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSlot,
    pyqtSignal,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem,
)

from markupwriter.mvc.model.corewidgets import DocumentTree
from markupwriter.mvc.view.corewidgets import DocumentTreeView
from markupwriter.config import AppConfig
from markupwriter.common.util import File
from markupwriter.gui.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

import markupwriter.support.doctree.item as dti


class DocumentTreeController(QObject):
    filePreviewed = pyqtSignal(str, str)
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str, str)
    fileOpened = pyqtSignal(str, list)
    fileMoved = pyqtSignal(str, list)
    fileRenamed = pyqtSignal(str, str, str)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentTree(self)
        self.view = DocumentTreeView(None)

    def setup(self):
        # --- Tree bar signals --- #
        treebar = self.view.treebar
        treebar.addItemAction.itemCreated.connect(self._onItemCreated)
        treebar.navUpAction.triggered.connect(self._onItemNavUp)
        treebar.navDownAction.triggered.connect(self._onItemNavDown)

        # --- Tree signals --- #
        tree = self.view.treewidget
        tree.fileAdded.connect(self._onFileAdded)
        tree.fileRemoved.connect(self._onFileRemoved)
        tree.fileOpened.connect(self._onFileOpened)
        tree.fileMoved.connect(self._onFileMoved)

        # --- Tree context menu signals --- #
        tcm = self.view.treewidget.treeContextMenu
        tcm.addItemMenu.itemCreated.connect(self._onItemCreated)

        # --- Item context menu signals --- #
        icm = self.view.treewidget.itemContextMenu
        icm.addItemMenu.itemCreated.connect(self._onItemCreated)
        icm.previewAction.triggered.connect(self._onPreviewItem)
        icm.renameAction.triggered.connect(self._onItemRename)
        icm.toTrashAction.triggered.connect(self._onItemMoveToTrash)
        icm.recoverAction.triggered.connect(self._onItemRecover)

        # --- Trash context menu signals --- #
        trcm = self.view.treewidget.trashContextMenu
        trcm.emptyAction.triggered.connect(self._onEmptyTrash)
        
    def setEnabledTreeBarActions(self, isEnabled: bool):
        treeBar = self.view.treebar
        treeBar.navUpAction.setEnabled(isEnabled)
        treeBar.navDownAction.setEnabled(isEnabled)
        treeBar.addItemAction.setEnabled(isEnabled)

    def setEnabledTreeActions(self, isEnabled: bool):
        tree = self.view.treewidget
        tree.treeContextMenu.addItemMenu.setEnabled(isEnabled)

    def createRootFolders(self):
        tree = self.view.treewidget
        tree.add(dti.PlotFolderItem())
        tree.add(dti.TimelineFolderItem())
        tree.add(dti.CharsFolderItem())
        tree.add(dti.LocFolderItem())
        tree.add(dti.ObjFolderItem())
        tree.add(dti.TrashFolderItem())

    def onWordCountChanged(self, uuid: str, wc: int):
        widget = self.findItemWidget(uuid)
        if widget is None:
            return
        
        owc = widget.wordCount()
        twc = widget.totalWordCount() - owc + wc
        
        widget.setWordCount(wc)
        widget.setTotalWordCount(twc)

        self._refreshParentWordCounts(widget.item.parent(), owc, wc)

    def findItemWidget(self, uuid: str) -> dti.BaseTreeItem | None:
        return self.view.treewidget.findWidget(uuid)
        
    def _refreshParentWordCounts(self, item: QTreeWidgetItem, owc: int, wc: int):
        tree = self.view.treewidget
        
        while item is not None:
            widget: dti.BaseTreeItem = tree.itemWidget(item, 0)
            twc = widget.totalWordCount() - owc + wc
            widget.setTotalWordCount(twc)
            item = item.parent()
        
    def _refreshAllWordCounts(self):
        tree = self.view.treewidget
        
        def helper(pitem: QTreeWidgetItem) -> int:
            pw: dti.BaseTreeItem = tree.itemWidget(pitem, 0)
            twc = pw.wordCount()
            
            for j in range(pitem.childCount()):
                citem = pitem.child(j)
                twc += helper(citem)
                
            pw.setTotalWordCount(twc)
            
            return twc
        
        for i in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(i)
            helper(item)

    @pyqtSlot(str)
    def _onFileAdded(self, uuid: str):
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path = os.path.join(path, uuid)
        File.write(path, "")
        
        self.fileAdded.emit(uuid)

    @pyqtSlot(str, str)
    def _onFileRemoved(self, title: str, uuid: str):
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path = os.path.join(path, uuid)
        File.remove(path)
        
        self._refreshAllWordCounts()
        self.fileRemoved.emit(title, uuid)

    @pyqtSlot(str, list)
    def _onFileOpened(self, uuid: str, pathList: list[str]):
        self.fileOpened.emit(uuid, pathList)

    @pyqtSlot(str, list)
    def _onFileMoved(self, uuid: str, pathList: list[str]):
        self._refreshAllWordCounts()
        self.fileMoved.emit(uuid, pathList)

    @pyqtSlot()
    def _onItemNavUp(self):
        self.view.treewidget.translate(-1)

    @pyqtSlot()
    def _onItemNavDown(self):
        self.view.treewidget.translate(1)

    @pyqtSlot(dti.BaseTreeItem)
    def _onItemCreated(self, item: dti.BaseTreeItem):
        self.view.treewidget.add(item)

    @pyqtSlot()
    def _onPreviewItem(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        widget: dti.BaseTreeItem = tree.itemWidget(item, 0)
        self.filePreviewed.emit(widget.title(), widget.UUID())

    @pyqtSlot()
    def _onItemRename(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        widget: dti.BaseTreeItem = tree.itemWidget(item, 0)
        text = StrDialog.run("Rename", widget.title(), self.view)
        if text is None:
            return

        oldTitle = widget.title()
        widget.setTitle(text)

        if widget.hasFlag(dti.ITEM_FLAG.file):
            self.fileRenamed.emit(widget.UUID(), oldTitle, text)

    @pyqtSlot()
    def _onItemMoveToTrash(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Move to trash?", self.view):
            return

        trash = tree.findTrash()
        if trash is None:
            return

        tree.moveTo(item, trash)

    @pyqtSlot()
    def _onItemRecover(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        tree.moveTo(item, None)

    @pyqtSlot()
    def _onEmptyTrash(self):
        tree = self.view.treewidget
        
        item = tree.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Empty trash?", self.view):
            return

        for i in range(item.childCount() - 1, -1, -1):
            tree.remove(item.child(i))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view.treewidget
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view.treewidget
        return sin
