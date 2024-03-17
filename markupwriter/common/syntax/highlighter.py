#!/usr/bin/python

from __future__ import annotations
from enum import auto, Enum
import re, enchant

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
    keyword = auto()
    formatting = auto()
    header = auto()
    searchText = auto()
    spellCheck = auto()
    mdHeaders = auto()
    mdLists = auto()


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument | None, endict: enchant.Dict | None):
        super().__init__(document)

        parenRegex = r"\(|\)"
        commentRegex = r"%(.*)"
        multiComRegex = [r"<#", r"#>"]
        keywordRegex = r"@(tag|ref|pov|loc|img|vspace|newpage|alignl|alignc|alignr)"
        formattingRegex = r"@\b(b|i)\b"
        headerRegex = r"^@(title|chapter|scene|section)"
        mdHeadersRegex = r"^#{1,4}"
        mdListsRegex = r"^(-|\+)"

        self._behaviours: dict[BEHAVIOUR, HighlightBehaviour] = dict()

        if endict is not None:
            self.addBehaviour(
                BEHAVIOUR.spellCheck,
                HighlightSpellBehaviour(QColor(255, 255, 255), r"(?iu)[\w\']+", endict),
            )

        self.addBehaviour(
            BEHAVIOUR.paren,
            HighlightExprBehaviour(HighlighterConfig.parenCol, parenRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.comment,
            HighlightExprBehaviour(HighlighterConfig.commentCol, commentRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.multicomment,
            HighlightMultiExprBehaviour(
                HighlighterConfig.commentCol, multiComRegex[0], multiComRegex[1]
            ),
        )

        self.addBehaviour(
            BEHAVIOUR.keyword,
            HighlightExprBehaviour(HighlighterConfig.keywordCol, keywordRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.formatting,
            HighlightExprBehaviour(HighlighterConfig.formattingCol, formattingRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.mdHeaders,
            HighlightExprBehaviour(HighlighterConfig.mdHeadersCol, mdHeadersRegex),
        )

        self.addBehaviour(
            BEHAVIOUR.mdLists,
            HighlightExprBehaviour(HighlighterConfig.mdListsCol, mdListsRegex),
        )

        # Headers
        headerBehaviour = HighlightExprBehaviour(
            HighlighterConfig.headerCol, headerRegex
        )
        headerBehaviour.format.setFontWeight(QFont.Weight.Bold)
        self.addBehaviour(BEHAVIOUR.header, headerBehaviour)

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
    
    def toggleBehaviours(self):
        for key in self._behaviours:
            b = self._behaviours[key]
            b.isEnabled = not b.isEnabled

    def setBehaviourEnable(self, type: BEHAVIOUR, val: bool):
        if not type in self._behaviours:
            return
        self._behaviours[type].isEnabled = val

    def getBehaviour(
        self, type: BEHAVIOUR
    ) -> (
        HighlightWordBehaviour
        | HighlightSpellBehaviour
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
        self.isEnabled = True

        self.format = QTextCharFormat()
        self.format.setForeground(QBrush(color))

    def process(self, highlighter: Highlighter, text: str):
        raise NotImplementedError()

    def setColor(self, color: QColor):
        self.format.setForeground(QBrush(color))

    def setExpression(self, expr: str):
        self._expr = re.compile(expr)


class HighlightSpellBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str, enchantDict: enchant.Dict):
        super().__init__(color, expr)
        self.format.setUnderlineColor(QColor(255, 0, 0))
        self.format.setUnderlineStyle(
            QTextCharFormat.UnderlineStyle.SpellCheckUnderline
        )
        self.enchantDict = enchantDict

        exclude = "tag|ref|pov|loc|img|title|chapter|scene|section"
        self.excludeRegex = re.compile(r"@({})\(.*?\)".format(exclude))

    def process(self, highlighter: Highlighter, text: str):
        if not self.isEnabled:
            return

        check = self.excludeRegex.search(text)
        if check is not None:
            return

        it = self._expr.finditer(text)
        for found in it:
            if self.enchantDict.check(found.group(0)):
                continue
            start = found.start()
            end = found.end() - start
            highlighter.setFormat(start, end, self.format)


class HighlightWordBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, wordSet: set):
        super().__init__(color, "")
        self._wordSet = wordSet

    def process(self, highlighter: Highlighter, text: str):
        if not self.isEnabled:
            return

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
        if not self.isEnabled:
            return

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
        if not self.isEnabled:
            return

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
