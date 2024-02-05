#!/usr/bin/python

import os

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTextEdit,
    QPushButton,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File
from markupwriter.common.syntax import Highlighter
from markupwriter.common.tokenizers import HtmlTokenizer
from markupwriter.common.parsers import HtmlParser


class DocumentPreviewWidget(QWidget):
    def __init__(self, title: str, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent)

        path = os.path.join(AppConfig.projectContentPath(), uuid)

        self.title = title
        self.uuid = uuid
        self.plainText = File.read(path)
        self.html = ""
        self.isPlainText = True

        self.textedit = QTextEdit(self)
        self.highlighter = Highlighter(self.textedit.document())
        self.textedit.setReadOnly(True)
        self.textedit.setTabStopDistance(20.0)
        self.textedit.setPlainText(self.plainText)

        self.refreshButton = QPushButton("Refresh", self)
        self.refreshButton.clicked.connect(self._onRefreshButton)

        self.toggleButton = QPushButton("Plain", self)
        self.toggleButton.clicked.connect(self._onToggleButton)
        
        self.mLayout = QGridLayout(self)
        self.mLayout.addWidget(self.textedit, 0, 0, 1, 2)
        self.mLayout.addWidget(self.refreshButton, 1, 0)
        self.mLayout.addWidget(self.toggleButton, 1, 1)

    def checkForMatch(self, title: str, uuid: str) -> bool:
        return title == self.title and uuid == self.uuid

    def _onRefreshButton(self):
        path = os.path.join(AppConfig.projectContentPath(), self.uuid)
        if not File.exists(path):
            self.close()
            
        vb = self.textedit.verticalScrollBar()
        vbpos = vb.value()

        text = File.read(path)
        self.plainText = text
        self.html = ""
        if self.isPlainText:
            self._setPlainText(text)
        else:
            self._setHtmlText(self.html)
            
        vb.setValue(vbpos)

    def _onToggleButton(self):
        self.isPlainText = not self.isPlainText

        if self.isPlainText:
            self._setPlainText(self.plainText)
        else:
            self._setHtmlText(self.html)

    def _setPlainText(self, text: str):
        self.plainText = text
        self.toggleButton.setText("Plain")
        self.textedit.setPlainText(text)

    def _setHtmlText(self, text: str):
        if text == "":
            tokenizer = HtmlTokenizer(self.plainText)
            body = tokenizer.run()
            
            parser = HtmlParser()
            text = parser.run(body)

        self.html = text
        self.toggleButton.setText("HTML")
        self.textedit.setHtml(self.html)
