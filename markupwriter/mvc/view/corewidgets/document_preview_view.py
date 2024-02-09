#!/usr/bin/python

from PyQt6.QtGui import QResizeEvent

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from markupwriter.config import AppConfig
from markupwriter.common.provider import Style
import markupwriter.gui.widgets as mw


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.tabWidget = mw.PreviewTabWidget(self)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.tabWidget, 0, 0)
        
        self.setStyleSheet(Style.PREVIEW_VIEW)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        return super().resizeEvent(e)
