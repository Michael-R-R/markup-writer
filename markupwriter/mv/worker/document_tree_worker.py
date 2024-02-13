#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

from markupwriter.gui.dialogs.modal import StrDialog

import markupwriter.mv.delegate as d
import markupwriter.support.doctree.item as ti


class DocumentTreeWorker(QObject):
    def __init__(self, dtd: d.DocumentTreeDelegate, parent: QObject | None) -> None:
        super().__init__(parent)

        self.dtd = dtd

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
