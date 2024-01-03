#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
)

from PyQt6.QtGui import (
    QAction,
    QCursor,
)

from markupwriter.support.provider import (
    Icon,
)

from markupwriter.coresupport.documenttree.treeitem import (
    BaseTreeItem,
)

from markupwriter.menus.documenttree import (
    AddItemMenu,
)

class ItemAddAction(QAction):
    itemCreated = pyqtSignal(BaseTreeItem)

    def __init__(self, parent: QObject):
        super().__init__(Icon.ADD_ITEM, "Add item", parent)

        self._addItemMenu = AddItemMenu(None)
        self._addItemMenu.itemCreated.connect(lambda item: self.itemCreated.emit(item))
        self.setMenu(self._addItemMenu)

        self.triggered.connect(lambda: self._addItemMenu.popup(QCursor.pos()))