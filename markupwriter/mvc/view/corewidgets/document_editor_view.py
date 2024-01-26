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
        
    def reset(self):
        self.editorBar.reset()
        self.textEdit.reset()
        
    def setPathLabel(self, path: str):
        self.editorBar.pathLabel.setText(path)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        
        # TODO test
        sw = 0
        ww = self.textEdit.width()
        wh = self.textEdit.height()
        tb = self.textEdit.frameWidth()
        rh = self.searchReplace.height()
        rw = self.searchReplace.width()
        rl = ww - sw - rw - 2*tb
        self.searchReplace.move(rl, 2*tb)
        
        return super().resizeEvent(e)
