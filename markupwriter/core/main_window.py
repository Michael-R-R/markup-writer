#!/usr/bin/python

from PyQt6.QtGui import (
    QCloseEvent,
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QMainWindow,
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

from markupwriter.coresupport.mainwindow import (
    ProjectHandler,
)

from .central_widget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        widget = CentralWidget(self)

        ProjectHandler.setActionStates(widget, False)

        self.setup(widget)

    def setup(self, widget: CentralWidget):
        self.mainWidget = widget

        self.setMenuBar(widget.menuBar)
        self.setCentralWidget(widget)
        self.setStatusBar(widget.statusBar)
        self.setupConnections()

        self.setWindowTitle(AppConfig.fullWindowTitle())
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(AppConfig.mainWindowSize)

    def setupConnections(self):
        # --- File menu --- #
        menuBar = self.mainWidget.menuBar
        fileMenu = menuBar.fileMenu
        fileMenu.newAction.triggered.connect(self._onNewProject)
        fileMenu.openAction.triggered.connect(self._onOpenProject)
        fileMenu.saveAction.triggered.connect(self._onSaveProject)
        fileMenu.saveAsAction.triggered.connect(self._onSaveAsProject)
        fileMenu.closeAction.triggered.connect(self._onCloseProject)
        fileMenu.exitAction.triggered.connect(self._onExit)

    def _onNewProject(self):
        if not self._onCloseProject():
            return

        widget: CentralWidget = ProjectHandler.createProject(self)
        if widget is None:
            return

        self.setup(widget)

    def _onOpenProject(self):
        if not self._onCloseProject():
            return

        widget: CentralWidget = ProjectHandler.openProject(self)
        if widget is None:
            return

        self.setup(widget)

    def _onSaveProject(self):
        if Serialize.write(AppConfig.projectFilePath(), self.mainWidget):
            self.statusBar().showMessage("Project saved", 2000)

    def _onSaveAsProject(self):
        raise NotImplementedError()

    def _onCloseProject(self) -> bool:
        if not AppConfig.hasActiveProject():
            return True

        if YesNoDialog.run("Save and close current project?"):
            Serialize.write(AppConfig.projectFilePath(), self.mainWidget)

            widget: CentralWidget = ProjectHandler.closeProject(self)

            self.setup(widget)

            return True

        return False

    def _onExit(self):
        if not YesNoDialog.run("Quit application?"):
            return

        QApplication.quit()

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = e.size()
        super().resizeEvent(e)

    def closeEvent(self, e: QCloseEvent | None) -> None:
        if AppConfig.hasActiveProject():
            Serialize.write(AppConfig.projectFilePath(), self.mainWidget)

        super().closeEvent(e)
