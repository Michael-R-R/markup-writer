#!/usr/bin/python

import re

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
)


class Tokenizer(QObject):
    tokensChanged = pyqtSignal(dict, dict)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)
        self._pattern = re.compile(r"^@(create|import)\s")
        self._prevTokens: dict[str, list[str]] = self._baseDict()

    def tokenize(self, text: str):
        tokens: dict[str, list[str]] = self._baseDict()

        index = text.find("\n")
        while index > -1:
            line = text[: index + 1].strip()
            text = text[index + 1 :]
            index = text.find("\n")

            found = self._pattern.search(line)
            if found is None:
                continue

            tokens[found.group(0)].append(line)

        removed: dict[str, list[str]] = dict()
        for key in self._prevTokens:
            removed[key] = list()
            for line in self._prevTokens[key]:
                if line not in tokens[key]:
                    removed[key].append(line)

        added: dict[str, list[str]] = dict()
        for key in tokens:
            added[key] = list()
            for line in tokens[key]:
                if line not in self._prevTokens[key]:
                    added[key].append(line)

        self._prevTokens = tokens

        self.tokensChanged.emit(removed, added)

    def reset(self):
        self._prevTokens = self._baseDict()

    def _baseDict(self) -> dict:
        return {
            "@create ": list(),
            "@import ": list(),
        }
