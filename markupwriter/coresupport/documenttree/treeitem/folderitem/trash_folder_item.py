#!/usr/bin/python

from __future__ import annotations

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem,
    QWidget
)

from markupwriter.common.provider import(
    Icon,
)

from .base_folder_item import (
    ITEM_FLAG,
    BaseFolderItem,
)

class TrashFolderItem(BaseFolderItem):
    def __init__(self,
                 title: str = None,
                 item: QTreeWidgetItem = None,
                 parent: QWidget = None):
        super().__init__(title, item, parent)
        self._flags -= ITEM_FLAG.draggable
        self._flags -= ITEM_FLAG.mutable

    def shallowcopy(self, other = None):
        other: TrashFolderItem = super().shallowcopy(TrashFolderItem())
        other.applyChanges()
        return other
    
    def applyIcon(self):
        self.icon = Icon.TRASH_FOLDER

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn) 