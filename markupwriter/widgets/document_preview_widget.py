#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File
from markupwriter.common.syntax import Highlighter
from markupwriter.common.tokenizers import PreviewTokenizer
from markupwriter.common.parsers import PreviewParser


class DocumentPreviewWidget(QWidget):
    def __init__(self, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        path = AppConfig.projectContentPath() + uuid
        
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
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.refreshButton)
        self.hLayout.addWidget(self.toggleButton)
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.textedit)
        self.vLayout.addLayout(self.hLayout)
        
    def _onRefreshButton(self):
        path = AppConfig.projectContentPath() + self.uuid
        if not File.exists(path):
            self.close()
            
        text = File.read(path)
        self.plainText = text
        self.html = ""
        if self.isPlainText:
            self._setPlainText(text)
        else:
            self._setHtmlText(self.html)
        
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
            tokenizer = PreviewTokenizer(self.plainText)
            tokens = tokenizer.run()
            parser = PreviewParser()
            text = parser.run(tokens)
            
        self.html = text
        self.toggleButton.setText("HTML")
        self.textedit.setHtml(self.html)
