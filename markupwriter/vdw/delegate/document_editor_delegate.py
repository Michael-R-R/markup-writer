#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
    QSize,
    QPoint,
)

import markupwriter.vdw.view as v


class DocumentEditorDelegate(QObject):
    closeDocClicked = pyqtSignal()

    docStatusChanged = pyqtSignal(bool)
    showSearchTriggered = pyqtSignal()
    refPopupTriggered = pyqtSignal(str)
    refPreviewTriggered = pyqtSignal(str)
    wordCountChanged = pyqtSignal(str, int)
    editorResized = pyqtSignal(QSize)
    contextMenuRequested = pyqtSignal(QPoint)

    searchChanged = pyqtSignal(str, bool)
    nextSearchClicked = pyqtSignal()
    prevSearchCliced = pyqtSignal()
    replaceClicked = pyqtSignal()
    replaceAllClicked = pyqtSignal()
    closeSearchClicked = pyqtSignal()

    docPreviewRequested = pyqtSignal(str)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.DocumentEditorView(None)

        self._setupViewConnections()

    def _setupViewConnections(self):
        ed = self.view.editorBar
        ed.closeAction.triggered.connect(lambda: self.closeDocClicked.emit())

        te = self.view.textEdit
        te.docStatusChanged.connect(lambda x: self.docStatusChanged.emit(x))
        te.searchHotkey.triggered.connect(lambda: self.showSearchTriggered.emit())
        te.refPopupTriggered.connect(lambda x: self.refPopupTriggered.emit(x))
        te.refPreviewTriggered.connect(lambda x: self.refPreviewTriggered.emit(x))
        te.wordCountChanged.connect(lambda x, y: self.wordCountChanged.emit(x, y))
        te.resized.connect(lambda x: self.editorResized.emit(x))
        te.customContextMenuRequested.connect(
            lambda x: self.contextMenuRequested.emit(x)
        )

        sb = self.view.searchBox
        sb.searchChanged.connect(lambda x, y: self.searchChanged.emit(x, y))
        sb.nextAction.triggered.connect(lambda: self.nextSearchClicked.emit())
        sb.prevAction.triggered.connect(lambda: self.prevSearchCliced.emit())
        sb.replaceAction.triggered.connect(lambda: self.replaceClicked.emit())
        sb.replaceAllAction.triggered.connect(lambda: self.replaceAllClicked.emit())
        sb.closeAction.triggered.connect(lambda: self.closeSearchClicked.emit())

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
