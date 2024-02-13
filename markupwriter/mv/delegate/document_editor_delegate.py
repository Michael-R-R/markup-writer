#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
)

import markupwriter.mv.model as m
import markupwriter.mv.view as v


class DocumentEditorDelegate(QObject):
    closeDocTriggered = pyqtSignal()
    searchTriggered = pyqtSignal()
    popupRequested = pyqtSignal(str, int)
    previewRequested = pyqtSignal(str, int)
    searchChanged = pyqtSignal(str, bool)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = m.DocumentEditorModel(self)
        self.view = v.DocumentEditorView(None)
        
        self._setupViewConnections()

    def _setupViewConnections(self):
        ed = self.view.editorBar
        ed.closeAction.triggered.connect(lambda: self.closeDocTriggered.emit())

        te = self.view.textEdit
        te.searchHotkey.triggered.connect(lambda: self.searchTriggered.emit())
        te.popupRequested.connect(lambda x, y: self.popupRequested.emit(x, y))
        te.previewRequested.connect(lambda x, y: self.previewRequested.emit(x, y))
        
        sb = self.view.searchBox
        sb.searchChanged.connect(lambda x, y: self.searchChanged.emit(x, y))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.model
        sout << self.view
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.model
        sin >> self.view
        return sin
