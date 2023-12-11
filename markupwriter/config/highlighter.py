#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
    QDataStream,
)

from PyQt6.QtGui import (
    QColor,
)

from .base import BaseConfig

class HighlighterConfig(BaseConfig):
    INI_PATH = QDir("./resources/configs/highlighterConfig.ini").absolutePath()
    # Base-line: 70% lightness, 50% saturation
    refTagCol = QColor(64, 191, 142)
    aliasTagCol = QColor(224, 224, 133)
    commentCol = QColor(121, 210, 121)
    importCol = QColor(217, 140, 179)

    def reset():
        HighlighterConfig.refTagCol = QColor(64, 191, 142)
        HighlighterConfig.aliasTagCol = QColor(224, 224, 133)
        HighlighterConfig.commentCol = QColor(121, 210, 121)
        HighlighterConfig.importCol = QColor(217, 140, 179)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HighlighterConfig.refTagCol
        sOut << HighlighterConfig.aliasTagCol
        sOut << HighlighterConfig.commentCol
        sOut << HighlighterConfig.importCol
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HighlighterConfig.refTagCol
        sIn >> HighlighterConfig.aliasTagCol
        sIn >> HighlighterConfig.commentCol
        sIn >> HighlighterConfig.importCol
        return sIn