#!/usr/bin/python

from __future__ import annotations

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem,
    QWidget
)

from markupwriter.support.provider import(
    Icon,
)

from .base_folder_item import (
    ITEM_FLAG,
    BaseFolderItem
)

class CharsFolderItem(BaseFolderItem):
    def __init__(self,
                 title: str = None,
                 item: QTreeWidgetItem = None,
                 parent: QWidget = None):
        flags = ITEM_FLAG.none
        super().__init__(title, flags, item, parent)
        self.applyChanges()

    def shallowcopy(self):
        folder = CharsFolderItem(self.title,
                                self.item,
                                self.parentWidget())
        folder._flags = self._flags
        folder.applyIcon()
        return folder
    
    def applyIcon(self):
        self.icon = Icon.CHARACTERS_FOLDER

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn) 