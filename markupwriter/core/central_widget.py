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
    DocumentTreeView,
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

        self.documentTreeView = DocumentTreeView(self)
        self.documentEditor = DocumentEditor(self)
        self.terminal = Terminal(self)
        self.documentPreview = DocumentPreview(self)

        hSplitter.addWidget(self.documentTreeView)
        hSplitter.addWidget(vSplitter)
        vSplitter.addWidget(self.documentEditor)
        vSplitter.addWidget(self.terminal)
        hSplitter.addWidget(self.documentPreview)

        hSplitter.setSizes([AppConfig.docTreeViewSize.width(),
                            AppConfig.docEditorSize.width(),
                            AppConfig.docPreviewSize.width()])
        vSplitter.setSizes([AppConfig.docEditorSize.height(),
                            AppConfig.terminalSize.height()])

        vLayout.addWidget(hSplitter)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn