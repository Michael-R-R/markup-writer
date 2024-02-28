#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
    QPoint,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem,
)

from markupwriter.gui.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

from markupwriter.config import ProjectConfig
from markupwriter.common.util import File

import markupwriter.vdw.delegate as d
import markupwriter.gui.widgets as w
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
        
        tw = self.dtd.view.treeWidget
        tcm = tw.treeContextMenu
        tcm.itemMenu.setEnabled(True)
        
    def refreshParentWordCounts(self, child: QTreeWidgetItem, owc: int, twc: int):
        tw = self.dtd.view.treeWidget
        
        item = child.parent()
        while item is not None:
            widget: ti.BaseTreeItem = tw.itemWidget(item, 0)
            twc = widget.totalWordCount() - owc + twc
            widget.setTotalWordCount(twc)
            item = item.parent()
        
    def refreshAllWordCounts(self):
        tw = self.dtd.view.treeWidget
        
        def helper(pitem: QTreeWidgetItem) -> int:
            pw: ti.BaseTreeItem = tw.itemWidget(pitem, 0)
            twc = pw.wordCount()

            for j in range(pitem.childCount()):
                citem = pitem.child(j)
                twc += helper(citem)

            pw.setTotalWordCount(twc)

            return twc

        for i in range(tw.topLevelItemCount()):
            item = tw.topLevelItem(i)
            helper(item)
            
    def findTrashFolder(self) -> QTreeWidgetItem | None:
        tw = self.dtd.view.treeWidget
        
        for i in range(tw.topLevelItemCount() - 1, -1, -1):
            item = tw.topLevelItem(i)
            widget = tw.itemWidget(item, 0)
            if isinstance(widget, ti.TrashFolderItem):
                return item

        return None
            
    def isInTrash(self, item: QTreeWidgetItem) -> bool:
        trash = self.findTrashFolder()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash
    
    @pyqtSlot()
    def onFocusTreeTriggered(self):
        tw = self.dtd.view.treeWidget
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

        self.refreshAllWordCounts()
        
    @pyqtSlot()
    def onDragDropDone(self):
        self.refreshAllWordCounts()
        
    @pyqtSlot(QPoint)
    def onContextMenuRequested(self, pos: QPoint):
        tw = self.dtd.view.treeWidget
        
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
            inTrash = self.isInTrash(item)
            isMutable = widget.hasFlag(ti.ITEM_FLAG.mutable)
            args = [isFile, inTrash, isMutable]
            tw.itemContextMenu.onShowMenu(pos, args)
        
    @pyqtSlot()
    def onNavItemUp(self):
        self.dtd.view.treeWidget.translate(-1)
    
    @pyqtSlot()
    def onNavItemDown(self):
        self.dtd.view.treeWidget.translate(1)
    
    @pyqtSlot()
    def onPreviewItem(self):
        tw = self.dtd.view.treeWidget
        item = tw.currentItem()
        if item is None:
            return

        widget: ti.BaseTreeItem = tw.itemWidget(item, 0)
        self.dtd.previewRequested.emit(widget.title(), widget.UUID())
    
    @pyqtSlot()
    def onRenamedItem(self):
        tw = self.dtd.view.treeWidget
        item = tw.currentItem()
        if item is None:
            return
        
        name = StrDialog.run("Rename", "", self.dtd.view)
        if name is None:
            return
        
        tw.rename(item, name)
    
    @pyqtSlot()
    def onTrashItem(self):
        tw = self.dtd.view.treeWidget
        item = tw.currentItem()
        if item is None:
            return
        
        if not YesNoDialog.run("Move to trash?", self.dtd.view):
            return
        
        trash = self.findTrashFolder()
        if trash is None:
            return

        tw.moveTo(item, trash)
    
    @pyqtSlot()
    def onRecoverItem(self):
        tw = self.dtd.view.treeWidget
        item = tw.currentItem()
        if item is None:
            return

        tw.moveTo(item, None)
    
    @pyqtSlot()
    def onEmptyTrash(self):
        tw = self.dtd.view.treeWidget
        item = tw.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Empty trash?", self.dtd.view):
            return

        for i in range(item.childCount() - 1, -1, -1):
            tw.remove(item.child(i))

    @pyqtSlot()
    def onNovelFolderCreated(self):
        title = StrDialog.run("Novel Name", "Novel", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        item = ti.NovelFolderItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onMiscFolderCreated(self):
        title = StrDialog.run("Folder Name", "Folder", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        item = ti.MiscFolderItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onTitleFileCreated(self):
        title = StrDialog.run("Title Name", "Title", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        item = ti.TitleFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onChapterFileCreated(self):
        title = StrDialog.run("Chapter Name", "Chapter", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        item = ti.ChapterFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onSceneFileCreated(self):
        title = StrDialog.run("Scene Name", "Scene", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        item = ti.SceneFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onSectionFileCreated(self):
        title = StrDialog.run("Section Name", "Section", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        item = ti.SectionFileItem(title, tw)
        tw.add(item)

    @pyqtSlot()
    def onMiscFileCreated(self):
        title = StrDialog.run("Misc. Name", "Misc.", self.dtd.view)
        if title is None:
            return
        tw = self.dtd.view.treeWidget
        item = ti.MiscFileItem(title, tw)
        tw.add(item)
        
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

        self.refreshParentWordCounts(widget.item, owc, count)
        
    @pyqtSlot(str)
    def onRefPreviewRequested(self, uuid: str):
        tw = self.dtd.view.treeWidget
        widget: ti.BaseTreeItem = tw.findWidget(uuid)
        if widget is None:
            return
        self.dtd.previewRequested.emit(widget.title(), uuid)
        
    @pyqtSlot()
    def onTelescopeTriggered(self):
        tw = self.dtd.view.treeWidget
        parent = self.dtd.view
        telescope = w.TelescopeWidget(tw, parent)
        telescope.resize(800, 400)
        telescope.show()
        telescope.move(parent.rect().center())
