#!/usr/bin/python

from __future__ import annotations
from enum import auto, Enum
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
    bold = auto()
    italize = auto()
    boldItal = auto()
    header = auto()
    tags = auto()
    keyword = auto()
    searchText = auto()


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument | None):
        super().__init__(document)

        parenRegex = r"\(|\)"
        commentRegex = r"%(.*)"
        multiComRegex = [r"<#", r"#>"]
        tagsRegex = r"^@(tag|ref|pov|loc)"
        keywordRegex = r"@(r)"
        boldRegex = r"@bold"
        italRegex = r"@ital"
        boldItalRegex = r"@boldItal"
        headerRegex = r"^#{1,4} .*"

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

        # Header behaviour
        headerBehaviour = HighlightExprBehaviour(
            HighlighterConfig.headerCol, headerRegex
        )
        headerBehaviour.format.setFontWeight(QFont.Weight.Bold)
        self.addBehaviour(BEHAVIOUR.header, headerBehaviour)

        # Bold behaviour
        boldBehaviour = HighlightExprBehaviour(HighlighterConfig.boldCol, boldRegex)
        boldBehaviour.format.setFontWeight(QFont.Weight.Bold)
        self.addBehaviour(BEHAVIOUR.bold, boldBehaviour)

        # Italize behaviour
        italBehaviour = HighlightExprBehaviour(HighlighterConfig.boldCol, italRegex)
        italBehaviour.format.setFontItalic(True)
        self.addBehaviour(BEHAVIOUR.italize, italBehaviour)
        
        # Bold+Italize behaviour
        boldItalBehaviour = HighlightExprBehaviour(HighlighterConfig.boldCol, boldItalRegex)
        boldItalBehaviour.format.setFontWeight(QFont.Weight.Bold)
        boldItalBehaviour.format.setFontItalic(True)
        self.addBehaviour(BEHAVIOUR.boldItal, boldItalBehaviour)

        # Searched word
        searchedWordBehaviour = HighlightWordBehaviour(QColor(255, 255, 255), set())
        searchedWordBehaviour.format.setBackground(HighlighterConfig.searchedCol)
        self.addBehaviour(BEHAVIOUR.searchText, searchedWordBehaviour)

    def highlightBlock(self, text: str | None) -> None:
        for _, val in self._behaviours.items():
            val.process(self, text)

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
    ) -> (
        HighlightWordBehaviour
        | HighlightExprBehaviour
        | HighlightMultiExprBehaviour
        | None
    ):
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
    def __init__(self, color: QColor, wordSet: set):
        super().__init__(color, "")
        self._wordSet = wordSet

    def process(self, highlighter: Highlighter, text: str):
        for word in self._wordSet:
            it = re.finditer(word, text)
            for found in it:
                start = found.start()
                end = found.end() - start
                highlighter.setFormat(start, end, self.format)

    def add(self, word: str) -> bool:
        if word in self._wordSet:
            return False
        self._wordSet.add(word)
        return True

    def remove(self, word: str) -> bool:
        if not word in self._wordSet:
            return False
        self._wordSet.remove(word)
        return True

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
