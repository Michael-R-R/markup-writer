#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QColor,
)

# Base-line: 70% lightness, 50% saturation
class Config:
    tagsCol = QColor(64, 191, 142)
    commentCol = QColor(121, 210, 121)
    importCol = QColor(217, 140, 179)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << Config.tagsCol
        sOut << Config.commentCol
        sOut << Config.importCol
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> Config.tagsCol
        sIn >> Config.commentCol
        sIn >> Config.importCol
        return sIn