#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSlot,
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

from markupwriter.common.provider import (
    Style,
)

from markupwriter.coresupport.documenteditor import (
    DocumentEditorBar,
    DocumentEditor,
)


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.editorBar = DocumentEditorBar(self)
        self.editor = DocumentEditor(self)

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        vLayout.addWidget(self.editorBar)
        vLayout.addWidget(self.editor)
        
        self.setStyleSheet(Style.EDITOR_VIEW)

    @pyqtSlot(str, list)
    def onFileDoubleClicked(self, uuid: str, paths: list[str]):
        self.editorBar.onFileDoubleClicked(paths)
        self.editor.onFileDoubleClicked(uuid)

    @pyqtSlot(str)
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
