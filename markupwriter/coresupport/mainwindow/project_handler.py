#!/usr/bin/python

import re

from PyQt6.QtCore import (
    QDir,
    QFileInfo,
)

from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.dialogs.modal import (
    StrDialog,
)

from markupwriter.util import (
    Serialize,
)

from markupwriter.coresupport.documenttree.treeitem import (
    PlotFolderItem,
    TimelineFolderItem,
    CharsFolderItem,
    LocFolderItem,
    ObjFolderItem,
    TrashFolderItem,
)

import markupwriter.core.central_widget as cw


class ProjectHandler(object):
    def setActionStates(widget: cw.CentralWidget, isEnabled: bool):
        # --- File menu --- #
        fileMenu = widget.menuBar.fileMenu
        fileMenu.saveAction.setEnabled(isEnabled)
        fileMenu.saveAsAction.setEnabled(isEnabled)
        fileMenu.closeAction.setEnabled(isEnabled)

        # --- Tree bar --- #
        treeBar = widget.treeView.treeBar
        treeBar.navUpAction.setEnabled(isEnabled)
        treeBar.navDownAction.setEnabled(isEnabled)
        treeBar.addItemAction.setEnabled(isEnabled)

        # --- Tree --- #
        tree = widget.treeView.tree
        tree.helper.treeContextMenu.addItemMenu.setEnabled(isEnabled)

    def createProject(parent: QWidget) -> cw.CentralWidget | None:
        name: str = StrDialog.run("Project name?", "Default", None)
        if name is None:
            return None
        name = name.strip()
        found = re.search(r"^[a-zA-Z0-9_\-\s]+$", name)
        if found is None:
            return None
        name += AppConfig.APP_EXTENSION

        path = QFileDialog.getExistingDirectory(
            None,
            "New Project",
            "/home",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if path == "":
            return None

        dir = QDir()
        if not dir.mkpath("{}/data/content/".format(path)):
            return None

        widget = cw.CentralWidget(parent)
        ProjectHandler.setActionStates(widget, True)
        ProjectHandler.createRootFolders(widget)

        AppConfig.projectName = name
        AppConfig.projectDir = path

        Serialize.write(AppConfig.projectFilePath(), widget)

        return widget

    def openProject(parent: QWidget) -> cw.CentralWidget | None:
        path = QFileDialog.getOpenFileName(
            None, "Open Project", "/home", "Markup Writer Files (*.mwf)"
        )
        if path[0] == "":
            return None

        widget: cw.CentralWidget = Serialize.read(cw.CentralWidget, path[0])
        if widget is None:
            return None
        
        ProjectHandler.setActionStates(widget, True)

        info = QFileInfo(path[0])
        AppConfig.projectName = info.fileName()
        AppConfig.projectDir = info.canonicalPath()

        return widget

    def closeProject(parent: QWidget):
        AppConfig.projectName = None
        AppConfig.projectDir = None
        
        widget = cw.CentralWidget(parent)
        ProjectHandler.setActionStates(widget, False)

        return widget

    def createRootFolders(widget: cw.CentralWidget):
        tree = widget.treeView.tree
        tree.add(PlotFolderItem(), False)
        tree.add(TimelineFolderItem(), False)
        tree.add(CharsFolderItem(), False)
        tree.add(LocFolderItem(), False)
        tree.add(ObjFolderItem(), False)
        tree.add(TrashFolderItem(), False)
