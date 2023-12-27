#!/usr/bin/python

from enum import Enum, auto

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from .base_tree_item import BaseTreeItem

from markupwriter.support.iconprovider import(
    Icon,
)

class FOLDER(Enum):
    root = auto(),
    plot = auto(),
    timeline = auto(),
    characters = auto(),
    locations = auto(),
    objects = auto(),
    misc = auto(),

class FolderTreeItem(BaseTreeItem):
    def __init__(self,
                 type: FOLDER,
                 title: str, path: str,
                 item: QTreeWidgetItem,
                 parent: QWidget):
        super().__init__(title, path, item, parent)
        self._type = type

        self.applyIcon()

    def applyIcon(self):
        match self._type:
            case FOLDER.root:
                self.setIcon(Icon.ROOT_FOLDER)
            case FOLDER.plot:
                self.setIcon(Icon.PLOT_FOLDER)
            case FOLDER.timeline:
                self.setIcon(Icon.TIMELINE_FOLDER)
            case FOLDER.characters:
                self.setIcon(Icon.CHARACTERS_FOLDER)
            case FOLDER.locations:
                self.setIcon(Icon.LOCATIONS_FOLDER)
            case FOLDER.objects:
                self.setIcon(Icon.OBJECTS_FOLDER)
            case FOLDER.misc:
                self.setIcon(Icon.MISC_FILE)
