#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.model.corewidgets import (
    DocumentEditor,
)

from markupwriter.view.corewidgets import (
    DocumentEditorView,
)


class DocumentEditorController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentEditor(self)
        self.view = DocumentEditorView(None)
