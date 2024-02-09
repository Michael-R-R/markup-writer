#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
    QDataStream,
)

from PyQt6.QtWidgets import (
    QWidget,
)

from markupwriter.mvc.model.corewidgets import (
    DocumentPreview,
)

from markupwriter.mvc.view.corewidgets import (
    DocumentPreviewView,
)

import markupwriter.gui.widgets as mw


class DocumentPreviewController(QObject):
    resizeRequested = pyqtSignal()

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentPreview(self)
        self.view = DocumentPreviewView(None)

    def setup(self):
        tabWidget = self.view.tabWidget
        tabWidget.tabCloseRequested.connect(self._onTabCloseRequested)

    def onFileRemoved(self, title: str, uuid: str):
        index = self._pageIndex(title, uuid)
        if index < 0:
            return
        tabwidget = self.view.tabWidget
        tabwidget.removeTab(index)

    def onFileRenamed(self, uuid: str, old: str, new: str):
        index = self._pageIndex(old, uuid)
        if index < 0:
            return
        tabwidget = self.view.tabWidget
        widget: mw.DocumentPreviewWidget = tabwidget.widget(index)
        widget.title = new
        tabwidget.setTabText(index, new)

    def onFilePreviewed(self, title: str, uuid: str):
        ww = self.view.size().width()
        if ww <= 0:
            self.resizeRequested.emit()

        widget = mw.DocumentPreviewWidget(title, uuid, self.view)
        self._addPage(title, uuid, widget)

    def _addPage(self, title: str, uuid: str, widget: QWidget):
        tabwidget = self.view.tabWidget
        index = self._pageIndex(title, uuid)
        if index > -1:
            tabwidget.setCurrentIndex(index)
            return

        tabwidget.addTab(widget, title)
        tabwidget.setCurrentWidget(widget)

    def _pageIndex(self, title: str, uuid: str) -> int:
        tabwidget = self.view.tabWidget
        for i in range(tabwidget.count()):
            widget: mw.DocumentPreviewWidget = tabwidget.widget(i)
            if widget is None:
                continue

            if widget.checkForMatch(title, uuid):
                return i

        return -1

    @pyqtSlot(int)
    def _onTabCloseRequested(self, index: int):
        self.view.tabWidget.removeTab(index)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
