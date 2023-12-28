#!/usr/bin/python

from enum import auto, Enum

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem, 
    QWidget,
)

from .base_tree_item import (
    BaseTreeItem,
)

from markupwriter.support.iconprovider import(
    Icon,
)

class FOLDER(Enum):
    root = 0
    plot = auto()
    timeline = auto()
    characters = auto()
    locations = auto()
    objects = auto()
    misc = auto()

class FolderTreeItem(BaseTreeItem):
    def __init__(self,
                 folderType: FOLDER,
                 path: str,
                 title: str,
                 item: QTreeWidgetItem,
                 parent: QWidget):
        super().__init__(path, title, item, True, parent)
        self._folderType = folderType

        self.applyIcon()

    def folderType(self, folderType: FOLDER):
        self._folderType = folderType
        self.applyIcon()
    folderType = property(lambda self: self._folderType, folderType)

    def applyIcon(self):
        match self._folderType:
            case FOLDER.root:
                self.icon = Icon.ROOT_FOLDER
            case FOLDER.plot:
                self.icon = Icon.PLOT_FOLDER
            case FOLDER.timeline:
                self.icon = Icon.TIMELINE_FOLDER
            case FOLDER.characters:
                self.icon = Icon.CHARACTERS_FOLDER
            case FOLDER.locations:
                self.icon = Icon.LOCATIONS_FOLDER
            case FOLDER.objects:
                self.icon = Icon.OBJECTS_FOLDER
            case FOLDER.misc:
                self.icon = Icon.MISC_FILE
    
    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeInt(self._folderType.value)
        return super().__rlshift__(sOut)

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._folderType = FOLDER(sIn.readInt())
        return super().__rrshift__(sIn)
    