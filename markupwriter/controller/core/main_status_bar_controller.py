#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.model.core import (
    MainStatusBar,
)

from markupwriter.view.core import (
    MainStatusBarView,
)


class MainStatusBarController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = MainStatusBar(self)
        self.view = MainStatusBarView(None)

    def setup(self):
        pass
