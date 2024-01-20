#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
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
        
        self.toggleButton = QPushButton("Plain", self)
        self.toggleButton.clicked.connect(self._onToggleButton)
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.textedit)
        self.vLayout.addWidget(self.toggleButton)
        
    def _onToggleButton(self):
        self.isPlainText = not self.isPlainText
        
        if self.isPlainText:
            self.toggleButton.setText("Plain")
            self.textedit.setPlainText(self.plainText)
        else:
            self.toggleButton.setText("HTML")
            self.textedit.clear()
            if self.html == "":
                tokenizer = PreviewTokenizer(self.plainText)
                tokens = tokenizer.run()
                parser = PreviewParser()
                self.html = parser.run(tokens)
                self.textedit.setHtml(self.html)
            else:
                self.textedit.setHtml(self.html)
