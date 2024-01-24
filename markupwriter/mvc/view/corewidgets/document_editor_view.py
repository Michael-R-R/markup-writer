#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from markupwriter.config import AppConfig
import markupwriter.widgets as mw


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.editorBar = mw.DocumentEditorBarWidget(self)
        self.textEdit = mw.DocumentEditorWidget(self)
        
        hLayout = QHBoxLayout()
        hLayout.addStretch()
        hLayout.addWidget(self.editorBar)
        hLayout.addStretch()
        self.hLayout = hLayout
        
        vLayout = QVBoxLayout(self)
        vLayout.addLayout(self.hLayout)
        vLayout.addWidget(self.textEdit)
        self.vLayout = vLayout
        
    def clearAll(self):
        self.editorBar.pathLabel.clear()
        self.textEdit.clear()
        
    def setPathLabel(self, path: str):
        self.editorBar.pathLabel.setText(path)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        return super().resizeEvent(e)
