#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.model.corewidgets import (
    DocumentTree,
)

from markupwriter.view.corewidgets import (
    DocumentTreeView,
)


class DocumentTreeController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentTree(self)
        self.view = DocumentTreeView(None)
