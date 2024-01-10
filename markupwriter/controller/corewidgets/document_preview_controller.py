#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.model.corewidgets import (
    DocumentPreview,
)

from markupwriter.view.corewidgets import (
    DocumentPreviewView,
)


class DocumentPreviewController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.model = DocumentPreview(self)
        self.view = DocumentPreviewView(None)
