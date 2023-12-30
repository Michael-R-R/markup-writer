#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from . import (
    BaseFileItem,
)

from markupwriter.support.iconprovider import(
    Icon,
)

class SectionFileItem(BaseFileItem):
    def __init__(self,
                 title: str = None,
                 content: str = None,
                 item: QTreeWidgetItem = None,
                 parent: QWidget = None):
        super().__init__(title, content, True, True, item, parent)
        self.applyChanges()

    def deepcopy(self):
        myCopy = SectionFileItem(self.title,
                              self.content,
                              self.item,
                              self.parentWidget())
        myCopy.hash = self.hash
        myCopy.applyIcon()
        return myCopy
    
    def applyIcon(self):
        self.icon = Icon.SECTION_FILE

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
