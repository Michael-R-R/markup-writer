#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

import markupwriter.mv.delegate as d


class DocumentEditorWorker(QObject):
    def __init__(self, ded: d.DocumentEditorDelegate, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.ded = ded
        
    @pyqtSlot()
    def onCloseDocument(self):
        pass
    
    @pyqtSlot()
    def onSaveDocument(self):
        pass