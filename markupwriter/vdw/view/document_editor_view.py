#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
    pyqtSignal,
    QSize,
)

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)


import markupwriter.gui.widgets as w


class DocumentEditorView(QWidget):
    resized = pyqtSignal(QSize)
    
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.editorBar = w.DocumentEditorBarWidget(self)
        self.textEdit = w.DocumentEditorWidget(self)
        self.searchBox = w.SearchReplaceWidget(self.textEdit)
        
        self.searchBox.hide()

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.editorBar, 0, 0)
        self.gLayout.addWidget(self.textEdit, 1, 0)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        self.resized.emit(e.size())
        return super().resizeEvent(e)
    
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.textEdit
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.textEdit
        return sin
