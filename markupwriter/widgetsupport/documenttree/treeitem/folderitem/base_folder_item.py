#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from markupwriter.widgetsupport.documenttree.treeitem import (
    BaseTreeItem,
)

class BaseFolderItem(BaseTreeItem):
    def __init__(self,
                 title: str=None,
                 isDraggable: bool=False,
                 isEditable: bool=False,
                 item: QTreeWidgetItem=None,
                 parent: QWidget=None):
        super().__init__(title, isDraggable, isEditable, True, item, parent)

    def shallowcopy(self):
        raise NotImplementedError()
    
    def applyIcon(self):
        raise NotImplementedError()
    
    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
    