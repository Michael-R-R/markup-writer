#!/usr/bin/python

import re

from PyQt6.QtCore import (
    QDir,
    QFileInfo,
)

from PyQt6.QtGui import (
    QCloseEvent,
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QApplication,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.dialogs.modal import (
    YesNoDialog,
    StrDialog,
)

from markupwriter.util import (
    Serialize,
)

from .central_widget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.mainWidget = CentralWidget(self)
        self.setMenuBar(self.mainWidget.menuBar)
        self.setCentralWidget(self.mainWidget)
        self.setStatusBar(self.mainWidget.statusBar)
        self.setupConnections()

        self.setWindowTitle(AppConfig.fullWindowTitle())
        self.resize(AppConfig.mainWindowSize)
        self.setContentsMargins(0, 0, 0, 0)

    def setupConnections(self):
        # --- Main Window --- #
        menuBar = self.mainWidget.menuBar
        fileMenu = menuBar.fileMenu
        fileMenu.newAction.triggered.connect(self._onNewClicked)
        fileMenu.openAction.triggered.connect(self._onOpenClicked)
        fileMenu.saveAction.triggered.connect(self._onSaveClicked)
        fileMenu.saveAsAction.triggered.connect(self._onSaveAsClicked)
        fileMenu.closeAction.triggered.connect(self._onCloseClicked)
        fileMenu.exitAction.triggered.connect(self._onExitClicked)

    def reset(self):
        AppConfig.projectName = None
        AppConfig.projectDir = None

        self.mainWidget = CentralWidget(self)
        self.setMenuBar(self.mainWidget.menuBar)
        self.setCentralWidget(self.mainWidget)
        self.setStatusBar(self.mainWidget.statusBar)
        self.setupConnections()
        self.setWindowTitle(AppConfig.fullWindowTitle())
        self.resize(AppConfig.mainWindowSize)

    def _onNewClicked(self):
        self._createProject("New Project", True)

    def _onOpenClicked(self):
        if not self._shouldClose():
            return

        filePath = QFileDialog.getOpenFileName(
            None, "Open Project", "/home", "Markup Writer Files (*.mwf)"
        )
        if filePath[0] == "":
            return None

        widget: CentralWidget = Serialize.read(CentralWidget, filePath[0])
        self.mainWidget = widget
        self.setMenuBar(self.mainWidget.menuBar)
        self.setCentralWidget(self.mainWidget)
        self.setStatusBar(self.mainWidget.statusBar)
        self.setupConnections()

        info = QFileInfo(filePath[0])
        AppConfig.projectName = info.fileName()
        AppConfig.projectDir = info.canonicalPath()

        self.setWindowTitle(AppConfig.fullWindowTitle())

    def _onSaveClicked(self):
        if not AppConfig.hasActiveProject():
            self._onSaveAsClicked()
        else:
            Serialize.write(AppConfig.projectFilePath(), self.mainWidget)
            self.statusBar().showMessage("Project saved", 2000)

    def _onSaveAsClicked(self):
        self._createProject("Save As Project", False)

    def _onCloseClicked(self):
        self._shouldClose()

    def _onExitClicked(self):
        if not YesNoDialog.run("Quit application?"):
            return
        
        QApplication.quit()

    def _createProject(self, title: str, doReset: bool):
        if not self._shouldClose(doReset):
            return

        name: str = self._selectProjectName()
        if name is None:
            return

        path = self._selectProjectDir(title)
        if path is None:
            return

        dir = QDir()
        if not dir.mkpath("{}/data/content/".format(path)):
            return

        AppConfig.projectName = name
        AppConfig.projectDir = path

        Serialize.write(AppConfig.projectFilePath(), self.mainWidget)

        self.setWindowTitle(AppConfig.fullWindowTitle())

    def _selectProjectName(self) -> str | None:
        name: str = StrDialog.run("Project name?", "Default", None)
        if name is None:
            return None

        name = name.strip()
        found = re.search(r"^[a-zA-Z0-9_\-\s]+$", name)
        if found is None:
            return None
        name += AppConfig.APP_EXTENSION

        return name

    def _selectProjectDir(self, title: str) -> str | None:
        path = QFileDialog.getExistingDirectory(
            None,
            title,
            "/home",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if path == "":
            return None

        return path

    def _shouldClose(self, doReset: bool = True) -> bool:
        if AppConfig.hasActiveProject():
            if YesNoDialog.run("Save and close current project?"):
                Serialize.write(AppConfig.projectFilePath(), self.mainWidget)
                if doReset:
                    self.reset()
            else:
                return False
        return True

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = e.size()
        super().resizeEvent(e)

    def closeEvent(self, e: QCloseEvent | None) -> None:
        if AppConfig.hasActiveProject():
            Serialize.write(AppConfig.projectFilePath(), self.mainWidget)

        super().closeEvent(e)
