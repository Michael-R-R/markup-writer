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
    BaseTreeItem,
    RootFolderItem,
    MiscFolderItem,
    TitleFileItem,
    ChapterFileItem,
    SceneFileItem,
    SectionFileItem,
    MiscFileItem,
)

from markupwriter.support.provider import (
    Icon,
)

from markupwriter.dialogs.modal import (
    StrDialog,
)

class AddItemMenu(QMenu):
    itemCreated = pyqtSignal(BaseTreeItem)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        self.setTitle("Add Item")

        self._folderMenu = QMenu("Folder", self)
        self.setupFolderAction(QAction(Icon.ROOT_FOLDER, "Root", self._folderMenu), RootFolderItem)
        self.setupFolderAction(QAction(Icon.MISC_FOLDER, "Miscellaneous", self._folderMenu), MiscFolderItem)
        self.addMenu(self._folderMenu)

        self._fileMenu = QMenu("File", self)
        self.setupFileAction(QAction(Icon.TITLE_FILE, "Title", self._fileMenu), TitleFileItem)
        self.setupFileAction(QAction(Icon.CHAPTER_FILE, "Chapter", self._fileMenu), ChapterFileItem)
        self.setupFileAction(QAction(Icon.SCENE_FILE, "Scene", self._fileMenu), SceneFileItem)
        self.setupFileAction(QAction(Icon.SECTION_FILE, "Section", self._fileMenu), SectionFileItem)
        self.setupFileAction(QAction(Icon.MISC_FILE, "Miscellaneous", self._fileMenu), MiscFileItem)
        self.addMenu(self._fileMenu)

    def setupFolderAction(self, action: QAction, folderClass):
        self._folderMenu.addAction(action)
        action.triggered.connect(lambda: self.onFolderCreate(folderClass))

    def setupFileAction(self, action: QAction, fileClass):
        self._fileMenu.addAction(action)
        action.triggered.connect(lambda: self.createFile(fileClass))

    def onFolderCreate(self, folderClass):
        text = StrDialog.run("Enter Name", "Folder", None)
        if text is None:
            return

        folder = folderClass(text, QTreeWidgetItem())
        self.itemCreated.emit(folder)
    
    def createFile(self, fileClass):
        text = StrDialog.run("Enter Name", "File", None)
        if text is None:
            return
        
        file = fileClass(text, "", QTreeWidgetItem())
        self.itemCreated.emit(file)
