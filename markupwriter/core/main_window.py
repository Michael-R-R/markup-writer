#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSignal,
    pyqtSlot,
)

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
    setupTriggered = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()

        # TODO read in file for testing purposes
        widget: CentralWidget = Serialize.read(CentralWidget, "/home/michael/ssd1/writing/markup_writer/demo/demo.mwf")
        ProjectHandler.setActionStates(widget, True)
        AppConfig.projectDir = "/home/michael/ssd1/writing/markup_writer/demo/"
        AppConfig.projectName = "demo.mwf"

        self.setup(widget)

    def setup(self, widget: CentralWidget):
        self.mainWidget = widget

        self.setMenuBar(widget.menuBar)
        self.setCentralWidget(widget)
        self.setStatusBar(widget.statusBar)

        self.setWindowTitle(AppConfig.fullWindowTitle())
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(AppConfig.mainWindowSize)
        
        self.setupTriggered.emit()

    @pyqtSlot()
    def onNewProject(self):
        if not self.onCloseProject():
            return

        widget: CentralWidget = ProjectHandler.createProject(self)
        if widget is None:
            return

        self.setup(widget)

    @pyqtSlot()
    def onOpenProject(self):
        if not self.onCloseProject():
            return

        widget: CentralWidget = ProjectHandler.openProject(self)
        if widget is None:
            return

        self.setup(widget)

    @pyqtSlot()
    def onSaveProject(self):
        if Serialize.write(AppConfig.projectFilePath(), self.mainWidget):
            self.statusBar().showMessage("Project saved", 2000)

    @pyqtSlot()
    def onSaveAsProject(self):
        # TODO implement
        raise NotImplementedError()

    @pyqtSlot()
    def onCloseProject(self) -> bool:
        if not AppConfig.hasActiveProject():
            return True

        if YesNoDialog.run("Save and close current project?"):
            Serialize.write(AppConfig.projectFilePath(), self.mainWidget)

            widget: CentralWidget = ProjectHandler.closeProject(self)

            self.setup(widget)

            return True

        return False

    @pyqtSlot()
    def onExit(self):
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
