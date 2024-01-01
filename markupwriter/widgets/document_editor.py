#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
)

from markupwriter.config import (
    AppConfig,
)

import markupwriter.widgetsupport.documenteditor as de

class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._document = de.PlainDocument()
        
        self.setDocument(self._document)
        self.setTabStopDistance(20.0)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        return super().resizeEvent(e)