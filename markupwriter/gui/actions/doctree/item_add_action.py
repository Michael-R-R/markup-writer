#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSignal,
)

from PyQt6.QtGui import (
    QAction,
    QCursor,
)

from PyQt6.QtWidgets import (
    QWidget,
)

from markupwriter.common.provider import (
    Icon,
)

from markupwriter.support.doctree.item import (
    BaseTreeItem,
)

from markupwriter.gui.menus.doctree import (
    AddItemMenu,
)


class ItemAddAction(QAction):
    itemCreated = pyqtSignal(BaseTreeItem)

    def __init__(self, parent: QWidget):
        super().__init__(Icon.ADD_ITEM, "Add item", parent)

        self._addItemMenu = AddItemMenu(parent)
        self._addItemMenu.itemCreated.connect(lambda item: self.itemCreated.emit(item))
        self.setMenu(self._addItemMenu)

        self.triggered.connect(lambda: self._addItemMenu.popup(QCursor.pos()))
