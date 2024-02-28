#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
)

from markupwriter.config import HotkeyConfig


class ViewMainMenu(QMenu):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__("View", parent)
        
        self.treeAction = QAction("Document Tree", self)
        self.treeAction.setShortcut(HotkeyConfig.viewDocTree)
    
        self.editorAction = QAction("Document Editor", self)
        self.editorAction.setShortcut(HotkeyConfig.viewDocEditor)
        
        self.previewAction = QAction("Document Preview", self)
        self.previewAction.setShortcut(HotkeyConfig.viewDocPreview)
        
        self.telecopeAction = QAction("Telescope", self)
        self.telecopeAction.setShortcut(HotkeyConfig.viewTelescope)
        
        self.addAction(self.treeAction)
        self.addAction(self.editorAction)
        self.addAction(self.previewAction)
        self.addAction(self.telecopeAction)
