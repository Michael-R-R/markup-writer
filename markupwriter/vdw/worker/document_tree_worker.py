#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
    QPoint,
)

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.gui.dialogs.modal import (
    StrDialog,
    YesNoDialog,
    ErrorDialog,
)

from markupwriter.config import ProjectConfig
from markupwriter.common.util import File

import markupwriter.vdw.view as v
import markupwriter.gui.dialogs.modal as dm
import markupwriter.gui.widgets as w
import markupwriter.support.doctree as dt
import markupwriter.support.doctree.item as ti


class DocumentTreeWorker(QObject):
    filePreviewed = pyqtSignal(str, str)
    
    def __init__(self, dtv: v.DocumentTreeView, parent: QObject | None) -> None:
        super().__init__(parent)

        self.dtv = dtv
        
    def onNewProject(self):
        tb = self.dtv.treeBar
        tb.navUpAction.setEnabled(True)
        tb.navDownAction.setEnabled(True)
        tb.itemMenuAction.setEnabled(True)
        
        tw = self.dtv.treeWidget
        tcm = tw.treeContextMenu
        tcm.itemMenu.setEnabled(True)
        
        tw.add(ti.PlotFolderItem())
        tw.add(ti.TimelineFolderItem())
        tw.add(ti.CharsFolderItem())
        tw.add(ti.LocFolderItem())
        tw.add(ti.ObjFolderItem())
        tw.add(ti.TrashFolderItem())
        
    def onOpenProject(self):
        tb = self.dtv.treeBar
        tb.navUpAction.setEnabled(True)
        tb.navDownAction.setEnabled(True)
        tb.itemMenuAction.setEnabled(True)
        
        tw = self.dtv.treeWidget
        tcm = tw.treeContextMenu
        tcm.itemMenu.setEnabled(True)
    
    @pyqtSlot()
    def onImportTxtFile(self):
        dialog = dm.ImportDialog("", self.dtv)
        if dialog.exec() != 1:
            return
        
        content = File.read(dialog.path)
        if content is None:
            ErrorDialog.run("ERROR: cannot read file contents", None)
            return
        
        path = os.path.join(ProjectConfig.contentPath(), dialog.value.UUID())
        if not File.write(path, content):
            ErrorDialog.run("ERROR: cannot write file contents", None)
            return
        
        tw = self.dtv.treeWidget
        tw.blockSignals(True)
        tw.add(dialog.value)
        tw.blockSignals(False)
        
    @pyqtSlot()
    def onExportNovel(self):
        tw = self.dtv.treeWidget
        
        e = dt.EpubExporter()
        e.export(tw, tw)
    
    @pyqtSlot()
    def onFocusTreeTriggered(self):
        tw = self.dtv.treeWidget
        tw.setFocus()
        tw.setExpanded(tw.currentIndex(), True)
        
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

        tw = self.dtv.treeWidget
        tw.refreshAllWordCounts()
        
    @pyqtSlot()
    def onDragDropDone(self):
        tw = self.dtv.treeWidget
        tw.refreshAllWordCounts()
        
    @pyqtSlot(QPoint)
    def onContextMenuRequested(self, pos: QPoint):
        tw = self.dtv.treeWidget
        
        item = tw.itemAt(pos)
        widget: ti.BaseTreeItem = tw.itemWidget(item, 0)
        pos = tw.mapToGlobal(pos)
        if item is None:
            tw.treeContextMenu.onShowMenu(pos)
        elif isinstance(widget, ti.TrashFolderItem):
            isEmpty = item.childCount() < 1
            args = [isEmpty]
            tw.trashContextMenu.onShowMenu(pos, args)
        else:
            isFile = widget.hasFlag(ti.ITEM_FLAG.file)
            inTrash = tw.isInTrash(item)
            isMutable = widget.hasFlag(ti.ITEM_FLAG.mutable)
            args = [isFile, inTrash, isMutable]
            tw.itemContextMenu.onShowMenu(pos, args)
        
    @pyqtSlot()
    def onNavItemUp(self):
        self.dtv.treeWidget.translate(-1)
    
    @pyqtSlot()
    def onNavItemDown(self):
        self.dtv.treeWidget.translate(1)
    
    @pyqtSlot()
    def onPreviewItem(self):
        tw = self.dtv.treeWidget
        item = tw.currentItem()
        if item is None:
            return

        widget: ti.BaseTreeItem = tw.itemWidget(item, 0)
        self.filePreviewed.emit(widget.title(), widget.UUID())
    
    @pyqtSlot()
    def onRenamedItem(self):
        tw = self.dtv.treeWidget
        item = tw.currentItem()
        if item is None:
            return
        
        name = StrDialog.run("Rename", "", self.dtv)
        if name is None:
            return
        
        tw.rename(item, name)
    
    @pyqtSlot()
    def onTrashItem(self):
        tw = self.dtv.treeWidget
        item = tw.currentItem()
        if item is None:
            return
        
        if not YesNoDialog.run("Move to trash?", self.dtv):
            return
        
        trash = tw.findTrashFolder()
        if trash is None:
            return

        tw.moveTo(item, trash)
    
    @pyqtSlot()
    def onRecoverItem(self):
        tw = self.dtv.treeWidget
        item = tw.currentItem()
        if item is None:
            return

        tw.moveTo(item, None)
    
    @pyqtSlot()
    def onEmptyTrash(self):
        tw = self.dtv.treeWidget
        item = tw.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Empty trash?", self.dtv):
            return

        for i in range(item.childCount() - 1, -1, -1):
            tw.remove(item.child(i))

    @pyqtSlot()
    def onNovelFolderCreated(self):
        title = StrDialog.run("Novel Name", "Novel", self.dtv)
        if title is None:
            return
        tw = self.dtv.treeWidget
        item = ti.NovelFolderItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onMiscFolderCreated(self):
        title = StrDialog.run("Folder Name", "Folder", self.dtv)
        if title is None:
            return
        tw = self.dtv.treeWidget
        item = ti.MiscFolderItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onTitleFileCreated(self):
        title = StrDialog.run("Title Name", "Title", self.dtv)
        if title is None:
            return
        tw = self.dtv.treeWidget
        item = ti.TitleFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onChapterFileCreated(self):
        title = StrDialog.run("Chapter Name", "Chapter", self.dtv)
        if title is None:
            return
        tw = self.dtv.treeWidget
        item = ti.ChapterFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onSceneFileCreated(self):
        title = StrDialog.run("Scene Name", "Scene", self.dtv)
        if title is None:
            return
        tw = self.dtv.treeWidget
        item = ti.SceneFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onSectionFileCreated(self):
        title = StrDialog.run("Section Name", "Section", self.dtv)
        if title is None:
            return
        tw = self.dtv.treeWidget
        item = ti.SectionFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onMiscFileCreated(self):
        title = StrDialog.run("Misc. Name", "Misc.", self.dtv)
        if title is None:
            return
        tw = self.dtv.treeWidget
        item = ti.MiscFileItem(title, tw)
        tw.add(item)
        
    @pyqtSlot(str, int)
    def onWordCountChanged(self, uuid: str, count: int):
        tw = self.dtv.treeWidget
        widget = tw.findWidget(uuid)
        if widget is None:
            return

        owc = widget.wordCount()
        twc = widget.totalWordCount() - owc + count

        widget.setWordCount(count)
        widget.setTotalWordCount(twc)

        tw.refreshParentWordCounts(widget.item, owc, count)
        
    @pyqtSlot(str)
    def onRefPreviewRequested(self, uuid: str):
        tw = self.dtv.treeWidget
        widget: ti.BaseTreeItem = tw.findWidget(uuid)
        if widget is None:
            return
        self.filePreviewed.emit(widget.title(), uuid)
        
    @pyqtSlot()
    def onTelescopeTriggered(self):
        tw = self.dtv.treeWidget
        telescope = w.TelescopeWidget(tw, tw)
        telescope.resize(800, 400)
        telescope.show()
        
        center = QApplication.primaryScreen().availableGeometry().center() / 2
        telescope.move(center)
