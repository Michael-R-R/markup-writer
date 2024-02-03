#!/usr/bin/python

import os, re

from markupwriter.config import AppConfig
from markupwriter.common.util import File


class HtmlParser(object):
    def __init__(self) -> None:
        self.body = ""

        self.parseDict = {
            "p": self._processParagraph,
            "#": self._processHeader1,
            "##": self._processHeader2,
            "###": self._processHeader3,
            "####": self._processHeader4,
        }

    def run(self, tokens: list[(str, str)]) -> str:
        self._process(tokens)
        self._postprocess()

        return self._createHTML()

    def _process(self, tokens: list[(str, str)]):
        for t in tokens:
            tag = t[0]
            text = t[1]
            self.parseDict[tag](text)

    def _postprocess(self):
        self._searchReplace(r"@bold\(.*\)", "<b>?</b>")  # bold
        self._searchReplace(r"@ital\(.*\)", "<i>?</i>")  # italize
        self._searchReplace(r"@boldItal\(.*\)", "<b><i>?</i></b>")  # bold+italize

    def _createHTML(self) -> str:
        tpath = os.path.join(AppConfig.WORKING_DIR, "resources/html/preview.html")
        template: str = File.read(tpath)
        if template is None:
            return ""
        
        cpath = os.path.join(AppConfig.WORKING_DIR, "resources/css/preview.css")
        css: str = File.read(cpath)
        if css is None:
            return ""
        
        template = template.replace("/*style*/", css)
        template = template.replace("<!--body-->", self.body)
        
        return template

    def _processParagraph(self, text: str):
        self.body += "<p class='paragraph'>{}</p>\n".format(text)

    def _processHeader1(self, text: str):
        self.body += "<h1 class='title'>{}</h1>\n".format(text)

    def _processHeader2(self, text: str):
        self.body += "<h2 class='chapter'>{}</h2>\n".format(text)

    def _processHeader3(self, text: str):
        self.body += "<p class='scene'>* * *</p>\n"

    def _processHeader4(self, text: str):
        self.body += "<div class='section'><br><br></div>\n"

    def _searchReplace(self, regex: str, html: str):
        tagRegex = re.compile(regex)
        textRegex = re.compile(r"(?<=\().+?(?=\))")
        
        it = tagRegex.finditer(self.body)
        for found in it:
            tag = found.group(0)
            textFound = textRegex.search(tag)
            if textFound is None:
                continue
            
            html = html.replace("?", textFound.group(0))
            self.body = self.body.replace(tag, html)
