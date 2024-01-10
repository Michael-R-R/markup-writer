#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.model.core import (
    CentralWidget,
)

from markupwriter.view.core import (
    CentralWidgetView,
)


class CentralWidgetController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = CentralWidget(self)
        self.view = CentralWidgetView(None)

    def setup(self):
        self.view.hSplitter.insertWidget(0, self.model.docTreeController.view)
        self.view.vSplitter.addWidget(self.model.docEditorController.view)
        self.view.vSplitter.addWidget(self.model.consoleController.view)
        self.view.hSplitter.addWidget(self.model.docPreviewController.view)
        