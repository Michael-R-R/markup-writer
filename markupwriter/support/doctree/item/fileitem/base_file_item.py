#!/usr/bin/python

from __future__ import annotations

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QWidget,
)

from markupwriter.support.doctree.item import (
    ITEM_FLAG,
    BaseTreeItem,
)


class BaseFileItem(BaseTreeItem):
    def __init__(self, title: str = None, parent: QWidget = None):
        super().__init__(title, parent)

        self.flags += ITEM_FLAG.file
        self.flags += ITEM_FLAG.draggable
        self.flags += ITEM_FLAG.mutable

    def deepcopy(self, other=None):
        other: BaseFileItem = super().deepcopy(other)
        return other

    def applyIcon(self):
        raise NotImplementedError()

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
