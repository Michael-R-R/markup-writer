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


class TimelineFolderItem(BaseFolderItem):
    def __init__(self, parent: QWidget = None):
        super().__init__("Timeline", parent)
        self.flags -= ITEM_FLAG.draggable
        self.flags -= ITEM_FLAG.mutable

    def deepcopy(self, other=None):
        other: TimelineFolderItem = super().deepcopy(TimelineFolderItem())
        other.applyChanges()
        return other

    def applyIcon(self):
        self.setIcon(Icon.TIMELINE_FOLDER)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
