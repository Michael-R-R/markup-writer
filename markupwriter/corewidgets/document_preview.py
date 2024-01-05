#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QTextBrowser,
    QWidget,
)

from markupwriter.config import (
    AppConfig,
)

class DocumentPreview(QTextBrowser):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        return super().resizeEvent(e)
