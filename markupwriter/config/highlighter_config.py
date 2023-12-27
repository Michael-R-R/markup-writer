#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
    QDataStream,
)

from PyQt6.QtGui import (
    QColor,
)

from .base_config import BaseConfig

class HighlighterConfig(BaseConfig):
    INI_PATH = QDir.cleanPath("./resources/configs/highlighterConfig.ini")
    # Base-line: 70% lightness, 50% saturation
    refTagCol = QColor(64, 191, 142)
    aliasTagCol = QColor(224, 224, 133)
    commentCol = QColor(128, 128, 128)
    keywordCol = QColor(217, 140, 179)

    def reset():
        HighlighterConfig.refTagCol = QColor(64, 191, 142)
        HighlighterConfig.aliasTagCol = QColor(224, 224, 133)
        HighlighterConfig.commentCol = QColor(128, 128, 128)
        HighlighterConfig.keywordCol = QColor(217, 140, 179)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HighlighterConfig.refTagCol
        sOut << HighlighterConfig.aliasTagCol
        sOut << HighlighterConfig.commentCol
        sOut << HighlighterConfig.keywordCol
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HighlighterConfig.refTagCol
        sIn >> HighlighterConfig.aliasTagCol
        sIn >> HighlighterConfig.commentCol
        sIn >> HighlighterConfig.keywordCol
        return sIn