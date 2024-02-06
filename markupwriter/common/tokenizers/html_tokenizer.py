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


class HtmlTokenizer(QRunnable):
    def __init__(self, text: str, parent: QObject | None) -> None:
        super().__init__()
        
        self.text = text
        self.tokens: list[(str, str)] = list() # tag, text
        self.signals = WorkerSignal(parent)

        self.parenRegex = re.compile(r"(?<=\().*?(?=\))")
        self.nlParenRegex = re.compile(r"(?<=\()(\n|.)*?(?=\))")
        self.keywordRegex = re.compile(r"^@.*(?=\()")

        self.replaceDict = {
            r"@bold\((\n|.)*?\)": self._preprocessBold,
            r"@ital\((\n|.)*?\)": self._preprocessItal,
            r"@boldItal\((\n|.)*?\)": self._preprocessBoldItal,
        }

        self.removeDict = {
            r"^cpos:.*": self._preprocessRemove,
            r"^@(tag|ref|pov|loc)(\(.*\))": self._preprocessRemove,
            r"%.*": self._preprocessRemove,
            r"<#(\n|.)*?#>": self._preprocessRemove,
        }

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

    def _preprocessBold(self, tag: str):
        self._preprocessFormat(tag, "<b>?</b>")

    def _preprocessItal(self, tag: str):
        self._preprocessFormat(tag, "<i>?</i>")

    def _preprocessBoldItal(self, tag: str):
        self._preprocessFormat(tag, "<b><i>?</i></b>")

    def _preprocessFormat(self, tag: str, htmlTag: str):
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
            for i in range(size-1):
                if lines[i] == "":
                    continue
                htmlText += htmlTag.replace("?", lines[i]) + "\n"
                
            htmlText += htmlTag.replace("?", lines[size-1])
                
            self.text = self.text.replace(found, htmlText)

    def _preprocessRemove(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
            self.text = self.text.replace(found.group(0), "")

    def _process(self):
        lines = self.text.splitlines()
        for line in lines:
            if line == "":
                continue

            if line.startswith("@"):
                token: (str, str) = self._processKeyword(line)
                self.tokens.append(token)
            else:
                self.tokens.append(("p", line))
                
    def _processKeyword(self, line: str) -> (str, str):
        keyword = self.keywordRegex.search(line)
        if keyword is None:
            return ("", "")
        keyword = keyword.group(0)
        
        text = self.parenRegex.search(line)
        if text is None:
            return ("", "")
        text = text.group(0)
        
        return (keyword, text)
