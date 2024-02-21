#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

from markupwriter.gui.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

from markupwriter.config import ProjectConfig
from markupwriter.common.util import File

import markupwriter.vdw.delegate as d
import markupwriter.support.doctree.item as ti


class DocumentTreeWorker(QObject):
    def __init__(self, dtd: d.DocumentTreeDelegate, parent: QObject | None) -> None:
        super().__init__(parent)

        self.dtd = dtd
        
    def onNewProject(self):
        tb = self.dtd.view.treeBar
        tb.navUpAction.setEnabled(True)
        tb.navDownAction.setEnabled(True)
        tb.itemMenuAction.setEnabled(True)
        tb.filterAction.setEnabled(True)
        
        tw = self.dtd.view.treeWidget
        tcm = tw.treeContextMenu
        tcm.itemMenu.setEnabled(True)
        
        tw.add(ti.PlotFolderItem())
        tw.add(ti.TimelineFolderItem())
        tw.add(ti.CharsFolderItem())
        tw.add(ti.LocFolderItem())
        tw.add(ti.ObjFolderItem())
        tw.add(ti.TrashFolderItem())
        
    def onOpenProject(self):
        tb = self.dtd.view.treeBar
        tb.navUpAction.setEnabled(True)
        tb.navDownAction.setEnabled(True)
        tb.itemMenuAction.setEnabled(True)
        tb.filterAction.setEnabled(True)
        
        tw = self.dtd.view.treeWidget
        tcm = tw.treeContextMenu
        tcm.itemMenu.setEnabled(True)
        
    @pyqtSlot(str)
    def onFileAdded(self, uuid: str):
        path = ProjectConfig.contentPath()
        if path is None:
            return
        path = os.path.join(path, uuid)
        File.write(path, "")
    
    @pyqtSlot(str, str)
    def onFileRemoved(self, title: str, uuid: str):
        path = ProjectConfig.contentPath()
        if path is None:
            return
        path = os.path.join(path, uuid)
        File.remove(path)

        tw = self.dtd.view.treeWidget
        tw.refreshAllWordCounts()
        
    @pyqtSlot()
    def onDragDropDone(self):
        self.dtd.view.treeWidget.refreshAllWordCounts()
        
    @pyqtSlot()
    def onNavItemUp(self):
        self.dtd.view.treeWidget.translate(-1)
    
    @pyqtSlot()
    def onNavItemDown(self):
        self.dtd.view.treeWidget.translate(1)
        
    @pyqtSlot(str)
    def onFilterTextChanged(self, text: str):
        # TODO implement
        tw = self.dtd.view.treeWidget
        tw.filter(text)
    
    @pyqtSlot()
    def onPreviewItem(self):
        tw = self.dtd.view.treeWidget
        index = tw.currentIndex()
        if index is None:
            return

        widget: ti.BaseTreeItem = tw.indexWidget(index)
        self.dtd.previewRequested.emit(widget.title(), widget.UUID())
    
    @pyqtSlot()
    def onRenamedItem(self):
        tw = self.dtd.view.treeWidget
        index = tw.currentIndex()
        if index is None:
            return
        
        name = StrDialog.run("Rename", "", self.dtd.view)
        if name is None:
            return
        
        item = tw.dataModel.itemFromIndex(index)
        tw.rename(item, name)
    
    @pyqtSlot()
    def onTrashItem(self):
        tw = self.dtd.view.treeWidget
        index = tw.currentIndex()
        if index is None:
            return
        
        if not YesNoDialog.run("Move to trash?", self.dtd.view):
            return
        
        trash = tw.findTrash()
        if trash is None:
            return

        item = tw.dataModel.itemFromIndex(index)
        tw.appendMove(item, trash)
    
    @pyqtSlot()
    def onRecoverItem(self):
        tw = self.dtd.view.treeWidget
        index = tw.currentIndex()
        if index is None:
            return

        item = tw.dataModel.itemFromIndex(index)
        tw.appendMove(item, None)
    
    @pyqtSlot()
    def onEmptyTrash(self):
        tw = self.dtd.view.treeWidget
        index = tw.currentIndex()
        if index is None:
            return

        if not YesNoDialog.run("Empty trash?", self.dtd.view):
            return

        item = tw.dataModel.itemFromIndex(index)
        for i in range(item.rowCount() - 1, -1, -1):
            tw.remove(item.child(i))

    @pyqtSlot()
    def onNovelFolderCreated(self):
        title = StrDialog.run("Novel Name", "Novel", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        widget = ti.NovelFolderItem(title, tw)
        tw.add(widget)

    @pyqtSlot()
    def onMiscFolderCreated(self):
        title = StrDialog.run("Folder Name", "Folder", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        widget = ti.MiscFolderItem(title, tw)
        tw.add(widget)

    @pyqtSlot()
    def onTitleFileCreated(self):
        title = StrDialog.run("Title Name", "Title", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        widget = ti.TitleFileItem(title, tw)
        tw.add(widget)

    @pyqtSlot()
    def onChapterFileCreated(self):
        title = StrDialog.run("Chapter Name", "Chapter", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        widget = ti.ChapterFileItem(title, tw)
        tw.add(widget)

    @pyqtSlot()
    def onSceneFileCreated(self):
        title = StrDialog.run("Scene Name", "Scene", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        widget = ti.SceneFileItem(title, tw)
        tw.add(widget)

    @pyqtSlot()
    def onSectionFileCreated(self):
        title = StrDialog.run("Section Name", "Section", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        widget = ti.SectionFileItem(title, tw)
        tw.add(widget)

    @pyqtSlot()
    def onMiscFileCreated(self):
        title = StrDialog.run("Misc. Name", "Misc.", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        widget = ti.MiscFileItem(title, tw)
        tw.add(widget)
        
    @pyqtSlot(str, int)
    def onWordCountChanged(self, uuid: str, count: int):
        tw = self.dtd.view.treeWidget
        widget = tw.findWidget(uuid)
        if widget is None:
            return

        owc = widget.wordCount()
        twc = widget.totalWordCount() - owc + count

        widget.setWordCount(count)
        widget.setTotalWordCount(twc)

        tw.refreshWordCounts(widget.item.parent(), owc, count)
        
    @pyqtSlot(str)
    def onDocPreviewRequested(self, uuid: str):
        tw = self.dtd.view.treeWidget
        widget: ti.BaseTreeItem = tw.findWidget(uuid)
        if widget is None:
            return
        self.dtd.previewRequested.emit(widget.title(), uuid)
