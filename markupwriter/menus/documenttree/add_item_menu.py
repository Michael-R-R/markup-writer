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

from markupwriter.common.provider import (
    Icon,
)

from markupwriter.dialogs.modal import (
    StrDialog,
)

from markupwriter.coresupport.documenttree.treeitem import (
    BaseTreeItem,
    NovelFolderItem,
    MiscFolderItem,
    TitleFileItem,
    ChapterFileItem,
    SceneFileItem,
    SectionFileItem,
    MiscFileItem,
)

class AddItemMenu(QMenu):
    itemCreated = pyqtSignal(BaseTreeItem)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        self.setTitle("Add Item")

        self._folderMenu = QMenu("Folder", self)
        self.setupFolderAction(QAction(Icon.NOVEL_FOLDER, "Novel", self._folderMenu), NovelFolderItem)
        self.setupFolderAction(QAction(Icon.MISC_FOLDER, "Misc.", self._folderMenu), MiscFolderItem)
        self.addMenu(self._folderMenu)

        self._fileMenu = QMenu("File", self)
        self.setupFileAction(QAction(Icon.TITLE_FILE, "Title", self._fileMenu), TitleFileItem)
        self.setupFileAction(QAction(Icon.CHAPTER_FILE, "Chapter", self._fileMenu), ChapterFileItem)
        self.setupFileAction(QAction(Icon.SCENE_FILE, "Scene", self._fileMenu), SceneFileItem)
        self.setupFileAction(QAction(Icon.SECTION_FILE, "Section", self._fileMenu), SectionFileItem)
        self.setupFileAction(QAction(Icon.MISC_FILE, "Misc.", self._fileMenu), MiscFileItem)
        self.addMenu(self._fileMenu)

    def setupFolderAction(self, action: QAction, folderClass):
        self._folderMenu.addAction(action)
        action.triggered.connect(lambda: self.onFolderCreate(action.text(), folderClass))

    def setupFileAction(self, action: QAction, fileClass):
        self._fileMenu.addAction(action)
        action.triggered.connect(lambda: self.createFile(action.text(), fileClass))

    def onFolderCreate(self, label: str, folderClass):
        text = StrDialog.run("Enter Name", label, None)
        if text is None:
            return

        folder = folderClass(text, QTreeWidgetItem())
        self.itemCreated.emit(folder)
    
    def createFile(self, label: str, fileClass):
        text = StrDialog.run("Enter Name", label, None)
        if text is None:
            return
        
        file = fileClass(text, QTreeWidgetItem())
        self.itemCreated.emit(file)
