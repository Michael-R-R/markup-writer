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

from markupwriter.config import (
    AppConfig,
)

from markupwriter.corewidgets import (
    MainMenuBar,
    DocumentTreeView,
    DocumentEditor,
    DocumentPreview,
    Terminal,
)

class CentralWidget(QWidget):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)
        
        self.menuBar = MainMenuBar(self)

        vLayout = QVBoxLayout(self)
        hSplitter = QSplitter(Qt.Orientation.Horizontal)
        vSplitter = QSplitter(Qt.Orientation.Vertical)

        self.treeView = DocumentTreeView(self)
        self.editor = DocumentEditor(self)
        self.terminal = Terminal(self)
        self.preview = DocumentPreview(self)

        hSplitter.addWidget(self.treeView)
        hSplitter.addWidget(vSplitter)
        vSplitter.addWidget(self.editor)
        vSplitter.addWidget(self.terminal)
        hSplitter.addWidget(self.preview)

        hSplitter.setSizes([AppConfig.docTreeViewSize.width(),
                            AppConfig.docEditorSize.width(),
                            AppConfig.docPreviewSize.width()])
        vSplitter.setSizes([AppConfig.docEditorSize.height(),
                            AppConfig.terminalSize.height()])

        vLayout.addWidget(hSplitter)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.setupConnections()

    def setupConnections(self):
        # --- Editor --- #
        self.treeView.tree.fileDoubleClicked.connect(self.editor.onFileDoubleClicked)
        self.treeView.tree.fileRemoved.connect(self.editor.onFileRemoved)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << self.treeView
        sOut << self.editor
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> self.treeView
        sIn >> self.editor
        return sIn