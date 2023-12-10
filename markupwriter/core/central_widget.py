#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
)

from PyQt6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
)

from markupwriter.config import AppConfig
from markupwriter.widgets import (
    DocumentTree,
    DocumentEditor,
    DocumentPreview,
    Terminal
)

class CentralWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        vLayout = QVBoxLayout(self)
        hSplitter = QSplitter(Qt.Orientation.Horizontal)
        vSplitter = QSplitter(Qt.Orientation.Vertical)

        documentTree = DocumentTree(self)
        documentEditor = DocumentEditor(self)
        terminal = Terminal(self)
        documentPreview = DocumentPreview(self)

        hSplitter.addWidget(documentTree)
        hSplitter.addWidget(vSplitter)
        vSplitter.addWidget(documentEditor)
        vSplitter.addWidget(terminal)
        hSplitter.addWidget(documentPreview)

        hSplitter.setSizes([AppConfig.docTreeSize.width(),
                            AppConfig.docEditorSize.width(),
                            AppConfig.docPreviewSize.width()])
        vSplitter.setSizes([AppConfig.docEditorSize.height(),
                            AppConfig.terminalSize.height()])

        vLayout.addWidget(hSplitter)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn