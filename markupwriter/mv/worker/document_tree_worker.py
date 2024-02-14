#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

from markupwriter.gui.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

import markupwriter.mv.delegate as d
import markupwriter.support.doctree.item as ti


class DocumentTreeWorker(QObject):
    def __init__(self, dtd: d.DocumentTreeDelegate, parent: QObject | None) -> None:
        super().__init__(parent)

        self.dtd = dtd
        
    @pyqtSlot()
    def onDragDropDone(self):
        self.dtd.view.treeWidget.refreshAllWordCounts()
        
    @pyqtSlot()
    def onNavItemUp(self):
        self.dtd.view.treeWidget.translate(-1)
    
    @pyqtSlot()
    def onNavItemDown(self):
        self.dtd.view.treeWidget.translate(1)
    
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
        
        trash = tw.findTrash()
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
