#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
)

from markupwriter.gui.menus.doctree import (
    ItemMenu,
)

from markupwriter.gui.contextmenus import (
    BaseContextMenu,
)


class TreeContextMenu(BaseContextMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.itemMenu = ItemMenu(parent)
        self.itemMenu.setEnabled(False)

        self._menu.addMenu(self.itemMenu)

    def preprocess(self, args: list[object] | None):
        pass

    def postprocess(self, args: list[object] | None):
        actions = self._menu.actions()
        for a in actions:
            a.setEnabled(True)
