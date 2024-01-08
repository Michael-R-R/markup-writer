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
    DocumentEditorView,
    DocumentPreview,
    Terminal,
    MainStatusBar,
)


class CentralWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.menuBar = MainMenuBar(self)
        self.statusBar = MainStatusBar(self)

        self.treeView = DocumentTreeView(self)
        self.editorView = DocumentEditorView(self)
        self.terminal = Terminal(self)
        self.preview = DocumentPreview(self)

        vLayout = QVBoxLayout(self)
        hSplitter = QSplitter(Qt.Orientation.Horizontal)
        vSplitter = QSplitter(Qt.Orientation.Vertical)

        hSplitter.addWidget(self.treeView)
        hSplitter.addWidget(vSplitter)
        vSplitter.addWidget(self.editorView)
        vSplitter.addWidget(self.terminal)
        hSplitter.addWidget(self.preview)

        hSplitter.setSizes(
            [
                AppConfig.docTreeViewSize.width(),
                AppConfig.docEditorViewSize.width(),
                AppConfig.docPreviewSize.width(),
            ]
        )
        vSplitter.setSizes(
            [AppConfig.docEditorViewSize.height(), AppConfig.terminalSize.height()]
        )

        vLayout.addWidget(hSplitter)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setupConnections()

    def setupConnections(self):
        # --- Tree --- #
        tree = self.treeView.tree
        tree.fileDoubleClicked.connect(self.editorView.onFileDoubleClicked)
        tree.fileRemoved.connect(self.editorView.onFileRemoved)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << self.treeView
        sOut << self.editorView
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> self.treeView
        sIn >> self.editorView
        return sIn
