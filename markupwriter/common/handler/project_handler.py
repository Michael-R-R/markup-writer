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

from markupwriter.util import (
    Serialize,
)

class ProjectHandler(object):

    T = TypeVar("T")

    def onNewClicked():
        projectPath = QFileDialog.getExistingDirectory(None,
                                                       "New Project",
                                                       "/home",
                                                       QFileDialog.Option.ShowDirsOnly |
                                                       QFileDialog.Option.DontResolveSymlinks)
        if projectPath == "":
            return

        dir = QDir()
        if not dir.mkpath(projectPath + "/data/content/"):
            return

        AppConfig.projectPath = projectPath

    def onOpenClicked(type: Type[T]) -> T | None:
        # TODO implement properly
        return Serialize.read(type, "./resources/.tests/sample.mwf")

    def onSaveClicked(data):
        # TODO implmement properly
        Serialize.write("./resources/.tests/sample.mwf", data)