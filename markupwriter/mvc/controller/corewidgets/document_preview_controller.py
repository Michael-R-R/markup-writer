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

from markupwriter.config import AppConfig
from markupwriter.common.util import File
import markupwriter.widgets as mw


class DocumentPreviewController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.model = DocumentPreview(self)
        self.view = DocumentPreviewView(None)
        
    pyqtSlot(str)
    def onTextPreview(self, uuid: str):
        widget = mw.DocumentTextEdit(self.view)
        widget.setEnabled(True)
        widget.setReadOnly(True)
        path = AppConfig.projectContentPath() + uuid
        widget.setPlainText(File.read(path))
        
        self.view.removeWidget()
        self.view.addWidget(widget)
        
    def onAddBrowserDocument(self, widget: mw.DocumentPreviewBrowser):
        self.view.removeWidget()
        self.view.addWidget(widget)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
