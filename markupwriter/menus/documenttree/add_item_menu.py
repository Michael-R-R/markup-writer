#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSignal,
)

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QWidget,
    QMenu,
    QTreeWidgetItem,
)

from markupwriter.widgetsupport.documenttree.treeitem import (
    FOLDER, FolderTreeItem,
    FILE, FileTreeItem,
    BaseTreeItem,
)

from markupwriter.support.iconprovider import (
    Icon,
)

from markupwriter.dialogs.modal import (
    StrDialog,
)

class AddItemMenu(QMenu):
    itemCreated = pyqtSignal(BaseTreeItem)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self._folderMenu = QMenu("Folder", self)
        self.setupFolderAction(QAction(Icon.ROOT_FOLDER, "Root", self._folderMenu), FOLDER.root)
        self.setupFolderAction(QAction(Icon.MISC_FOLDER, "Miscellaneous", self._folderMenu), FOLDER.misc)
        self.addMenu(self._folderMenu)

        self._fileMenu = QMenu("File", self)
        self.setupFileAction(QAction(Icon.TITLE_FILE, "Title", self._fileMenu), FILE.title)
        self.setupFileAction(QAction(Icon.CHAPTER_FILE, "Chapter", self._fileMenu), FILE.chapter)
        self.setupFileAction(QAction(Icon.SCENE_FILE, "Scene", self._fileMenu), FILE.scene)
        self.setupFileAction(QAction(Icon.SECTION_FILE, "Section", self._fileMenu), FILE.section)
        self.setupFileAction(QAction(Icon.MISC_FILE, "Miscellaneous", self._fileMenu), FILE.misc)
        self.addMenu(self._fileMenu)

    def setupFolderAction(self, action: QAction, folderType: FOLDER):
        self._folderMenu.addAction(action)
        action.triggered.connect(lambda: self.createFolder(folderType))

    def setupFileAction(self, action: QAction, fileType: FILE):
        self._fileMenu.addAction(action)
        action.triggered.connect(lambda: self.createFile(fileType))

    def createFolder(self, folderType: FOLDER):
        result: (str, bool) = StrDialog.run("Enter Name", None)
        if not result[1]:
            return

        folder = FolderTreeItem(folderType, result[0], QTreeWidgetItem())
        self.itemCreated.emit(folder)
    
    def createFile(self, fileType: FILE):
        result: (str, bool) = StrDialog.run("Enter Name", None)
        if not result[1]:
            return
        
        file = FileTreeItem(fileType, result[0], "", QTreeWidgetItem())
        self.itemCreated.emit(file)
