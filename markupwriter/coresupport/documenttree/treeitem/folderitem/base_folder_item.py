#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from markupwriter.coresupport.documenttree.treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
)

class BaseFolderItem(BaseTreeItem):
    def __init__(self,
                 title: str=None,
                 item: QTreeWidgetItem=None,
                 parent: QWidget=None):
        super().__init__(title, item, parent)

        self._flags += ITEM_FLAG.folder
        self._flags += ITEM_FLAG.draggable
        self._flags += ITEM_FLAG.mutable

    def shallowcopy(self, other = None):
        other: BaseFolderItem = super().shallowcopy(other)
        return other
    
    def applyIcon(self):
        raise NotImplementedError()
    
    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
    