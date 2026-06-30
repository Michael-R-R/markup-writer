#!/usr/bin/python

from __future__ import annotations
from enum import auto, Enum
import enchant, regex

from PyQt6.QtGui import (
    QSyntaxHighlighter,
    QTextDocument,
    QTextCharFormat,
    QColor,
    QBrush,
    QFont,
)

from markupwriter.config import HighlighterConfig
from markupwriter.common.referencetag import RefTagManager


class BEHAVIOUR(Enum):
    paren = 0
    comment = auto()
    multicomment = auto()
    keyword = auto()
    plotKeyword = auto()
    timelineKeyword = auto()
    charKeyword = auto()
    locKeyword = auto()
    objectKeyword = auto()
    underline = auto()
    plotInText = auto()
    tlInText = auto()
    charInText = auto()
    locInText = auto()
    objInText = auto()
    formatting = auto()
    header = auto()
    searchText = auto()
    spellCheck = auto()
    mdHeaders = auto()
    mdLists = auto()


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument | None, refManager: RefTagManager | None, endict: enchant.Dict | None):
        super().__init__(document)

        keywords = "tag|ref|cover|img|vspace|newpage|alignl|alignc|alignr"
        underlineTags = "ref|plot|tl|char|loc|obj"

        parenRegex = r"\(|\)"
        commentRegex = r"%(.*)"
        multiComRegex = [r"<#", r"#>"]
        keywordRegex = r"@({})".format(keywords)
        plotRegex = r"@(plot)"
        timelineRegex = r"@(tl)"
        charRegex = r"@(char)"
        locRegex = r"@(loc)"
        objectRegex = r"@(obj)"
        underlineTagsRegex = r"(?<=@(?:{})\([^()]*?)(?! )([^,()]*\S)(?=\s*(?:,|\)))".format(underlineTags)
        plotInTextRegex = r"(?<=@(?:plot)\([^()]*?)(?! )([^,()]*\S)(?=\s*(?:,|\)))"
        timelineInTextRegex = r"(?<=@(?:tl)\([^()]*?)(?! )([^,()]*\S)(?=\s*(?:,|\)))"
        charInTextRegex = r"(?<=@(?:char)\([^()]*?)(?! )([^,()]*\S)(?=\s*(?:,|\)))"
        locInTextRegex = r"(?<=@(?:loc)\([^()]*?)(?! )([^,()]*\S)(?=\s*(?:,|\)))"
        objInTextRegex = r"(?<=@(?:obj)\([^()]*?)(?! )([^,()]*\S)(?=\s*(?:,|\)))"
        formattingRegex = r"@\b(b|i|bi)\b"
        headerRegex = r"^@(title|chapter|scene|section)"
        mdHeadersRegex = r"^#{1,4}"
        mdListsRegex = r"^(-|\+)"

        self._normalBehaviours: dict[BEHAVIOUR, HighlightBehaviour] = dict()
        self._specialBehaviours: dict[BEHAVIOUR, HighlightBehaviour] = dict()

        if refManager is not None:
            self.addNormalBehaviour(BEHAVIOUR.underline, HighlightUnderlineTagsBehaviour(QColor(255, 255, 255), underlineTagsRegex, refManager))
            self.addNormalBehaviour(BEHAVIOUR.plotInText, HighlightTagsInTextBehaviour(HighlighterConfig.plotCol, plotInTextRegex, refManager))
            self.addNormalBehaviour(BEHAVIOUR.tlInText, HighlightTagsInTextBehaviour(HighlighterConfig.timelineCol, timelineInTextRegex, refManager))
            self.addNormalBehaviour(BEHAVIOUR.charInText, HighlightTagsInTextBehaviour(HighlighterConfig.charCol, charInTextRegex, refManager))
            self.addNormalBehaviour(BEHAVIOUR.locInText, HighlightTagsInTextBehaviour(HighlighterConfig.locCol, locInTextRegex, refManager))
            self.addNormalBehaviour(BEHAVIOUR.objInText, HighlightTagsInTextBehaviour(HighlighterConfig.objectCol, objInTextRegex, refManager))

        if endict is not None:
            self._specialBehaviours[BEHAVIOUR.spellCheck] = HighlightSpellBehaviour(QColor(255, 255, 255), r"(?iu)[\w\']+", endict)

        self.addNormalBehaviour(BEHAVIOUR.paren, HighlightExprBehaviour(HighlighterConfig.parenCol, parenRegex))
        self.addNormalBehaviour(BEHAVIOUR.comment, HighlightExprBehaviour(HighlighterConfig.commentCol, commentRegex))
        self.addNormalBehaviour(BEHAVIOUR.multicomment, HighlightMultiExprBehaviour(HighlighterConfig.commentCol, multiComRegex[0], multiComRegex[1]))
        self.addNormalBehaviour(BEHAVIOUR.keyword, HighlightExprBehaviour(HighlighterConfig.keywordCol, keywordRegex))
        self.addNormalBehaviour(BEHAVIOUR.plotKeyword, HighlightExprBehaviour(HighlighterConfig.plotCol, plotRegex))
        self.addNormalBehaviour(BEHAVIOUR.timelineKeyword, HighlightExprBehaviour(HighlighterConfig.timelineCol, timelineRegex))
        self.addNormalBehaviour(BEHAVIOUR.charKeyword, HighlightExprBehaviour(HighlighterConfig.charCol, charRegex))
        self.addNormalBehaviour(BEHAVIOUR.locKeyword, HighlightExprBehaviour(HighlighterConfig.locCol, locRegex))
        self.addNormalBehaviour(BEHAVIOUR.objectKeyword, HighlightExprBehaviour(HighlighterConfig.objectCol, objectRegex))
        self.addNormalBehaviour(BEHAVIOUR.formatting, HighlightExprBehaviour(HighlighterConfig.formattingCol, formattingRegex))
        self.addNormalBehaviour(BEHAVIOUR.mdHeaders, HighlightExprBehaviour(HighlighterConfig.mdHeadersCol, mdHeadersRegex))
        self.addNormalBehaviour(BEHAVIOUR.mdLists, HighlightExprBehaviour(HighlighterConfig.mdListsCol, mdListsRegex))
        self.addNormalBehaviour(BEHAVIOUR.header, HighlightHeaderBehaviour(HighlighterConfig.headerCol, headerRegex))
        self.addNormalBehaviour(BEHAVIOUR.searchText, HighlightWordBehaviour(QColor(255,255,255), HighlighterConfig.searchedCol, set()))

    def highlightBlock(self, text: str | None) -> None:
        for _, behaviour in self._normalBehaviours.items():
            behaviour.process(self, text)

        for _, behaviour in self._specialBehaviours.items():
            behaviour.process(self, text)

    def addNormalBehaviour(self, type: BEHAVIOUR, val: HighlightBehaviour) -> bool:
        if type in self._normalBehaviours:
            return False
        self._normalBehaviours[type] = val
        return True

    def removeNormalBehaviour(self, type: BEHAVIOUR) -> bool:
        if not type in self._normalBehaviours:
            return False
        self._normalBehaviours.pop(type)
        return True
    
    def toggleNormalBehaviours(self, status: bool):
        for key in self._normalBehaviours:
            b = self._normalBehaviours[key]
            b.isEnabled = status

    def setNormalBehaviourEnable(self, type: BEHAVIOUR, val: bool):
        if not type in self._normalBehaviours:
            return
        self._normalBehaviours[type].isEnabled = val

    def getNormalBehaviour(self, type: BEHAVIOUR) -> HighlightWordBehaviour | None:
        if not type in self._normalBehaviours:
            return None
        return self._normalBehaviours[type]

    def toggleSpellCheckBehaviour(self):
        if self._specialBehaviours[BEHAVIOUR.spellCheck] is None:
            return

        status = self._specialBehaviours[BEHAVIOUR.spellCheck].isEnabled
        self._specialBehaviours[BEHAVIOUR.spellCheck].isEnabled = not status

