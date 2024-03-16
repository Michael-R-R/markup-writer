#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from markupwriter.config import AppConfig
from markupwriter.common.provider import Style

import markupwriter.gui.widgets as w


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.editorBar = w.DocumentEditorBarWidget(self)
        self.textEdit = w.DocumentEditorWidget(self)
        self.statusBar = w.StatusBarWidget("-- NORMAL --", "", self)
        self.searchBox = w.SearchBoxWidget(self.textEdit)
        
        self.searchBox.hide()

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.editorBar, 0, 0)
        self.gLayout.addWidget(self.textEdit, 1, 0)
        self.gLayout.addWidget(self.statusBar, 2, 0)
        
        self.setStyleSheet(Style.EDITOR_VIEW)
        
    def adjustSearchBoxPos(self):
        vb = self.textEdit.verticalScrollBar()
        vbw = vb.width() if vb.isVisible() else 0
        ww = self.textEdit.width()
        fw = self.textEdit.frameWidth()
        
        self.searchBox.adjustPos(vbw, ww, fw)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        
        return super().resizeEvent(e)
    
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.editorBar
        sout << self.textEdit
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.editorBar
        sin >> self.textEdit
        return sin
