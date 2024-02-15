#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
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
import markupwriter.gui.widgets as mw


class DocumentEditorView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.editorBar = mw.DocumentEditorBarWidget(self)
        self.textEdit = mw.DocumentEditorWidget(self)
        self.searchBox = mw.SearchBoxWidget(self.textEdit)
        self.searchAction = QAction("search", self)

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.editorBar, 0, 0)
        self.gLayout.addWidget(self.textEdit, 1, 0)

        self.addAction(self.searchAction)

        self.searchBox.hide()
        self.searchAction.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_F))

    def reset(self):
        self.editorBar.reset()
        self.textEdit.reset()
        self.searchBox.reset()
        
    def adjustSearchBoxPos(self):
        vb = self.textEdit.verticalScrollBar()
        vbw = vb.width() if vb.isVisible() else 0
        ww = self.textEdit.width()
        fw = self.textEdit.frameWidth()
        
        self.searchBox.adjustPos(vbw, ww, fw)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        
        self.adjustSearchBoxPos()

        return super().resizeEvent(e)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.textEdit
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.textEdit
        return sin
