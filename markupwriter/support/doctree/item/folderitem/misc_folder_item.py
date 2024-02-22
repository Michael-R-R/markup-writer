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
    BaseFolderItem,
)


class MiscFolderItem(BaseFolderItem):
    def __init__(
        self, title: str = None, parent: QWidget = None
    ):
        super().__init__(title, parent)

    def deepcopy(self, other=None):
        other: MiscFolderItem = super().deepcopy(MiscFolderItem())
        other.applyChanges()
        return other

    def applyIcon(self):
        self.setIcon(Icon.MISC_FOLDER)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
