#!/usr/bin/python

import re


class HtmlParser(object):
    def __init__(self) -> None:
        self.html = ""
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

        return self.html

    def _processParagraph(self, text: str):
        self.html += "<p>{}</p>".format(text)

    def _processHeader1(self, text: str):
        self.html += "<h1 class='title'>{}</h1>".format(text)

    def _processHeader2(self, text: str):
        self.html += "<h2 class='chapter'>{}</h2>".format(text)

    def _processHeader3(self, text: str):
        self.html += "<h3 class='scene'>{}</h3>".format(text)

    def _processHeader4(self, text: str):
        self.html += "<h4 class='section'>{}</h4>".format(text)

    def _searchReplace(self, regex: str, char: str, tag: str):
        expr = re.compile(regex)
        it = expr.finditer(self.html)
        for found in it:
            pattern = found.group(0)
            text = pattern.replace(char, "")
            tag = tag.replace("?", text)
            self.html = self.html.replace(pattern, tag)

    def _process(self, tokens: list[(str, str)]):
        for t in tokens:
            tag = t[0]
            text = t[1]
            self.parseDict[tag](text)

    def _postprocess(self):
        self._searchReplace(r"_(.+?)_(?!_)", "_", "<i>?</i>")  # italize
        self._searchReplace(r"\*(.+?)\*(?!\*)", "*", "<b>?</b>")  # bold
        self._searchReplace(r"\^(.+?)\^(?!\^)", "^", "<i><b>?</b></i>")  # ital+bold
