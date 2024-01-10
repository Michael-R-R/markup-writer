#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.mvc.model.core import (
    MainWindow,
)

from markupwriter.mvc.view.core import (
    MainWindowView,
)


class MainWindowController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = MainWindow(self)
        self.view = MainWindowView(None)

    def setup(self):
        self.model.menuBarController.setup()
        self.model.centralController.setup()
        self.model.statusBarController.setup()

        self.view.setMenuBar(self.model.menuBarController.view)
        self.view.setCentralWidget(self.model.centralController.view)
        self.view.setStatusBar(self.model.statusBarController.view)

    def show(self):
        self.view.show()