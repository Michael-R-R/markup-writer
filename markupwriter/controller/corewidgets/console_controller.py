#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.model.corewidgets import (
    Console,
)

from markupwriter.view.corewidgets import (
    ConsoleView,
)


class ConsoleController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = Console(self)
        self.view = ConsoleView(None)
