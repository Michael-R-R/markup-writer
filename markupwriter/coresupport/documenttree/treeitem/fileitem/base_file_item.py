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

from markupwriter.coresupport.documenttree.treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
)

class BaseFileItem(BaseTreeItem):
    def __init__(self,
                 title: str=None,
                 content: str=None,
                 item: QTreeWidgetItem=None,
                 parent: QWidget=None):
        super().__init__(title, item, parent)
        self._flags += ITEM_FLAG.file
        self._docUUID = str(uuid.uuid1())
        self._content = content

    def shallowcopy(self):
        raise NotImplementedError()

    def applyIcon(self):
        raise NotImplementedError()
    
    def docUUID(self):
        return self._docUUID

    def content(self, text: str):
        self._content = text
    content = property(lambda self: self._content, content)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeQString(self._docUUID)
        sOut.writeQString(self._content)
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._docUUID = sIn.readQString()
        self._content = sIn.readQString()
        return super().__rrshift__(sIn)