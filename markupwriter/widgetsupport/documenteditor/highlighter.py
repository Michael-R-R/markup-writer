#!/usr/bin/python

from __future__ import annotations

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

from markupwriter.config.config_highlighter import (
    Config,
)

class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument):
        super().__init__(document)

        self.__behaviours: dict[str, HighlightBehaviour] = dict()
        self.addBehaviour("char-tags", HighlightWordBehaviour(Config.charCol, {}, "[A-Za-z0-9]+"))
        self.addBehaviour("loc-tags", HighlightWordBehaviour(Config.locCol, {}, "[A-Za-z0-9]+"))
        self.addBehaviour("comment-tag", HighlightExprBehaviour(Config.commentCol, "%(.*)"))
        self.addBehaviour("import-tag", HighlightExprBehaviour(Config.importCol, "^@(char|loc)\\:"))

    def highlightBlock(self, text: str | None) -> None:
        for _, val in self.__behaviours.items():
            val.process(self, text)
    
    def updateFormat(self, start: int, end: int, format: QTextCharFormat):
        self.setFormat(start, end, format)

    def addBehaviour(self, key: str, val: HighlightBehaviour) -> bool:
        if key in self.__behaviours:
            return False
        self.__behaviours[key] = val
        return True
    
    def removeBehaviour(self, key: str) -> bool:
        if not key in self.__behaviours:
            return False
        self.__behaviours.pop(key)
        return True
    
    def getBehaviour(self, key: str) -> HighlightWordBehaviour | HighlightExprBehaviour | None:
        if not key in self.__behaviours:
            return None
        return self.__behaviours[key]


class HighlightBehaviour(object):
    def __init__(self, color: QColor, expr: str):
        self._color = color
        self._format = QTextCharFormat()
        self._expression = QRegularExpression(expr)

        self._format.setFontWeight(QFont.Weight.Bold)
        self._format.setForeground(QBrush(self._color))

    def process(self, highlighter: Highlighter, text: str):
        raise NotImplementedError()
            
    def setColor(self, color: QColor):
        self._color = color
        self._format.setFontWeight(QFont.Weight.Bold)
        self._format.setForeground(QBrush(self._color))

    def setExpression(self, expr: str):
        self._expression = QRegularExpression(expr)
        

class HighlightWordBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, wordSet: set, expr: str):
        super().__init__(color, expr)
        self._wordSet = wordSet

    def process(self, highlighter: Highlighter, text: str):
        it = self._expression.globalMatch(text)
        while it.hasNext():
            match = it.next()
            if not match.captured(0) in self._wordSet:
                continue
            
            highlighter.updateFormat(match.capturedStart(),
                                     match.capturedLength(),
                                     self._format)
            
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


class HighlightExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, expr: str):
        super().__init__(color, expr)
            
    def process(self, highlighter: Highlighter, text: str):
        it = self._expression.globalMatch(text)
        while it.hasNext():
            match = it.next()
            if not match.captured(0) in text:
                return
            
            highlighter.updateFormat(match.capturedStart(),
                                     match.capturedLength(),
                                     self._format)