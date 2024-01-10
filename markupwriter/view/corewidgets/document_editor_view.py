#!/usr/bin/python

from PyQt6.QtGui import (
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
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addWidget(self.textEdit)
