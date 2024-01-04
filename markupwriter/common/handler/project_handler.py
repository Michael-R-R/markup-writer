#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
)

from PyQt6.QtWidgets import (
    QFileDialog,
)

from markupwriter.config import (
    AppConfig,
)

class ProjectHandler(object):

    def onNewProjectClicked(self):
        # Open file dialog and get working folder path
        projectPath = QFileDialog.getExistingDirectory(None,
                                                       "New Project",
                                                       None,
                                                       QFileDialog.Option.ShowDirsOnly |
                                                       QFileDialog.Option.DontResolveSymlinks)
        if projectPath == "":
            return
        
        print(projectPath)

        # Create 'data>documents' folder inside working folder
        dir = QDir()
        if not dir.mkpath(projectPath + "/data/content/"):
            return

        # Set AppConfig project path
        AppConfig.projectPath = projectPath