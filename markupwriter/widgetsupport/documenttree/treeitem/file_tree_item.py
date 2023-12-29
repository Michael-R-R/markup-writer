#!/usr/bin/python

from __future__ import annotations
from enum import auto, Enum
import uuid

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from .base_tree_item import (
    BaseTreeItem,
)

from markupwriter.support.iconprovider import(
    Icon,
)

class FILE(Enum):
    title = 0
    chapter = auto()
    scene = auto()
    section = auto()
    misc = auto()

class FileTreeItem(BaseTreeItem):
    def __init__(self,
                 fileType: FILE=None,
                 title: str=None,
                 content: str=None,
                 item: QTreeWidgetItem=None,
                 parent: QWidget=None):
        super().__init__(title, item, False, parent)
        self._hash = str(uuid.uuid1())
        self._fileType = fileType
        self._content = content
        self.applyChanges()

    def hash(self, value: str) -> str:
        self._hash = value
    hash = property(lambda self: self._hash, hash)

    def fileType(self, fileType: FILE):
        self._fileType = fileType
        self.applyIcon()
    fileType = property(lambda self: self._fileType, fileType)

    def content(self, text: str):
        self._content = text
    content = property(lambda self: self._content, content)

    def deepcopy(self, parent: QWidget):
        myCopy = FileTreeItem(self.fileType,
                              self.title,
                              self.content,
                              self.item,
                              parent)
        myCopy.hash = self.hash
        myCopy.applyIcon()
        return myCopy

    def applyIcon(self):
        match self._fileType:
            case FILE.title:
                self.icon = Icon.TITLE_FILE
            case FILE.chapter:
                self.icon = Icon.CHAPTER_FILE
            case FILE.scene:
                self.icon = Icon.SCENE_FILE
            case FILE.section:
                self.icon = Icon.SECTION_FILE
            case FILE.misc:
                self.icon = Icon.MISC_FILE

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeQString(self._hash)
        sOut.writeInt(self._fileType.value)
        sOut.writeQString(self._content)
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._hash = sIn.readQString()
        self._fileType = FILE(sIn.readInt())
        self._content = sIn.readQString()
        return super().__rrshift__(sIn)