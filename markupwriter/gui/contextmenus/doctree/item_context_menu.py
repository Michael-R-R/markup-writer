#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
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

from markupwriter.gui.contextmenus import (
    BaseContextMenu,
)


class ItemContextMenu(BaseContextMenu):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.itemMenu = ItemMenu(parent)
        self._menu.addMenu(self.itemMenu)

        self.previewAction = QAction("Preview", self)
        self.renameAction = QAction("Rename", self)
        self.toTrashAction = QAction(Icon.TRASH_FOLDER, "Move to trash", self)
        self.recoverAction = QAction(Icon.TRASH_FOLDER, "Recover", self)

        self._menu.addAction(self.previewAction)
        self._menu.addAction(self.renameAction)
        self._menu.addAction(self.toTrashAction)
        self._menu.addAction(self.recoverAction)

    def preprocess(self, args: list[object] | None):
        isFile: bool = args[0]
        inTrash: bool = args[1]
        isMutable: bool = args[2]

        self.previewAction.setEnabled(isFile)
        self.renameAction.setEnabled(isMutable)
        self.toTrashAction.setEnabled((not inTrash) and isMutable)
        self.recoverAction.setEnabled(inTrash)

    def postprocess(self, args: list[object] | None):
        actions = self._menu.actions()
        for a in actions:
            a.setEnabled(True)
