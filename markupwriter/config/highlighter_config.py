#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QColor,
)

from .base_config import BaseConfig


class HighlighterConfig(BaseConfig):
    INI_PATH: str = None
    sqBracketCol: QColor = None
    commentCol: QColor = None
    italizeCol: QColor = None
    boldCol: QColor = None
    italBoldCol: QColor = None
    headerCol: QColor = None
    tagsCol: QColor = None

    def init():
        HighlighterConfig.INI_PATH = "./resources/configs/highlighter.ini"
        # Base-line: 70% lightness, 50% saturation
        HighlighterConfig.sqBracketCol = QColor(64, 191, 142)
        HighlighterConfig.commentCol = QColor(128, 128, 128)
        HighlighterConfig.italizeCol = QColor(255, 153, 0)
        HighlighterConfig.boldCol = QColor(255, 153, 0)
        HighlighterConfig.italBoldCol = QColor(255, 153, 0)
        HighlighterConfig.headerCol = QColor(66, 113, 174)
        HighlighterConfig.tagsCol = QColor(217, 140, 179)

    def reset():
        HighlighterConfig.init()

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HighlighterConfig.sqBracketCol
        sOut << HighlighterConfig.commentCol
        sOut << HighlighterConfig.italizeCol
        sOut << HighlighterConfig.boldCol
        sOut << HighlighterConfig.italBoldCol
        sOut << HighlighterConfig.headerCol
        sOut << HighlighterConfig.tagsCol
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HighlighterConfig.sqBracketCol
        sIn >> HighlighterConfig.commentCol
        sIn >> HighlighterConfig.italizeCol
        sIn >> HighlighterConfig.boldCol
        sIn >> HighlighterConfig.italBoldCol
        sIn >> HighlighterConfig.headerCol
        sIn >> HighlighterConfig.tagsCol
        return sIn
