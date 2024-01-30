#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtGui import (
    QResizeEvent,
    QAction,
    QKeySequence,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from markupwriter.config import AppConfig
import markupwriter.widgets as mw


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.editorBar = mw.DocumentEditorBarWidget(self)
        self.textEdit = mw.DocumentEditorWidget(self)
        self.searchWidget = mw.SearchReplaceWidget(self.textEdit)
        self.searchAction = QAction("search", self)

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.editorBar, 0, 0)
        self.gLayout.addWidget(self.textEdit, 1, 0)

        self.addAction(self.searchAction)

        self.searchWidget.hide()
        self.searchAction.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_F))

    def reset(self):
        self.editorBar.reset()
        self.textEdit.reset()
        self.searchWidget.reset()

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        self.searchWidget.adjustPos()

        return super().resizeEvent(e)
