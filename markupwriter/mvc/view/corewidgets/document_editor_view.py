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
        self.searchReplace = mw.SearchReplaceWidget(self.textEdit)
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addStretch()
        self.hLayout.addWidget(self.editorBar)
        self.hLayout.addStretch()
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addWidget(self.textEdit)
        
        self.searchReplace.hide()
        
    def reset(self):
        self.editorBar.reset()
        self.textEdit.reset()
        
    def setPathLabel(self, path: str):
        self.editorBar.pathLabel.setText(path)
        
    def adjustSearchBox(self):
        if not self.searchReplace.isVisible():
            return
        
        vb = self.textEdit.verticalScrollBar()
        vbw = vb.width() if vb.isVisible() else 0
        ww = self.textEdit.width()
        fw = self.textEdit.frameWidth()
        srw = self.searchReplace.width()
        x = ww - vbw - srw - 2 * fw
        y = 2 * fw
        self.searchReplace.move(x, y)
        
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        self.adjustSearchBox()
        super().resizeEvent(e)
