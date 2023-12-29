#!/usr/bin/python

from PyQt6.QtCore import (
    QTimer,
)

from PyQt6.QtGui import (
    QResizeEvent,
    QTextCursor,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

from markupwriter.support.editorparser import (
    PassiveDocumentParser,
)

class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._document = PlainDocument()
        self._passiveParser = PassiveDocumentParser(self._document)
        
        self.setDocument(self._document)
        self.setTabStopDistance(20.0)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        return super().resizeEvent(e)