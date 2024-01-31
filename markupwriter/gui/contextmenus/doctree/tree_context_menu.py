#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
)

from markupwriter.gui.menus.doctree import (
    AddItemMenu,
)

from markupwriter.gui.contextmenus import (
    BaseContextMenu,
)


class TreeContextMenu(BaseContextMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.addItemMenu = AddItemMenu(parent)

        self._menu.addMenu(self.addItemMenu)
        
        self.addItemMenu.setEnabled(False)

    def preprocess(self, args: list[object] | None):
        pass

    def postprocess(self, args: list[object] | None):
        actions = self._menu.actions()
        for a in actions:
            a.setEnabled(True)
