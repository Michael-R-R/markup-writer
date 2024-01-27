#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from markupwriter.config import AppConfig
import markupwriter.widgets as mw


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.editorBar = mw.DocumentEditorBarWidget(self)
        self.textEdit = mw.DocumentEditorWidget(self)
        self.searchWidget = mw.SearchReplaceWidget(self.textEdit)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.editorBar, 0, 0)
        self.gLayout.addWidget(self.textEdit, 1, 0)
        
        self.searchWidget.hide()
        
    def reset(self):
        self.editorBar.reset()
        self.textEdit.reset()
        self.searchWidget.reset()
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        self.searchWidget.adjustPos()
        
        return super().resizeEvent(e)