class HighlightBehaviour(object):
    def __init__(self, color: QColor, expr: str):
        self._expr = regex.compile(expr)
        self.isEnabled = True

        self.format = QTextCharFormat()
        self.format.setForeground(QBrush(color))

    def process(self, highlighter: Highlighter, text: str):
        if not self.isEnabled:
            return

        it = self._expr.finditer(text)
        for w in it:
            start = w.start()
            end = w.end() - start
            highlighter.setFormat(start, end, self.format)

    def getStatus(self) -> bool:
        return self.isEnabled

    def setColor(self, color: QColor):
        self.format.setForeground(QBrush(color))

    def setExpression(self, expr: str):
        self._expr = regex.compile(expr)


class HighlightSpellBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str, enchantDict: enchant.Dict):
        super().__init__(color, expr)
        self.isEnabled = False
        self.format.setUnderlineColor(QColor(255, 0, 0))
        self.format.setUnderlineStyle(
            QTextCharFormat.UnderlineStyle.SpellCheckUnderline
        )
        self.enchantDict = enchantDict

        exclude = "tag|ref|plot|tl|char|loc|obj|cover|img|title|chapter|scene|section"
        self._excludeRegex = regex.compile(r"@({})\(.*?\)".format(exclude))

    def process(self, highlighter: Highlighter, text: str):
        if not self.isEnabled:
            return

        check = self._excludeRegex.search(text)
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
    def __init__(self, color: QColor, bgColor: QColor, wordSet: set):
        super().__init__(color, "")

        self.format.setBackground(bgColor)

        self._wordSet = wordSet

    def process(self, highlighter: Highlighter, text: str):
        if not self.isEnabled:
            return

        for word in self._wordSet:
            it = regex.finditer(word, text)
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


class HighlightUnderlineTagsBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str, refManager: RefTagManager):
        super().__init__(color, expr)

        self._refManager = refManager

        self.format.setUnderlineColor(QColor(255, 255, 255))
        self.format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)

    def process(self, highlighter: Highlighter, text: str):
        if not self.isEnabled:
            return
        
        # underline tags within parentheses
        it = self._expr.finditer(text)
        for w in it:
            word = w.group()
            word = word.strip()
            if not self._refManager.tagExists(word):
                continue

            start = w.start()
            end = w.end() - start
            highlighter.setFormat(start, end, self.format)


class HighlightTagsInTextBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str, refManager: RefTagManager):
        super().__init__(color, expr)

        self._refManager = refManager

        self._excludeRegex = regex.compile(r"@([a-zA-Z1-9].*)\(.*?\)")

        self._fullRegStr = ""

    def process(self, highlighter: Highlighter, text: str):
        if not self.isEnabled:
            return

        allTags = self._expr.findall(text)
        if len(allTags) > 0:
            self._fullRegStr = "|".join(regex.escape(word) for word in allTags if self._refManager.tagExists(word))

        if len(self._fullRegStr) < 1:
            return

        check = self._excludeRegex.search(text)
        if check is not None:
            return

        match = regex.compile(r"\b({})\b".format(self._fullRegStr))
        it = match.finditer(text)
        for w in it:
            start = w.start()
            end = w.end() - start
            highlighter.setFormat(start, end, self.format)


class HighlightExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str):
        super().__init__(color, expr)

    def process(self, highlighter: Highlighter, text: str):
        super().process(highlighter, text)


class HighlightHeaderBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str):
        super().__init__(color, expr)

        self.format.setFontWeight(QFont.Weight.Bold)

    def process(self, highlighter: Highlighter, text: str):
        super().process(highlighter, text)


class HighlightMultiExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str, end: str):
        super().__init__(color, expr)

        self._endExpr = regex.compile(end)

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
