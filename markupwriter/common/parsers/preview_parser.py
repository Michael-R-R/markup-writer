#!/usr/bin/python

import re


class PreviewParser(object):
    def __init__(self) -> None:
        self.html = ""

    def run(self, tokens: list[(str, str)]) -> str:
        funcs = {
            "p": self._processParagraph,
            "#": self._processHeader1,
            "##": self._processHeader2,
            "###": self._processHeader3,
            "####": self._processHeader4,
        }

        for t in tokens:
            funcs[t[0]](t[1])

        self._postprocess()

        return self.html

    def _processParagraph(self, line: str):
        self.html += "<p>{}</p>".format(line)

    def _processHeader1(self, line: str):
        self.html += "<h1 class='title'>{}</h1>".format(line)

    def _processHeader2(self, line: str):
        self.html += "<h2 class='chapter'>{}</h2>".format(line)

    def _processHeader3(self, line: str):
        self.html += "<h3 class='scene'>{}</h3>".format(line)

    def _processHeader4(self, line: str):
        self.html += "<h4 class='section'>{}</h4>".format(line)

    def _searchReplace(self, regex: str, char: str, tag: str):
        expr = re.compile(regex)
        it = expr.finditer(self.html)
        for found in it:
            pattern = found.group(0)
            text = pattern.replace(char, "")
            tag = tag.replace("?", text)
            self.html = self.html.replace(pattern, tag)

    def _postprocess(self):
        self._searchReplace(r"_(.+?)_(?!_)", "_", "<i>?</i>")  # italize
        self._searchReplace(r"\*(.+?)\*(?!\*)", "*", "<b>?</b>")  # bold
        self._searchReplace(r"\^(.+?)\^(?!\^)", "^", "<i><b>?</b></i>")  # ital+bold
