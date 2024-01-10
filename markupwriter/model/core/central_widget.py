#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.controller.corewidgets import (
    DocumentTreeController,
    DocumentEditorController,
    ConsoleController,
    DocumentPreviewController,
)


class CentralWidget(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.docTreeController = DocumentTreeController(self)
        self.docEditorController = DocumentEditorController(self)
        self.consoleController = ConsoleController(self)
        self.docPreviewController = DocumentPreviewController(self)
