#!/usr/bin/python

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

from markupwriter.gui.menus.doctree import (
    ItemMenu,
)


class ItemMenuAction(QAction):
    def __init__(self, parent: QWidget):
        super().__init__(Icon.ADD_ITEM, "Add item", parent)

        self.itemMenu = ItemMenu(parent)
        
        self.setMenu(self.itemMenu)
        
        self.triggered.connect(lambda: self.itemMenu.popup(QCursor.pos()))
