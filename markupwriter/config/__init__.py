#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QColor,
)

from markupwriter.util.serialize import (
    Serialize,
)

def readConfig():
    Serialize.read(AppConfig, "./resources/config/appConfig.ini")
    Serialize.read(HighlighterConfig, "./resources/config/highlighterConfig.ini")

def writeConfig():
    Serialize.write("./resources/config/appConfig.ini", AppConfig())
    Serialize.write("./resources/config/highlighterConfig.ini", HighlighterConfig())


class BaseConfig():
    def reset():
        raise NotImplementedError()

    
class AppConfig(BaseConfig):
    APP_NAME = "Markup Writer"

    def reset():
        pass

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn
    

class HighlighterConfig(BaseConfig):
    # Base-line: 70% lightness, 50% saturation
    tagsCol = QColor(64, 191, 142)
    commentCol = QColor(121, 210, 121)
    importCol = QColor(217, 140, 179)

    def reset():
        HighlighterConfig.tagsCol = QColor(64, 191, 142)
        HighlighterConfig.commentCol = QColor(121, 210, 121)
        HighlighterConfig.importCol = QColor(217, 140, 179)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << HighlighterConfig.tagsCol
        sOut << HighlighterConfig.commentCol
        sOut << HighlighterConfig.importCol
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> HighlighterConfig.tagsCol
        sIn >> HighlighterConfig.commentCol
        sIn >> HighlighterConfig.importCol
        return sIn