#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.coresupport.documenteditor import (
    DocumentEditor,
)


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.editor = DocumentEditor(self)

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        vLayout.addWidget(self.editor)

    def onFileDoubleClicked(self, uuid: str):
        self.editor.onFileDoubleClicked(uuid)

    def onFileRemoved(self, uuid: str):
        self.editor.onFileRemoved(uuid)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorViewSize = e.size()
        super().resizeEvent(e)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << self.editor
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> self.editor
        return sIn
