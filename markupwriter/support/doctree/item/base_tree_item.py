#!/usr/bin/python

import uuid

from enum import IntEnum

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QIcon,
    QStandardItem,
)

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)

from markupwriter.config import (
    AppConfig,
)


class ITEM_FLAG(IntEnum):
    none = 0
    file = 1
    folder = 2
    draggable = 4
    mutable = 8


class BaseTreeItem(QWidget):
    # Widget indices
    ICON = 1
    TITLE = 2
    WORD_COUNT = 3

    def __init__(self, title: str = None, parent: QWidget = None):
        super().__init__(parent)

        self.item = QStandardItem()
        self.flags = ITEM_FLAG.none

        self._uuid = str(uuid.uuid1())
        self._title = title
        self._wordCount = 0
        self._totalWordCount = 0

        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(1, 2, 1, 2)
        hLayout.addWidget(QLabel("icon", self))
        hLayout.addWidget(QLabel("title", self))
        hLayout.addStretch()
        hLayout.addWidget(QLabel("wc", self))

        self.applyChanges()

    def shallowcopy(self, other=None):
        other.item = self.item
        other.flags = self.flags
        other._uuid = self._uuid
        other._title = self._title
        other._wordCount = self._wordCount
        other._totalWordCount = self._totalWordCount
        return other

    def applyIcon(self):
        raise NotImplementedError()

    def applyChanges(self):
        self.applyIcon()
        self.setTitle(self._title)
        self.setTotalWordCount(self._totalWordCount)

    def UUID(self) -> str:
        return self._uuid

    def title(self) -> str:
        return self._title

    def wordCount(self) -> int:
        return self._wordCount
    
    def totalWordCount(self) -> int:
        return self._totalWordCount

    def hasFlag(self, flag: int) -> bool:
        return (self.flags & flag) == flag

    def setIcon(self, icon: QIcon):
        label: QLabel = self.children()[self.ICON]
        label.setPixmap(icon.pixmap(AppConfig.ICON_SIZE))

    def setTitle(self, text: str):
        if text == "":
            return
        self._title = text
        label: QLabel = self.children()[self.TITLE]
        label.setText(text)

    def setWordCount(self, count: int):
        self._wordCount = count
        
    def setTotalWordCount(self, count: int):
        self._totalWordCount = count
        label: QLabel = self.children()[self.WORD_COUNT]
        label.setText(str(count))

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeQString(self._uuid)
        sOut.writeQString(self._title)
        sOut.writeInt(self._wordCount)
        sOut.writeInt(self._totalWordCount)
        sOut.writeInt(self.flags)
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._uuid = sIn.readQString()
        self._title = sIn.readQString()
        self._wordCount = sIn.readInt()
        self._totalWordCount = sIn.readInt()
        self.flags = sIn.readInt()
        self.applyChanges()
        return sIn
