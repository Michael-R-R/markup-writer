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

from markupwriter.common.handler import (
    ProjectHandler,
)

from .central_widget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.mainWidget = None

        self.setup(CentralWidget(self))
        
        ProjectHandler.setActionStates(self.mainWidget, False)

    def setupConnections(self):
        # --- File menu --- #
        menuBar = self.mainWidget.menuBar
        fileMenu = menuBar.fileMenu
        fileMenu.newAction.triggered.connect(self._onNewClicked)
        fileMenu.openAction.triggered.connect(self._onOpenClicked)
        fileMenu.saveAction.triggered.connect(self._onSaveClicked)
        fileMenu.saveAsAction.triggered.connect(self._onSaveAsClicked)
        fileMenu.closeAction.triggered.connect(self._askToClose)
        fileMenu.exitAction.triggered.connect(self._onExitClicked)

    def setup(self, widget: CentralWidget):
        self.mainWidget = widget

        self.setMenuBar(widget.menuBar)
        self.setCentralWidget(widget)
        self.setStatusBar(widget.statusBar)
        self.setupConnections()

        self.setWindowTitle(AppConfig.fullWindowTitle())
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(AppConfig.mainWindowSize)

    def _onNewClicked(self):
        if not self._askToClose():
            return
        
        widget: CentralWidget = ProjectHandler.createNewProject(self)
        if widget is None:
            return
        
        self.setup(widget)

    def _onOpenClicked(self):
        if not self._askToClose():
            return

        widget: CentralWidget = ProjectHandler.openNewProject(self)
        if widget is None:
            return
        
        self.setup(widget)

    def _onSaveClicked(self):
        if Serialize.write(AppConfig.projectFilePath(), self.mainWidget):
            self.statusBar().showMessage("Project saved", 2000)

    def _onSaveAsClicked(self):
        raise NotImplementedError()

    def _onExitClicked(self):
        if not YesNoDialog.run("Quit application?"):
            return

        QApplication.quit()

    def _askToClose(self) -> bool:
        if AppConfig.hasActiveProject():
            if YesNoDialog.run("Save and close current project?"):
                Serialize.write(AppConfig.projectFilePath(), self.mainWidget)
                self.setup(CentralWidget(self))
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
