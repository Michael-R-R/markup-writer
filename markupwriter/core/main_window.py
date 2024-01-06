#!/usr/bin/python

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
        self.setupConnections()

        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.mainWindowSize)
        self.setContentsMargins(0, 0, 0, 0)

    def setupConnections(self):
        # --- Main Window --- #
        menuBar = self.mainWidget.menuBar
        fileMenu = menuBar.fileMenu
        fileMenu.newAction.triggered.connect(self._onNewClicked)
        fileMenu.openAction.triggered.connect(self._onOpenClicked)
        fileMenu.saveAction.triggered.connect(self._onSaveClicked)
        fileMenu.closeAction.triggered.connect(self._onCloseClicked)
        fileMenu.exitAction.triggered.connect(self._onExitClicked)

    def reset(self):
        self.mainWidget = CentralWidget(self)
        self.setMenuBar(self.mainWidget.menuBar)
        self.setCentralWidget(self.mainWidget)
        self.setupConnections()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.mainWindowSize)
        AppConfig.projectName = None
        AppConfig.projectDir = None

    def _onNewClicked(self):
        if not self._askToSave():
            return

        path = QFileDialog.getSaveFileName(
            None, "New Project", "/home", "Markup Writer Files (*.mwf)"
        )
        if path[0] == "":
            return

        info = QFileInfo(path[0])

        dir = QDir()
        if not dir.mkpath("{}/data/content/".format(info.canonicalPath())):
            return

        AppConfig.projectName = info.fileName()
        AppConfig.projectDir = info.canonicalPath()

        Serialize.write(self._fullProjectPath(), self.mainWidget)

        self.setWindowTitle("{} - {}".format(AppConfig.APP_NAME, AppConfig.projectName))

    def _onOpenClicked(self):
        if not self._askToSave():
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
        self.setupConnections()
        self.resize(AppConfig.mainWindowSize)

        info = QFileInfo(filePath[0])
        AppConfig.projectName = info.fileName()
        AppConfig.projectDir = info.canonicalPath()

        self.setWindowTitle("{} - {}".format(AppConfig.APP_NAME, AppConfig.projectName))

    def _onSaveClicked(self):
        if not self._hasOpenProject():
            return
        Serialize.write(self._fullProjectPath(), self.mainWidget)

    def _onCloseClicked(self):
        self._askToSave()

    def _onExitClicked(self):
        QApplication.quit()

    def _askToSave(self) -> bool:
        if self._hasOpenProject():
            if YesNoDialog.run("Save and close current project?"):
                Serialize.write(self._fullProjectPath(), self.mainWidget)
                self.reset()
            else:
                return False
        return True

    def _fullProjectPath(self) -> str | None:
        if not self._hasOpenProject():
            return None

        return "{}/{}".format(AppConfig.projectDir, AppConfig.projectName)

    def _hasOpenProject(self) -> bool:
        return AppConfig.projectDir != None

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = e.size()
        super().resizeEvent(e)

    def closeEvent(self, e: QCloseEvent | None) -> None:
        if self._hasOpenProject():
            Serialize.write(self._fullProjectPath(), self.mainWidget)
        
        super().closeEvent(e)
