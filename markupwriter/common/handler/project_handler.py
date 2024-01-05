#!/usr/bin/python

from typing import (
    TypeVar,
    Type,
)

from PyQt6.QtCore import (
    QDir,
)

from PyQt6.QtWidgets import (
    QFileDialog,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.dialogs.modal import (
    StrDialog,
)

class ProjectHandler(object):

    T = TypeVar("T")

    def onNewClicked() -> bool:
        projectName = StrDialog.run("Project name?",
                                    "Default",
                                    None)
        if projectName is None:
            return False

        projectDir = QFileDialog.getExistingDirectory(None,
                                                       "New Project",
                                                       "/home",
                                                       QFileDialog.Option.ShowDirsOnly |
                                                       QFileDialog.Option.DontResolveSymlinks)
        if projectDir == "":
            return False

        dir = QDir()
        if not dir.mkpath(projectDir + "/data/content/"):
            return False

        AppConfig.projectName = projectName
        AppConfig.projectDir = projectDir

        return True

    def onOpenClicked() -> str | None:
        projectFilePath = QFileDialog.getOpenFileName(None,
                                                      "Open Project",
                                                      "/home",
                                                      "Markup Writer Files (*.mwf)")
        # TODO implement
        
