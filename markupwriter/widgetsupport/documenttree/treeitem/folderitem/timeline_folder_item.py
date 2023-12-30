#!/usr/bin/python

from __future__ import annotations

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem,
    QWidget
)

from . import (
    BaseFolderItem
)

from markupwriter.support.iconprovider import(
    Icon,
)

class TimelineFolderItem(BaseFolderItem):
    def __init__(self,
                 title: str = None,
                 item: QTreeWidgetItem = None,
                 parent: QWidget = None):
        super().__init__(title, False, False, item, parent)
        self.applyChanges()

    def deepcopy(self):
        folder = TimelineFolderItem(self.title,
                                self.item,
                                self.parentWidget())
        folder.applyIcon()
        return folder
    
    def applyIcon(self):
        self.icon = Icon.TIMELINE_FOLDER

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn) 