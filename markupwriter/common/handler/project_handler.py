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

    def createNewProject(parent: QWidget) -> cw.CentralWidget | None:
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

        AppConfig.projectName = name
        AppConfig.projectDir = path

        widget = cw.CentralWidget(parent)
        ProjectHandler.setActionStates(widget, True)
        ProjectHandler.createDefaultFolders(widget)

        Serialize.write(AppConfig.projectFilePath(), widget)

        return widget

    def openNewProject(parent: QWidget) -> cw.CentralWidget | None:
        path = QFileDialog.getOpenFileName(
            None, "Open Project", "/home", "Markup Writer Files (*.mwf)"
        )
        if path[0] == "":
            return None

        widget: cw.CentralWidget = Serialize.read(cw.CentralWidget, path[0])
        ProjectHandler.setActionStates(widget, True)

        info = QFileInfo(path[0])
        AppConfig.projectName = info.fileName()
        AppConfig.projectDir = info.canonicalPath()

        return widget

    def closeProject():
        AppConfig.projectName = None
        AppConfig.projectDir = None
        # TODO implement

    def createDefaultFolders(widget: cw.CentralWidget):
        tree = widget.treeView.tree
        tree.add(PlotFolderItem(), False)
        tree.add(TimelineFolderItem(), False)
        tree.add(CharsFolderItem(), False)
        tree.add(LocFolderItem(), False)
        tree.add(ObjFolderItem(), False)
        tree.add(TrashFolderItem(), False)
