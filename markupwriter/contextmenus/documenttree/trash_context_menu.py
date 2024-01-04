#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.common.provider import (
    Icon,
)

from markupwriter.contextmenus import (
    BaseContextMenu,
)

class TrashContextMenu(BaseContextMenu):
    def __init__(self) -> None:
        super().__init__()

        self.emptyAction = QAction(Icon.TRASH_FOLDER, "Empty trash")

        self._menu.addAction(self.emptyAction)

    def preprocess(self, args: list[object] | None):
        isEmpty = args[0]

        self.emptyAction.setDisabled(isEmpty)

    def postprocess(self, args: list[object] | None):
        actions = self._menu.actions()
        for a in actions:
            a.setEnabled(True)
