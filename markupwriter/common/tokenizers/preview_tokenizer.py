#!/usr/bin/python

import re


class PreviewTokenizer(object):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.tokens: list[(str, str)] = list()

        self.tokenPatterns = [
            re.compile(r"^# "),  # title
            re.compile(r"^## "),  # chapter
            re.compile(r"^### "),  # scene
            re.compile(r"^#### "),  # section
        ]

        self.removePatterns = [
            re.compile(r"^@(tag|pov|loc).*", re.MULTILINE),  # tags
            re.compile(r"%.*", re.MULTILINE),  # single line comment
            re.compile(r"<#(\n|.)*?#>", re.MULTILINE),  # multi line comment
        ]

    def run(self) -> list[(str, str)]:
        self._preprocess()

        for line in self.text.splitlines():
            line = line.strip()
            if line == "":
                continue

            if self._processLine(line):
                continue

            self.tokens.append(("p", line))

        return self.tokens

    def _preprocess(self):
        for pattern in self.removePatterns:
            it = pattern.finditer(self.text)
            for found in it:
                self.text = self.text.replace(found.group(0), "")

    def _processLine(self, line: str) -> bool:
        for p in self.tokenPatterns:
            found = p.search(line)
            if found is None:
                continue

            tag = found.group(0).strip()
            text = line[len(tag) :].strip()
            self.tokens.append((tag, text))
            return True

        return False