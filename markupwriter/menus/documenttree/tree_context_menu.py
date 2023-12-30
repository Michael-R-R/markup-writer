#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QWidget,
    QMenu,
)

from markupwriter.support.iconprovider import (
    Icon,
)

from . import (
    AddItemMenu,
)

class TreeContextMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.addItemMenu = AddItemMenu(self)
        self.addMenu(self.addItemMenu)

        self.moveToTrash = QAction(Icon.TRASH_FOLDER, "Move to trash", self)
        self.addAction(self.moveToTrash)