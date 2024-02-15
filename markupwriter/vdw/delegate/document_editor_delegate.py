#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
    QSize,
)

import markupwriter.vdw.view as v


class DocumentEditorDelegate(QObject):
    closeDocClicked = pyqtSignal()
    docStatusChanged = pyqtSignal(bool)
    searchTriggered = pyqtSignal()
    popupRequested = pyqtSignal(str, int)
    previewRequested = pyqtSignal(str, int)
    searchChanged = pyqtSignal(str, bool)
    editorResized = pyqtSignal(QSize)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.view = v.DocumentEditorView(None)
        
        self._setupViewConnections()

    def _setupViewConnections(self):
        ed = self.view.editorBar
        ed.closeAction.triggered.connect(lambda: self.closeDocClicked.emit())

        te = self.view.textEdit
        te.docStatusChanged.connect(lambda x: self.docStatusChanged.emit(x))
        te.searchHotkey.triggered.connect(lambda: self.searchTriggered.emit())
        te.popupRequested.connect(lambda x, y: self.popupRequested.emit(x, y))
        te.previewRequested.connect(lambda x, y: self.previewRequested.emit(x, y))
        te.resized.connect(lambda x: self.editorResized.emit(x))
        
        sb = self.view.searchBox
        sb.searchChanged.connect(lambda x, y: self.searchChanged.emit(x, y))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.view
        return sin
