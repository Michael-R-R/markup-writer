#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QWidget,
    QMenu,
)

from markupwriter.common.provider import (
    Icon,
)


class ItemMenu(QMenu):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        self.setTitle("Add Item")

        self.novelAction = QAction(Icon.NOVEL_FOLDER, "Novel")
        self.miscFolderAction = QAction(Icon.MISC_FOLDER, "Misc.")

        self.titleAction = QAction(Icon.TITLE_FILE, "Title")
        self.chapterAction = QAction(Icon.CHAPTER_FILE, "Chapter")
        self.sceneAction = QAction(Icon.SCENE_FILE, "Scene")
        self.sectionAction = QAction(Icon.SECTION_FILE, "Section")
        self.miscFileAction = QAction(Icon.MISC_FILE, "Misc.")

        self._folderMenu = QMenu("Folder", self)
        self._folderMenu.addAction(self.novelAction)
        self._folderMenu.addAction(self.miscFolderAction)
        self.addMenu(self._folderMenu)

        self._fileMenu = QMenu("File", self)
        self._fileMenu.addAction(self.titleAction)
        self._fileMenu.addAction(self.chapterAction)
        self._fileMenu.addAction(self.sceneAction)
        self._fileMenu.addAction(self.sectionAction)
        self._fileMenu.addAction(self.miscFileAction)
        self.addMenu(self._fileMenu)
