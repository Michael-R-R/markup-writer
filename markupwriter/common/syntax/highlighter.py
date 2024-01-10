#!/usr/bin/python

from __future__ import annotations
from enum import auto, Enum
from collections import Counter
import re

from PyQt6.QtGui import (
    QSyntaxHighlighter,
    QTextDocument,
    QTextCharFormat,
    QColor,
    QBrush,
    QFont,
)

from markupwriter.common.config import (
    HighlighterConfig,
)


class BEHAVIOUR(Enum):
    refTag = 0
    aliasTag = auto()
    comment = auto()
    keyword = auto()


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument):
        super().__init__(document)

        self._behaviours: dict[BEHAVIOUR, HighlightBehaviour] = dict()
        self.addBehaviour(
            BEHAVIOUR.refTag,
            HighlightWordBehaviour(HighlighterConfig.refTagCol, set(), r"[\w']+"),
        )
        self.addBehaviour(
            BEHAVIOUR.aliasTag,
            HighlightWordBehaviour(HighlighterConfig.aliasTagCol, set(), r"[\w']+"),
        )
        self.addBehaviour(
            BEHAVIOUR.comment,
            HighlightExprBehaviour(HighlighterConfig.commentCol, r"%(.*)"),
        )
        self.addBehaviour(
            BEHAVIOUR.keyword,
            HighlightExprBehaviour(
                HighlighterConfig.keywordCol, r"@(create|import|as) "
            ),
        )

    def highlightBlock(self, text: str | None) -> None:
        for _, val in self._behaviours.items():
            val.process(self, text)

    def updateFormat(self, start: int, end: int, format: QTextCharFormat):
        self.setFormat(start, end, format)

    def addBehaviour(self, type: BEHAVIOUR, val: HighlightBehaviour) -> bool:
        if type in self._behaviours:
            return False
        self._behaviours[type] = val
        return True

    def removeBehaviour(self, type: BEHAVIOUR) -> bool:
        if not type in self._behaviours:
            return False
        self._behaviours.pop(type)
        return True

    def getBehaviour(
        self, type: BEHAVIOUR
    ) -> HighlightWordBehaviour | HighlightExprBehaviour | None:
        if not type in self._behaviours:
            return None
        return self._behaviours[type]


class HighlightBehaviour(object):
    def __init__(self, color: QColor, expr: str):
        self._color = color
        self._format = QTextCharFormat()
        self._expr = re.compile(expr)

        self._format.setFontWeight(QFont.Weight.Bold)
        self._format.setForeground(QBrush(self._color))

    def process(self, highlighter: Highlighter, text: str):
        raise NotImplementedError()

    def setColor(self, color: QColor):
        self._color = color
        self._format.setFontWeight(QFont.Weight.Bold)
        self._format.setForeground(QBrush(self._color))

    def setExpression(self, expr: str):
        self._expr = re.compile(expr)


class HighlightWordBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, wordSet: set, expr: str):
        super().__init__(color, expr)
        self._wordSet = wordSet

    def process(self, highlighter: Highlighter, text: str):
        wordCounter = Counter(self._expr.findall(text))
        for word, _ in wordCounter.items():
            if not word in self._wordSet:
                continue

            word = r"\b" + word + r"\b"
            it = re.finditer(word, text)
            for m in it:
                start = m.start()
                end = m.end() - start
                highlighter.updateFormat(start, end, self._format)

    def add(self, word: str) -> bool:
        if word in self._wordSet:
            return False
        self._wordSet.add(word)
        return True

    def addList(self, words: list[str]):
        for word in words:
            self.add(word)

    def remove(self, word: str) -> bool:
        if not word in self._wordSet:
            return False
        self._wordSet.remove(word)
        return True

    def removeList(self, words: list[str]):
        for word in words:
            self.remove(word)

    def rename(self, old: str, new: str) -> bool:
        if not old in self._wordSet:
            return False
        if new in self._wordSet:
            return False
        self._wordSet.remove(old)
        self._wordSet.add(new)
        return True

    def clear(self):
        self._wordSet.clear()

    def getWords(self) -> set:
        return self._wordSet

    def doesExist(self, word: str) -> bool:
        return word in self._wordSet


class HighlightExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str):
        super().__init__(color, expr)

    def process(self, highlighter: Highlighter, text: str):
        it = self._expr.finditer(text)
        for w in it:
            start = w.start()
            end = w.end() - start
            highlighter.updateFormat(start, end, self._format)
