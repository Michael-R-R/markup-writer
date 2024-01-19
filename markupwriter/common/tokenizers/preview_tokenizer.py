#!/usr/bin/python

import re
from typing import Iterator


class PreviewTokenizer(object):
    def __init__(self, text: str) -> None:
        self.text = text
        self.tokens: list[(str, str)] = list()
        
        self.tokenPatterns = [
            re.compile(r"^# "),  # title
            re.compile(r"^## "),  # chapter
            re.compile(r"^### "),  # scene
            re.compile(r"^#### "),  # section
        ]
        
        self.removePatterns = [
            re.compile(r"^@(tag|pov|loc).*"),  # tags
            re.compile(r"%.*"),  # single line comment
            re.compile(r"<#(\n|.)*?#>"),  # multi line comment
        ]

    def run(self):
        self._preprocess()

        for line in self.text.splitlines():
            line = line.strip()
            if line == "":
                continue

            if self._processLine(line):
                continue

            self.tokens.append(("p", line))

    def _preprocess(self):
        for pattern in self.removePatterns:
            it = pattern.finditer(self.text)
            for found in it:
                self.text = self.text.replace(found.group(0), "")

        # TODO preprocess text formatting

    def _processLine(self, line: str) -> bool:
        for p in self.tokenPatterns:
            found = p.search(line)
            if found is None:
                continue

            tag = found.group(0)
            text = line[len(tag) :].strip()
            self.tokens.append((tag, text))
            return True

        return False
