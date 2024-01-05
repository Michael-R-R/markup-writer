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
        projName = StrDialog.run("Project name?",
                                "Default",
                                None)
        if projName is None:
            return False

        dirPath = QFileDialog.getExistingDirectory(None,
                                                   "New Project",
                                                   "/home",
                                                    QFileDialog.Option.ShowDirsOnly |
                                                    QFileDialog.Option.DontResolveSymlinks)
        if dirPath == "":
            return False

        dir = QDir()
        if not dir.mkpath(dir + "/data/content/"):
            return False

        AppConfig.projectName = projName
        AppConfig.projectDir = dirPath

        return True

    def onOpenClicked() -> str | None:
        filePath = QFileDialog.getOpenFileName(None,
                                               "Open Project",
                                               "/home",
                                               "Markup Writer Files (*.mwf)")
        if filePath[0] == "":
            return None
        
        return filePath[0]
        
        
