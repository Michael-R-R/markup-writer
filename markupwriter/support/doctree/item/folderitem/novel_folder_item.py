#!/usr/bin/python

from __future__ import annotations

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import QWidget

from markupwriter.common.provider import (
    Icon,
)

from .base_folder_item import (
    ITEM_FLAG,
    BaseFolderItem,
)


class NovelFolderItem(BaseFolderItem):
    def __init__(self, title: str = None, parent: QWidget = None):
        super().__init__(title, parent)

        self.flags -= ITEM_FLAG.draggable

        label: QWidget = self.children()[self.TITLE]
        font = label.font()
        font.setUnderline(True)
        label.setFont(font)

    def deepcopy(self, other=None):
        other: NovelFolderItem = super().deepcopy(NovelFolderItem())
        other.applyChanges()
        return other

    def applyIcon(self):
        self.setIcon(Icon.NOVEL_FOLDER)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
