#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
    QTextOption,
)

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
    QFrame,
)

from markupwriter.config import AppConfig


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.docPathLabel = QLabel("", self)
        
        textEdit = QPlainTextEdit(self)
        textEdit.setFrameShape(QFrame.Shape.NoFrame)
        textEdit.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        textEdit.setTabStopDistance(20.0)
        self.textEdit = textEdit
        
        hLayout = QHBoxLayout()
        hLayout.addStretch()
        hLayout.addWidget(self.docPathLabel)
        hLayout.addStretch()
        self.hLayout = hLayout
        
        vLayout = QVBoxLayout(self)
        vLayout.addLayout(self.hLayout)
        vLayout.addWidget(self.textEdit)
        self.vLayout = vLayout
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        return super().resizeEvent(e)
