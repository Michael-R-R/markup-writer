#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
    QSize,
    QPoint,
)

from . import BaseDelegate

import markupwriter.vdw.view as v
import markupwriter.vdw.worker as w


class DocumentEditorDelegate(BaseDelegate):
    closeDocClicked = pyqtSignal()

    stateChanged = pyqtSignal(str)
    stateBufferChanged = pyqtSignal(str)
    docStatusChanged = pyqtSignal(bool)
    showSearchTriggered = pyqtSignal()
    showRefPopupClicked = pyqtSignal(QPoint)
    showRefPreviewClicked = pyqtSignal(QPoint)
    wordCountChanged = pyqtSignal(str, int)
    editorResized = pyqtSignal(QSize)
    contextMenuRequested = pyqtSignal(QPoint)

    searchChanged = pyqtSignal(str, bool)
    nextSearchClicked = pyqtSignal()
    prevSearchCliced = pyqtSignal()
    replaceClicked = pyqtSignal()
    replaceAllClicked = pyqtSignal()
    closeSearchClicked = pyqtSignal()

    refPreviewRequested = pyqtSignal(str)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.DocumentEditorView(None)
        self.worker = w.DocumentEditorWorker(self.view, self)
        
        self.setupConnections()
        
    def setup(self):
        pass

    def setupConnections(self):
        ed = self.view.editorBar
        ed.closeAction.triggered.connect(lambda: self.closeDocClicked.emit())

        te = self.view.textEdit
        te.stateChanged.connect(lambda x: self.stateChanged.emit(x))
        te.stateBufferChanged.connect(lambda x: self.stateBufferChanged.emit(x))
        te.docStatusChanged.connect(lambda x: self.docStatusChanged.emit(x))
        te.searchHotkey.triggered.connect(lambda: self.showSearchTriggered.emit())
        te.showRefPopupClicked.connect(lambda x: self.showRefPopupClicked.emit(x))
        te.showRefPreviewClicked.connect(lambda x: self.showRefPreviewClicked.emit(x))
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
        
        worker = self.worker
        worker.refPreviewRequested.connect(lambda x: self.refPreviewRequested.emit(x))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
