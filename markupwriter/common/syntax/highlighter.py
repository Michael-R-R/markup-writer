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

from markupwriter.config import (
    HighlighterConfig,
)


class BEHAVIOUR(Enum):
    paren = 0
    comment = auto()
    multicomment = auto()
    italize = auto()
    bold = auto()
    italBold = auto()
    header1 = auto()
    header2 = auto()
    header3 = auto()
    header4 = auto()
    tags = auto()
    keyword = auto()


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument | None):
        super().__init__(document)

        parenRegex = r"\(|\)"
        commentRegex = r"%(.*)"
        multiComRegex = [r"<#", r"#>"]
        tagsRegex = r"^@(tag|ref|pov|loc)"
        keywordRegex = r"@(r)"
        boldRegex = r"\*(.+?)\*(?!\*)"
        italRegex = r"_(.+?)_(?!_)"
        italBoldRegex = r"\^(.+?)\^(?!\^)"
        headerRegex = [r"^# .*", r"^## .*", r"^### .*", r"^#### .*"]

        self._behaviours: dict[BEHAVIOUR, HighlightBehaviour] = dict()

        self.addBehaviour(
            BEHAVIOUR.paren,
            HighlightExprBehaviour(HighlighterConfig.parenCol, parenRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.comment,
            HighlightExprBehaviour(HighlighterConfig.commentCol, commentRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.tags,
            HighlightExprBehaviour(HighlighterConfig.tagsCol, tagsRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.keyword,
            HighlightExprBehaviour(HighlighterConfig.tagsCol, keywordRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.multicomment,
            HighlightMultiExprBehaviour(
                HighlighterConfig.commentCol, multiComRegex[0], multiComRegex[1]
            ),
        )

        # Header behaviours
        self.addHeaderBehaviour(BEHAVIOUR.header1, headerRegex[0], 34.0)
        self.addHeaderBehaviour(BEHAVIOUR.header2, headerRegex[1], 24.0)
        self.addHeaderBehaviour(BEHAVIOUR.header3, headerRegex[2], 18.72)
        self.addHeaderBehaviour(BEHAVIOUR.header4, headerRegex[3], 16.0)

        # Italize behaviour
        italBehaviour = HighlightExprBehaviour(HighlighterConfig.boldCol, italRegex)
        italBehaviour.format.setFontItalic(True)
        self.addBehaviour(BEHAVIOUR.italize, italBehaviour)

        # Bold behaviour
        boldBehaviour = HighlightExprBehaviour(HighlighterConfig.boldCol, boldRegex)
        boldBehaviour.format.setFontWeight(QFont.Weight.Bold)
        self.addBehaviour(BEHAVIOUR.bold, boldBehaviour)

        # Italize+Bold behaviour
        italBoldBehaviour = HighlightExprBehaviour(
            HighlighterConfig.italBoldCol, italBoldRegex
        )
        italBoldBehaviour.format.setFontWeight(QFont.Weight.Bold)
        italBoldBehaviour.format.setFontItalic(True)
        self.addBehaviour(BEHAVIOUR.italBold, italBoldBehaviour)

    def highlightBlock(self, text: str | None) -> None:
        for _, val in self._behaviours.items():
            val.process(self, text)

    def addHeaderBehaviour(self, behaviour: BEHAVIOUR, expr: str, size: float):
        header = HighlightExprBehaviour(QColor(), expr)
        format = QTextCharFormat()
        format.setFontWeight(QFont.Weight.Bold)
        format.setForeground(QBrush(HighlighterConfig.headerCol))
        format.setFontPointSize(size)
        header.format = format
        self.addBehaviour(behaviour, header)

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
        self._expr = re.compile(expr)

        self.format = QTextCharFormat()
        self.format.setForeground(QBrush(color))

    def process(self, highlighter: Highlighter, text: str):
        raise NotImplementedError()

    def setColor(self, color: QColor):
        self.format.setForeground(QBrush(color))

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

            word = "\\b{}\\b".format(word)
            it = re.finditer(word, text)
            for m in it:
                start = m.start()
                end = m.end() - start
                highlighter.setFormat(start, end, self.format)

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

    def clear(self):
        self._wordSet.clear()

    def exist(self, word: str) -> bool:
        return word in self._wordSet


class HighlightExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str):
        super().__init__(color, expr)

    def process(self, highlighter: Highlighter, text: str):
        it = self._expr.finditer(text)
        for w in it:
            start = w.start()
            end = w.end() - start
            highlighter.setFormat(start, end, self.format)


class HighlightMultiExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str, end: str):
        super().__init__(color, expr)

        self._endExpr = re.compile(end)

    def process(self, highlighter: Highlighter, text: str):
        highlighter.setCurrentBlockState(0)

        startIndex = 0
        if highlighter.previousBlockState() != 1:
            startIndex = text.find(self._expr.pattern)

        while startIndex > -1:
            endMatch = self._endExpr.search(text, startIndex)
            endIndex = -1 if endMatch is None else endMatch.start()
            multiLength = 0

            if endIndex < 0:
                highlighter.setCurrentBlockState(1)
                multiLength = len(text) - startIndex
            else:
                multiLength = (
                    endIndex - startIndex + (endMatch.end() - endMatch.start())
                )

            highlighter.setFormat(startIndex, multiLength, self.format)

            startIndex = text.find(self._expr.pattern, startIndex + multiLength)
