#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
)

from markupwriter.mvc.model.corewidgets import (
    Console,
)

from markupwriter.mvc.view.corewidgets import (
    ConsoleView,
)


class ConsoleController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = Console(self)
        self.view = ConsoleView(None)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
