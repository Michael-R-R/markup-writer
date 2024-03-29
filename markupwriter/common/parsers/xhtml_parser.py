#!/usr/bin/python

import os
import textwrap

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File


class WorkerSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(str)


class XHtmlParser(QRunnable):
    def __init__(self, tokens: list[(str, str)], parent: QObject | None) -> None:
        super().__init__()

        self.tokens: list[(str, str)] = tokens
        self.body = ""
        self.xhtml = ""
        self.signals = WorkerSignal(parent)

        self.tokenDict = {
            r"p": self._processParagraph,
            r"@title": self._processTitle,
            r"@chapter": self._processChapter,
            r"@scene": self._processScene,
            r"@section": self._processSection,
            r"@alignl": self._processAlignL,
            r"@alignc": self._processAlignC,
            r"@alignr": self._processAlignR,
            r"@vspace": self._processVSpace,
            r"@newpage": self._processNewPage,
            r"@cover": self._processCover,
            r"@img": self._processImg,
        }

    @pyqtSlot()
    def run(self):
        try:
            self._processTokens()
            self._createHtmlPage()

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(self.xhtml)

    def _processTokens(self):
        for t in self.tokens:  # keyword(0), text(1)
            if not t[0] in self.tokenDict:
                continue

            self.tokenDict[t[0]](t[1])

    def _processTitle(self, text: str):
        self.body += "<h1 class='title'>{}</h1>\n".format(text)

    def _processChapter(self, text: str):
        self.body += "<h2 class='chapter'>{}</h2>\n".format(text)

    def _processScene(self, _: str):
        self.body += "<p class='scene'>* * *</p>\n"

    def _processSection(self, _: str):
        self.body += "<p class='section'>&#160;</p>\n"

    def _processAlignL(self, text: str):
        self.body += "<p class='alignL'>{}</p>\n".format(text)

    def _processAlignC(self, text: str):
        self.body += "<p class='alignC'>{}</p>\n".format(text)

    def _processAlignR(self, text: str):
        self.body += "<p class='alignR'>{}</p>\n".format(text)

    def _processVSpace(self, text: str):
        if not text.isnumeric():
            return

        htmlText = "<p class='vspace'>&#160;</p>\n" * int(text)
        self.body += htmlText

    def _processNewPage(self, text: str):
        if not text.isnumeric():
            return

        htmlText = "<p class='newPage'>&#160;</p>\n" * int(text)
        self.body += htmlText
        
    def _processCover(self, text: str):
        htmlText = f"<p class='cover'><img src='{text}' alt='' width='512'/></p>\n"
        self.body += htmlText
        
    def _processImg(self, text: str):
        htmlText = "<p class='image'><img src='{}' alt='' width='512'/></p>\n".format(text)
        self.body += htmlText

    def _processParagraph(self, text: str):
        if text.startswith("\t"):
            self.body += "<p class='indent'>{}</p>\n".format(text.strip())
        else:
            self.body += "<p class='noindent'>{}</p>\n".format(text)

    def _createHtmlPage(self):
        tpath = "resources/templates/xhtml/preview.xhtml"
        ppath = os.path.join(AppConfig.WORKING_DIR, tpath)
        template: str = File.read(ppath)
        if template is None:
            return ""

        tpath = "resources/templates/css/base.css"
        cpath = os.path.join(AppConfig.WORKING_DIR, tpath)
        css: str = File.read(cpath)
        if css is None:
            return ""
        
        css = textwrap.indent(css, "\t" * 3)
        body = textwrap.indent(self.body, "\t" * 2)

        template = template.replace("/*style*/", css)
        template = template.replace("<!--body-->", body)

        self.xhtml = template
