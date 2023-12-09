#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QColor,
)

# TODO fill out colors
class Config:
    charCol = QColor(0, 0, 0)
    locCol = QColor(0, 0, 0)
    commentCol = QColor(0, 0, 0)
    importCol = QColor(0, 0, 0)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << Config.charCol
        sOut << Config.locCol
        sOut << Config.commentCol
        sOut << Config.importCol
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> Config.charCol
        sIn >> Config.locCol
        sIn >> Config.commentCol
        sIn >> Config.importCol
        return sIn