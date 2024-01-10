#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.mvc.model.corewidgets import (
    DocumentEditor,
)

from markupwriter.mvc.view.corewidgets import (
    DocumentEditorView,
)


class DocumentEditorController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentEditor(self)
        self.view = DocumentEditorView(None)
