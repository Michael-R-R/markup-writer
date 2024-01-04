#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.common.provider import (
    Icon,
)

from markupwriter.menus.documenttree import (
    AddItemMenu,
)

from markupwriter.contextmenus import (
    BaseContextMenu,
)

class ItemContextMenu(BaseContextMenu):
    def __init__(self) -> None:
        super().__init__()

        self.addItemMenu = AddItemMenu(None)
        self._menu.addMenu(self.addItemMenu)

        self.renameAction = QAction("Rename")
        self.toTrashAction = QAction(Icon.TRASH_FOLDER, "Move to trash")
        self.recoverAction = QAction(Icon.TRASH_FOLDER, "Recover")

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