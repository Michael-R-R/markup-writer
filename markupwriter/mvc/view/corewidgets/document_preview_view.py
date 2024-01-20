#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSlot,
)

from PyQt6.QtGui import QResizeEvent

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
)

from markupwriter.config import AppConfig


class DocumentPreviewView(QWidget):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.setStyleSheet("padding: 0px;")
        self.tabWidget.tabCloseRequested.connect(self._onTabCloseRequested)

        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.tabWidget)

    def addPage(self, title: str, widget: QWidget):
        index = self.pageExist(title)
        if index > -1:
            self.tabWidget.setCurrentIndex(index)
            return

        self.tabWidget.addTab(widget, title)
        self.tabWidget.setCurrentWidget(widget)

    def pageExist(self, title: str) -> int:
        for i in range(self.tabWidget.count()):
            temp = self.tabWidget.tabText(i)
            if temp == title:
                return i

        return -1

    @pyqtSlot(int)
    def _onTabCloseRequested(self, index: int):
        self.tabWidget.removeTab(index)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docPreviewSize = e.size()
        return super().resizeEvent(e)
