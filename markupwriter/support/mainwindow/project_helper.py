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
    YesNoDialog,
)


class ProjectHelper(object):
    def mkProjectDir(parent: QWidget | None) -> (str | None, str | None):
        name: str = StrDialog.run("Project name?", "Default", parent)
        if name is None:
            return None, None
        name = name.strip()
        found = re.search(r"^[a-zA-Z0-9_\-\s]+$", name)
        if found is None:
            return None, None
        name += AppConfig.APP_EXTENSION

        path = QFileDialog.getExistingDirectory(
            parent,
            "New Project",
            "/home",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if path == "":
            return None, None

        dir = QDir()
        if not dir.mkpath("{}/data/content/".format(path)):
            return None, None

        return name, path

    def openProjectPath(parent: QWidget) -> (str | None, str | None):
        path = QFileDialog.getOpenFileName(
            parent, "Open Project", "/home", "Markup Writer Files (*.mwf)"
        )
        if path[0] == "":
            return None, None

        info = QFileInfo(path[0])
        
        return info.fileName(), info.canonicalPath()

    def askToSave(parent: QWidget | None) -> bool:
        return YesNoDialog.run("Save current project?", parent)

    def askToSaveClose(parent: QWidget | None) -> bool:
        return YesNoDialog.run("Save and close current project?", parent)

    def askToExit(parent: QWidget | None) -> bool:
        return YesNoDialog.run("Exit application?", parent)
    