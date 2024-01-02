#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from markupwriter.support.provider import(
    Icon,
)

from .base_file_item import (
    BaseFileItem,
)

class MiscFileItem(BaseFileItem):
    def __init__(self,
                 title: str = None,
                 content: str = None,
                 item: QTreeWidgetItem = None,
                 parent: QWidget = None):
        super().__init__(title, content, item, parent)
        self.applyChanges()

    def shallowcopy(self):
        myCopy = MiscFileItem(self.title,
                              self.content,
                              self.item,
                              self.parentWidget())
        myCopy._hash = self._hash
        myCopy._flags = self._flags
        myCopy.applyIcon()
        return myCopy
    
    def applyIcon(self):
        self.icon = Icon.MISC_FILE

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
