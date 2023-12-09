#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
)

from markupwriter.config import AppConfig
from markupwriter.widgetsupport.documenteditor.plain_document import (
    PlainDocument,
)

class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setDocument(PlainDocument())

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        return super().resizeEvent(e)