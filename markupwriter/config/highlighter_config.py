#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QColor,
)

from .base_config import BaseConfig


class HighlighterConfig(BaseConfig):
    INI_PATH: str = None
    parenCol: QColor = None
    commentCol: QColor = None
    formattingCol: QColor = None
    headerCol: QColor = None
    keywordCol: QColor = None
    searchedCol: QColor = None
    mdHeadersCol: QColor = None
    mdListsCol: QColor = None

    def init(wd: str):
        HighlighterConfig.INI_PATH = os.path.join(wd, "resources/configs/highlighter.ini")
        # Base-line: 70% lightness, 50% saturation
        HighlighterConfig.parenCol = QColor(64, 191, 142)
        HighlighterConfig.commentCol = QColor(128, 128, 128)
        HighlighterConfig.formattingCol = QColor(255, 153, 0)
        HighlighterConfig.headerCol = QColor(66, 113, 174)
        HighlighterConfig.keywordCol = QColor(217, 140, 179)
        HighlighterConfig.searchedCol = QColor(255, 153, 0)
        HighlighterConfig.mdHeadersCol = QColor(64, 191, 142)
        HighlighterConfig.mdListsCol = QColor(230, 153, 255)

    def reset(wd: str):
        HighlighterConfig.init(wd)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HighlighterConfig.parenCol
        sOut << HighlighterConfig.commentCol
        sOut << HighlighterConfig.formattingCol
        sOut << HighlighterConfig.headerCol
        sOut << HighlighterConfig.keywordCol
        sOut << HighlighterConfig.searchedCol
        sOut << HighlighterConfig.mdHeadersCol
        sOut << HighlighterConfig.mdListsCol
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HighlighterConfig.parenCol
        sIn >> HighlighterConfig.commentCol
        sIn >> HighlighterConfig.formattingCol
        sIn >> HighlighterConfig.headerCol
        sIn >> HighlighterConfig.keywordCol
        sIn >> HighlighterConfig.searchedCol
        sIn >> HighlighterConfig.mdHeadersCol
        sIn >> HighlighterConfig.mdListsCol
        return sIn
