#!/usr/bin/python

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

class Highlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument):
        super().__init__(document)

        self.__behaviours: list[HighlightBehaviour] = list()

        self.__behaviours.append(HighlightWordBehaviour(QColor(255, 0, 0), {"hi", "hello", "hola"}, "\\b[A-Za-z_]+\\b"))
        self.__behaviours.append(HighlightWordBehaviour(QColor(0, 255, 0), {"bye", "goodbye"}, "\\b[A-Za-z_]+\\b"))
        self.__behaviours.append(HighlightExprBehaviour(QColor(0, 0, 255), "^@import(.*?):"))

    def highlightBlock(self, text: str | None) -> None:
        for i in self.__behaviours:
            i.process(self, text)
    
    def updateFormat(self, start: int, end: int, format: QTextCharFormat):
        self.setFormat(start, end, format)

    def updateCurrentBlockState(self, state: int):
        self.setCurrentBlockState(state)


class HighlightBehaviour(object):
    def __init__(self, color: QColor):
        self._color = color
        self._format = QTextCharFormat()

        self._format.setFontWeight(QFont.Weight.Bold)
        self._format.setForeground(QBrush(self._color))

    def process(self, highlighter: Highlighter, text: str):
        raise NotImplementedError()
        

class HighlightWordBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, wordSet: set, expr: str):
        super().__init__(color)
        self._wordSet = wordSet
        self._expression = QRegularExpression(expr)

    def process(self, highlighter: Highlighter, text: str):
        it = self._expression.globalMatch(text)
        while it.hasNext():
            match = it.next()
            if not match.captured(0) in self._wordSet:
                continue
            
            highlighter.updateFormat(match.capturedStart(),
                                     match.capturedLength(),
                                     self._format)
            
class HighlightExprBehaviour(HighlightBehaviour):
    def __init__(self, color: QColor, start: str):
        super().__init__(color)
        self._expression = QRegularExpression(start)

    def process(self, highlighter: Highlighter, text: str):
        it = self._expression.globalMatch(text)
        while it.hasNext():
            match = it.next()
            if not match.captured(0) in text:
                return
            
            highlighter.updateFormat(match.capturedStart(),
                                     match.capturedLength(),
                                     self._format)