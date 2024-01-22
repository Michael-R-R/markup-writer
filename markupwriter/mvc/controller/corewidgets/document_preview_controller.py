#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
    QDataStream,
)

from markupwriter.mvc.model.corewidgets import (
    DocumentPreview,
)

from markupwriter.mvc.view.corewidgets import (
    DocumentPreviewView,
)

import markupwriter.widgets as mw


class DocumentPreviewController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.model = DocumentPreview(self)
        self.view = DocumentPreviewView(None)
        
    def setup(self):
        pass
        
    pyqtSlot(str)
    def onFilePreviewed(self, title: str, uuid: str):
        widget = mw.DocumentPreviewWidget(uuid, self.view)
        self.view.addPage(title, widget)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
