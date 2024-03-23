#!/usr/bin/python

import re

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)


class WorkerSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(list)


class XHtmlTokenizer(QRunnable):
    def __init__(self, text: str, parent: QObject | None) -> None:
        super().__init__()

        self.text = text
        self.tokens: list[(str, str)] = list()  # tag, text
        self.signals = WorkerSignal(parent)

        self.parenRegex = re.compile(r"(?<=\().*?(?=\))")
        self.nlParenRegex = re.compile(r"(?<=\()(\n|.)*?(?=\))")
        self.keywordRegex = re.compile(r"^@.*(?=\()")
        
        self.ignoreSet = set()

        self.replaceDict = {
            r"@b\((\n|.)*?\)": self._replaceBold,
            r"@i\((\n|.)*?\)": self._replaceItal,
            r"@bi\((\n|.)*?\)": self._replaceBoldItal,
        }

        self.removeDict = dict()

    @pyqtSlot()
    def run(self):
        try:
            self._preprocess()
            self._process()

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(self.tokens)

    def _preprocess(self):
        for tag in self.replaceDict:
            self.replaceDict[tag](tag)

        for tag in self.removeDict:
            self.removeDict[tag](tag)

        self.text = self.text.strip("\r\n ")

    def _process(self):
        raise NotImplementedError()

    def _replaceBold(self, tag: str):
        self._replaceFormat(tag, "<b>?</b>")

    def _replaceItal(self, tag: str):
        self._replaceFormat(tag, "<i>?</i>")
        
    def _replaceBoldItal(self, tag: str):
        self._replaceFormat(tag, "<b><i>?</i></b>")

    def _replaceFormat(self, tag: str, htmlTag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            found = found.group(0)
            text = self.nlParenRegex.search(found)
            if text is None:
                continue

            lines = text.group(0).splitlines()
            size = len(lines)
            if size <= 0:
                return

            htmlText = ""
            for i in range(size - 1):
                if lines[i] == "":
                    continue
                htmlText += htmlTag.replace("?", lines[i]) + "\n"

            htmlText += htmlTag.replace("?", lines[size - 1])

            self.text = self.text.replace(found, htmlText)

    def _processRemove(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
            self.text = self.text.replace(found.group(0), "")

    def _processKeyword(self, line: str) -> tuple[str, str]:
        keyword = self.keywordRegex.search(line)
        if keyword is None:
            return ("", "")
        keyword = keyword.group(0)
        
        if keyword in self.ignoreSet:
            return ("p", line)

        text = self.parenRegex.search(line)
        if text is None:
            return ("", "")
        text = text.group(0)

        return (keyword, text)


class XHtmlPreviewTokenizer(XHtmlTokenizer):
    def __init__(self, text: str, parent: QObject | None) -> None:
        super().__init__(text, parent)
        
        self.ignoreSet = {
            "@tag", "@ref",
            "@pov", "@loc",
        }

        self.removeDict = {
            r"^cpos:.*": self._processRemove,
        }

    def _process(self):
        lines = self.text.splitlines()
        for line in lines:
            if line == "":
                self.tokens.append(("p", "&nbsp;"))
            elif line.startswith("@"):
                token: tuple[str, str] = self._processKeyword(line)
                self.tokens.append(token)
            else:
                self.tokens.append(("p", line))


class XHtmlExportTokenizer(XHtmlTokenizer):
    def __init__(self, text: str, parent: QObject | None) -> None:
        super().__init__(text, parent)

        self.removeDict = {
            r"^cpos:.*": self._processRemove,
            r"^@(tag|ref|pov|loc)(\(.*\))": self._processRemove,
            r"%.*": self._processRemove,
            r"<#(\n|.)*?#>": self._processRemove,
        }

    def _process(self):
        lines = self.text.splitlines()
        for line in lines:
            if line == "":
                continue

            if line.startswith("@"):
                token: tuple[str, str] = self._processKeyword(line)
                self.tokens.append(token)
            else:
                self.tokens.append(("p", line))
