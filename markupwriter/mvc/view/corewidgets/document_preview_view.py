#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
)

from PyQt6.QtGui import QResizeEvent

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTabWidget,
)

from markupwriter.config import AppConfig
from markupwriter.common.provider import Style


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.setStyleSheet("padding: 0px;")
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.tabWidget, 0, 0)
        
        self.setStyleSheet(Style.PREVIEW_VIEW)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        return super().resizeEvent(e)
