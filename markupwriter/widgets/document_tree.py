#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)


from PyQt6.QtWidgets import (
    QTreeWidget,
    QWidget,
)

from markupwriter.config import AppConfig

class DocumentTree(QTreeWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.resize(AppConfig.docTreeSize)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeSize = e.size()
        return super().resizeEvent(e)