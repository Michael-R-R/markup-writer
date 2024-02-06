#!/usr/bin/python

import os

from PyQt6.QtCore import (
    pyqtSlot,
    QThreadPool,
)

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
        self.threadPool = QThreadPool(parent)

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
            self._runHtmlTokenizer()
            
        vb.setValue(vbpos)

    def _onToggleButton(self):
        self.isPlainText = not self.isPlainText

        if self.isPlainText:
            self._setPlainText(self.plainText)
        else:
            self._runHtmlTokenizer()

    def _setPlainText(self, text: str):
        self.plainText = text
        self.toggleButton.setText("Plain")
        self.textedit.setPlainText(text)

    def _runHtmlTokenizer(self):
        if self.html == "":
            self.refreshButton.setEnabled(False)
            self.toggleButton.setEnabled(False)
            
            tokenizer = HtmlTokenizer(self.plainText, self)
            tokenizer.signals.error.connect(self._onError)
            tokenizer.signals.result.connect(self._onTokenizerFinished)
            self.threadPool.start(tokenizer)
        else:
            self.toggleButton.setText("HTML")
            self.textedit.setHtml(self.html)
            
    @pyqtSlot(list)
    def _onTokenizerFinished(self, tokens: list[(str, str)]):
        parser = HtmlParser(tokens, self)
        parser.signals.error.connect(self._onError)
        parser.signals.result.connect(self._onParserFinished)
        self.threadPool.start(parser)
    
    @pyqtSlot(str)
    def _onParserFinished(self, html: str):
        self.html = html
        self.toggleButton.setText("HTML")
        self.textedit.setHtml(html)
        
        self.refreshButton.setEnabled(True)
        self.toggleButton.setEnabled(True)
        
    @pyqtSlot(str)
    def _onError(self, e: str):
        print(e)
        self.refreshButton.setEnabled(True)
        self.toggleButton.setEnabled(True)
