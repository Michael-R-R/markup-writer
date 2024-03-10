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

from markupwriter.config import ProjectConfig
from markupwriter.common.util import File
from markupwriter.common.syntax import Highlighter
from markupwriter.common.tokenizers import XHtmlPreviewTokenizer
from markupwriter.common.parsers import XHtmlParser


class DocumentPreviewWidget(QWidget):
    def __init__(self, title: str, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent)

        path = os.path.join(ProjectConfig.contentPath(), uuid)

        self.title = title
        self.uuid = uuid
        self.plainText = File.read(path)
        self.html = ""
        self.isPlainText = False
        self.prevVal = 0
        self.threadPool = QThreadPool(parent)

        self.textedit = QTextEdit(self)
        self.highlighter = Highlighter(self.textedit.document(), None)
        self.textedit.setReadOnly(True)
        self.textedit.setTabStopDistance(20.0)

        self.refreshButton = QPushButton("Refresh", self)
        self.refreshButton.clicked.connect(self.refreshContent)

        self.toggleButton = QPushButton("Plain", self)
        self.toggleButton.clicked.connect(self.toggleView)

        self.mLayout = QGridLayout(self)
        self.mLayout.addWidget(self.textedit, 0, 0, 1, 2)
        self.mLayout.addWidget(self.refreshButton, 1, 0)
        self.mLayout.addWidget(self.toggleButton, 1, 1)
        
        self._runHtmlTokenizer()

    def checkForMatch(self, title: str, uuid: str) -> bool:
        return title == self.title and uuid == self.uuid
    
    def scrollContentX(self, direction: int):
        hb = self.textedit.horizontalScrollBar()
        if hb is None:
            return
        val = hb.value()
        hb.setValue(val + (16 * direction))
    
    def scrollContentY(self, direction: int):
        vb = self.textedit.verticalScrollBar()
        if vb is None:
            return
        val = vb.value()
        vb.setValue(val + (16 * direction))

    @pyqtSlot()
    def refreshContent(self):
        path = os.path.join(ProjectConfig.contentPath(), self.uuid)
        if not File.exists(path):
            self.close()

        vbValue = self.textedit.verticalScrollBar().value()

        text = File.read(path)
        self.plainText = text
        self.html = ""
        if self.isPlainText:
            self._setPlainText(text)
        else:
            self._runHtmlTokenizer()

        self.textedit.verticalScrollBar().setValue(vbValue)

    @pyqtSlot()
    def toggleView(self):
        self.prevVal = self.textedit.verticalScrollBar().value()
        self.isPlainText = not self.isPlainText

        if self.isPlainText:
            self._setPlainText(self.plainText)
        else:
            self._runHtmlTokenizer()

    def _setPlainText(self, text: str):
        self.plainText = text
        self.toggleButton.setText("Plain")
        self.textedit.setPlainText(text)
        self.textedit.verticalScrollBar().setValue(self.prevVal)

    def _runHtmlTokenizer(self):
        if self.html == "":
            self.refreshButton.setEnabled(False)
            self.toggleButton.setEnabled(False)

            tokenizer = XHtmlPreviewTokenizer(self.plainText, self)
            tokenizer.signals.error.connect(self._onError)
            tokenizer.signals.result.connect(self._onTokenizerFinished)
            self.threadPool.start(tokenizer)
            self.toggleButton.setText("Tokenizing...")
        else:
            self.toggleButton.setText("HTML")
            self.textedit.setHtml(self.html)
            self.textedit.verticalScrollBar().setValue(self.prevVal)

    @pyqtSlot(list)
    def _onTokenizerFinished(self, tokens: list[(str, str)]):
        parser = XHtmlParser(tokens, self)
        parser.signals.error.connect(self._onError)
        parser.signals.result.connect(self._onParserFinished)
        self.threadPool.start(parser)
        self.toggleButton.setText("Parsing...")

    @pyqtSlot(str)
    def _onParserFinished(self, html: str):
        self.refreshButton.setEnabled(True)
        self.toggleButton.setEnabled(True)
        
        self.toggleButton.setText("HTML")
        self.html = html
        self.textedit.setHtml(html)
        self.textedit.verticalScrollBar().setValue(self.prevVal)
        
    @pyqtSlot(str)
    def _onProgressUpdate(self, status: str):
        self.toggleButton.setText(status)

    @pyqtSlot(str)
    def _onError(self, e: str):
        self.refreshButton.setEnabled(True)
        self.toggleButton.setEnabled(True)
        self.toggleButton.setText("HTML")
        
        self.html = ""
        self.prevVal = 0
        self.textedit.setPlainText("ERROR: {}".format(e))
