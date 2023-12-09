#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
    QDataStream,
    QSize,
)

from PyQt6.QtGui import (
    QColor,
)

from markupwriter.util.serialize import (
    Serialize,
)

def readConfig():
    Serialize.read(AppConfig, AppConfig.INI_PATH)
    Serialize.read(HighlighterConfig, HighlighterConfig.INI_PATH)

def writeConfig():
    Serialize.write(AppConfig.INI_PATH, AppConfig())
    Serialize.write(HighlighterConfig.INI_PATH, HighlighterConfig())


class BaseConfig():
    def reset():
        raise NotImplementedError()

    
class AppConfig(BaseConfig):
    INI_PATH = QDir("./resources/configs/appConfig.ini").absolutePath()
    APP_NAME = "Markup Writer"
    mainWindowSize = QSize(800, 600)
    docTreeSize = QSize(100, 100)
    docEditorSize = QSize(100, 100)
    docPreviewSize = QSize(100, 100)
    terminalSize = QSize(100, 100)

    def reset():
        pass

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << AppConfig.mainWindowSize
        sOut << AppConfig.docTreeSize
        sOut << AppConfig.docEditorSize
        sOut << AppConfig.docPreviewSize
        sOut << AppConfig.terminalSize
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> AppConfig.mainWindowSize
        sIn >> AppConfig.docTreeSize
        sIn >> AppConfig.docEditorSize
        sIn >> AppConfig.docPreviewSize
        sIn >> AppConfig.terminalSize
        return sIn
    

class HighlighterConfig(BaseConfig):
    INI_PATH = QDir("./resources/configs/highlighterConfig.ini").absolutePath()
    # Base-line: 70% lightness, 50% saturation
    refTagCol = QColor(64, 191, 142)
    aliasTagCol = QColor(255, 0, 0) # TODO add color
    commentCol = QColor(121, 210, 121)
    importCol = QColor(217, 140, 179)

    def reset():
        HighlighterConfig.refTagCol = QColor(64, 191, 142)
        HighlighterConfig.aliasTagCol = QColor(255, 0, 0) # TODO add color
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