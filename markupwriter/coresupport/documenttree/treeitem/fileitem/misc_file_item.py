#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from markupwriter.common.provider import(
    Icon,
)

from .base_file_item import (
    BaseFileItem,
)

class MiscFileItem(BaseFileItem):
    def __init__(self,
                 title: str=None,
                 item: QTreeWidgetItem=None,
                 parent: QWidget=None):
        super().__init__(title, item, parent)

    def shallowcopy(self, other = None):
        other: MiscFileItem = super().shallowcopy(MiscFileItem())
        other.applyChanges()
        return other
    
    def applyIcon(self):
        self.icon = Icon.MISC_FILE

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
