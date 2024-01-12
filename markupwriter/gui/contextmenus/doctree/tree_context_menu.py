#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.gui.menus.doctree import (
    AddItemMenu,
)

from markupwriter.gui.contextmenus import (
    BaseContextMenu,
)


class TreeContextMenu(BaseContextMenu):
    def __init__(self, parent: QObject | None):
        super().__init__(parent)

        self.addItemMenu = AddItemMenu(None)

        self._menu.addMenu(self.addItemMenu)

    def preprocess(self, args: list[object] | None):
        pass

    def postprocess(self, args: list[object] | None):
        actions = self._menu.actions()
        for a in actions:
            a.setEnabled(True)
