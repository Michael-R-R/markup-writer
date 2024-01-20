#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.common.provider import (
    Icon,
)

from markupwriter.gui.menus.doctree import (
    AddItemMenu,
)

from markupwriter.gui.contextmenus import (
    BaseContextMenu,
)


class ItemContextMenu(BaseContextMenu):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.addItemMenu = AddItemMenu(None)
        self._menu.addMenu(self.addItemMenu)

        self.renameAction = QAction("Rename", self)
        self.toTrashAction = QAction(Icon.TRASH_FOLDER, "Move to trash", self)
        self.recoverAction = QAction(Icon.TRASH_FOLDER, "Recover", self)

        self._menu.addAction(self.renameAction)
        self._menu.addAction(self.toTrashAction)
        self._menu.addAction(self.recoverAction)

    def preprocess(self, args: list[object] | None):
        inTrash: bool = args[0]
        isMutable: bool = args[1]

        self.recoverAction.setEnabled(inTrash)
        self.renameAction.setEnabled(isMutable)
        self.toTrashAction.setEnabled((not inTrash) and isMutable)

    def postprocess(self, args: list[object] | None):
        actions = self._menu.actions()
        for a in actions:
            a.setEnabled(True)
