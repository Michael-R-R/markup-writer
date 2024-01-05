#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QMainWindow,
)

from markupwriter.config import (
    AppConfig,
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

        self.mainWidget = CentralWidget(self)

        self.setMenuBar(self.mainWidget.menuBar)
        self.setCentralWidget(self.mainWidget)

        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.mainWindowSize)
        self.setContentsMargins(0, 0, 0, 0)

        self.setupConnections()

    def setupConnections(self):
        # --- Main Window --- #
        menuBar = self.mainWidget.menuBar
        fileMenu = menuBar.fileMenu
        fileMenu.newAction.triggered.connect(self._onNewClicked)
        fileMenu.openAction.triggered.connect(self._onOpenClicked)
        fileMenu.saveAction.triggered.connect(self._onSerialize)

    def _onNewClicked(self):
        if not ProjectHandler.onNewClicked():
            return
        self._onSerialize()
        self.setWindowTitle("{} - {}".format(AppConfig.APP_NAME,
                                             AppConfig.projectName))

    def _onOpenClicked(self):
        widget: CentralWidget = ProjectHandler.onOpenClicked()
        if widget is None:
            raise RuntimeError()
        self.mainWidget = widget
        self.setMenuBar(self.mainWidget.menuBar)
        self.setCentralWidget(self.mainWidget)
        self.setupConnections()

    def _onSerialize(self):
        path = AppConfig.projectFilePath()
        if path == "":
            return
        Serialize.write(path, self.mainWidget)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = a0.size()
        return super().resizeEvent(a0)
        