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

from markupwriter.gui.dialogs.modal import (
    StrDialog,
)

from markupwriter.common.util import (
    Serialize,
)

from markupwriter.support.doctree.item import (
    PlotFolderItem,
    TimelineFolderItem,
    CharsFolderItem,
    LocFolderItem,
    ObjFolderItem,
    TrashFolderItem,
)

import markupwriter.mvc.controller.core as cw


class ProjectHandler(object):
    def setMenuBarActionStates(controller: cw.MainMenuBarController, isEnabled: bool):
        # --- File menu --- #
        fileMenu = controller.view.filemenu
        fileMenu.saveAction.setEnabled(isEnabled)
        fileMenu.saveAsAction.setEnabled(isEnabled)
        fileMenu.closeAction.setEnabled(isEnabled)

    def setCentralActionStates(controller: cw.CentralWidgetController, isEnabled: bool):
        # --- Tree bar --- #
        treeBar = controller.model.docTreeController.view.treebar
        treeBar.navUpAction.setEnabled(isEnabled)
        treeBar.navDownAction.setEnabled(isEnabled)
        treeBar.addItemAction.setEnabled(isEnabled)

        # --- Tree --- #
        tree = controller.model.docTreeController.view.treewidget
        tree.treeContextMenu.addItemMenu.setEnabled(isEnabled)

    def createProject(parent: QWidget) -> cw.CentralWidgetController | None:
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

        widget = cw.CentralWidgetController(parent)
        ProjectHandler.setCentralActionStates(widget, True)
        ProjectHandler.createRootFolders(widget)

        AppConfig.projectName = name
        AppConfig.projectDir = path

        Serialize.write(AppConfig.projectFilePath(), widget)

        return widget

    def openProject(parent: QWidget) -> cw.CentralWidgetController | None:
        path = QFileDialog.getOpenFileName(
            None, "Open Project", "/home", "Markup Writer Files (*.mwf)"
        )
        if path[0] == "":
            return None

        widget = Serialize.read(cw.CentralWidgetController, path[0])
        if widget is None:
            return None

        ProjectHandler.setCentralActionStates(widget, True)

        info = QFileInfo(path[0])
        AppConfig.projectName = info.fileName()
        AppConfig.projectDir = info.canonicalPath()

        return widget

    def closeProject(parent: QWidget):
        AppConfig.projectName = None
        AppConfig.projectDir = None

        widget = cw.CentralWidgetController(parent)
        ProjectHandler.setCentralActionStates(widget, False)

        return widget

    def createRootFolders(controller: cw.CentralWidgetController):
        tree = controller.model.docTreeController.view.treewidget
        tree.add(PlotFolderItem())
        tree.add(TimelineFolderItem())
        tree.add(CharsFolderItem())
        tree.add(LocFolderItem())
        tree.add(ObjFolderItem())
        tree.add(TrashFolderItem())
        
    # TODO complete class overhaul
