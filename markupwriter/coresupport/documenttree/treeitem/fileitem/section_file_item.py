#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QWidget,
)

from markupwriter.common.provider import (
    Icon,
)

from .base_file_item import (
    BaseFileItem,
)


class SectionFileItem(BaseFileItem):
    def __init__(self, title: str = None, parent: QWidget = None):
        super().__init__(title, parent)

    def shallowcopy(self, other=None):
        other: SectionFileItem = super().shallowcopy(SectionFileItem())
        other.applyChanges()
        return other

    def applyIcon(self):
        self.icon = Icon.SECTION_FILE

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return super().__rrshift__(sIn)
