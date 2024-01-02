#!/usr/bin/python

from PyQt6.QtCore import (
    QPoint,
)

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QMenu,
)

from markupwriter.support.provider import (
    Icon,
)

from markupwriter.menus.documenttree import (
    AddItemMenu,
)

class TreeContextMenu(object):
    def __init__(self):
        self.addItemMenu = AddItemMenu(None)

        # empty click menu
        self.emptyClickMenu = QMenu()
        self.emptyClickMenu.addMenu(self.addItemMenu)

        # base item menu
        self.baseItemMenu = QMenu()
        self.baseItemMenu.addMenu(self.addItemMenu)

        self.renameItem = QAction("Rename")
        self.moveToTrash = QAction(Icon.TRASH_FOLDER, "Move to trash")
        self.baseItemMenu.addAction(self.renameItem)
        self.baseItemMenu.addAction(self.moveToTrash)

        # trash folder menu
        self.trashFolderMenu = QMenu()
        self.emptyTrash = QAction(Icon.TRASH_FOLDER, "Empty trash")
        self.trashFolderMenu.addAction(self.emptyTrash)

    def onEmptyClickMenu(self, pos: QPoint):
        self.emptyClickMenu.exec(pos)

    def onBaseItemMenu(self, pos: QPoint):
        self.baseItemMenu.exec(pos)

    def onTrashFolderMenu(self, pos: QPoint):
        self.trashFolderMenu.exec(pos)