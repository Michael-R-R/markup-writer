#!/usr/bin/python

from __future__ import annotations
import re

from collections import Counter

from PyQt6.QtGui import (
    QSyntaxHighlighter,
    QTextDocument,
    QTextCharFormat,
    QColor,
    QBrush,
    QFont,
)

from PyQt6.QtCore import (
    QRegularExpression,
)

from markupwriter.config import HighlighterConfig
from . import BEHAVIOUR

class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument):
        super().__init__(document)

        self.__behaviours: dict[BEHAVIOUR, HighlightBehaviour] = dict()
        self.addBehaviour(BEHAVIOUR.refTag, HighlightWordBehaviour(HighlighterConfig.refTagCol, set(), r"[\w']+"))
        self.addBehaviour(BEHAVIOUR.aliasTag, HighlightWordBehaviour(HighlighterConfig.aliasTagCol, set(), "[a-zA-Z0-9'_]+"))
        self.addBehaviour(BEHAVIOUR.comment, HighlightExprBehaviour(HighlighterConfig.commentCol, r"%(.*)"))
        self.addBehaviour(BEHAVIOUR.keyword, HighlightExprBehaviour(HighlighterConfig.keywordCol, r"@(create|import|as) "))

    def highlightBlock(self, text: str | None) -> None:
        for _, val in self.__behaviours.items():
            val.process(self, text)
    
    def updateFormat(self, start: int, end: int, format: QTextCharFormat):
        self.setFormat(start, end, format)

    def addBehaviour(self, type: BEHAVIOUR, val: HighlightBehaviour) -> bool:
        if type in self.__behaviours:
            return False
        self.__behaviours[type] = val
        return True
    
    def removeBehaviour(self, type: BEHAVIOUR) -> bool:
        if not type in self.__behaviours:
            return False
        self.__behaviours.pop(type)
        return True
    
    def getBehaviour(self, type: BEHAVIOUR) -> HighlightWordBehaviour | HighlightExprBehaviour | None:
        if not type in self.__behaviours:
            return None
        return self.__behaviours[type]


class HighlightBehaviour(object):
    def __init__(self, color: QColor, expr: str):
        self._color = color
        self._format = QTextCharFormat()
        self._expr = expr

        self._format.setFontWeight(QFont.Weight.Bold)
        self._format.setForeground(QBrush(self._color))

    def process(self, highlighter: Highlighter, text: str):
        raise NotImplementedError()
            
    def setColor(self, color: QColor):
        self._color = color
        self._format.setFontWeight(QFont.Weight.Bold)
        self._format.setForeground(QBrush(self._color))

    def setExpression(self, expr: str):
        self._expr = expr
        

class HighlightWordBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, wordSet: set, expr: str):
        super().__init__(color, expr)
        self._wordSet = wordSet

    def process(self, highlighter: Highlighter, text: str):
        wordCounter = Counter(re.findall(self._expr, text))
        for word, _ in wordCounter.items():
            if not word in self._wordSet:
                continue

            start = text.find(word, 0)
            while start > -1:
                length = len(word)
                highlighter.updateFormat(start,
                                         length,
                                         self._format)
                start = text.find(word, start + length)

    def addWord(self, word: str) -> bool:
        if word in self._wordSet:
            return False
        self._wordSet.add(word)
        return True
    
    def removeWord(self, word: str) -> bool:
        if not word in self._wordSet:
            return False
        self._wordSet.remove(word)
        return True
    
    def renameWord(self, old: str, new: str) -> bool:
        if not old in self._wordSet:
            return False
        if new in self._wordSet:
            return False
        self._wordSet.remove(old)
        self._wordSet.add(new)
        return True
    
    def getWords(self) -> set:
        return self._wordSet
    
    def doesExist(self, word: str) -> bool:
        return word in self._wordSet


class HighlightExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str):
        super().__init__(color, expr)
            
    def process(self, highlighter: Highlighter, text: str):
        it = re.finditer(self._expr, text)
        for w in it:
            start = w.start()
            end = w.end() - start
            highlighter.updateFormat(start, end, self._format)