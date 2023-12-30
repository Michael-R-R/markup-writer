#!/usr/bin/python

from __future__ import annotations
import uuid

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

class BaseFileItem(BaseTreeItem):
    def __init__(self,
                 title: str=None,
                 content: str=None,
                 isDraggable: bool=False,
                 isEditable: bool=False,
                 item: QTreeWidgetItem=None,
                 parent: QWidget=None):
        super().__init__(title, isDraggable, isEditable, False, item, parent)
        self._hash = str(uuid.uuid1())
        self._content = content

    def deepcopy(self):
        raise NotImplementedError()

    def applyIcon(self):
        raise NotImplementedError()
    
    def hash(self, value: str) -> str:
        self._hash = value
    hash = property(lambda self: self._hash, hash)

    def content(self, text: str):
        self._content = text
    content = property(lambda self: self._content, content)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeQString(self._hash)
        sOut.writeQString(self._content)
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._hash = sIn.readQString()
        self._content = sIn.readQString()
        return super().__rrshift__(sIn)