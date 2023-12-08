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

from markupwriter.widgets.document_tree import DocumentTree
from markupwriter.widgets.document_editor import DocumentEditor
from markupwriter.widgets.terminal import Terminal
from markupwriter.widgets.document_preview import DocumentPreview

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

        vLayout.addWidget(hSplitter)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn