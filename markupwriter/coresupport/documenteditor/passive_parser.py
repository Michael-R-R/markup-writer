#!/usr/bin/python

import re

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
)

class PassiveParser(QObject):
    tokenAdded = pyqtSignal(str, str)
    tokenRemoved = pyqtSignal(str, str)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        self._pattern = re.compile(r"^@(create|import)\s")
        self._prevParsed: list[(str, str)] = list()

    def tokenize(self, text: str):
        currParsed: list[(str, str)] = list()
        index = 0
        while index > -1:
            index = text.find("\n")
            line = text[:index+1].strip()
            text = text[index+1:]
            if line == "":
                continue

            found = self._pattern.search(line)
            if found is None:
                break

            currParsed.append((found.group(0), line))

        if currParsed == self._prevParsed:
            return

        for prev in self._prevParsed:
            self.tokenRemoved.emit(prev[0], prev[1])

        for curr in currParsed:
            self.tokenAdded.emit(curr[0], curr[1])

        self._prevParsed = currParsed

    def reset(self):
        self._prevParsed.clear()
