#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
    QDataStream,
    QSize,
)

from .base_config import BaseConfig

class AppConfig(BaseConfig):
    INI_PATH = QDir.cleanPath("./resources/configs/app.ini")
    APP_NAME = "Markup Writer"
    ICON_SIZE = QSize(16, 16)
    mainWindowSize = QSize(800, 600)
    docTreeViewSize = QSize(100, 100)
    docEditorSize = QSize(100, 100)
    docPreviewSize = QSize(100, 100)
    terminalSize = QSize(100, 100)

    def reset():
        pass

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << AppConfig.mainWindowSize
        sOut << AppConfig.docTreeViewSize
        sOut << AppConfig.docEditorSize
        sOut << AppConfig.docPreviewSize
        sOut << AppConfig.terminalSize
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> AppConfig.mainWindowSize
        sIn >> AppConfig.docTreeViewSize
        sIn >> AppConfig.docEditorSize
        sIn >> AppConfig.docPreviewSize
        sIn >> AppConfig.terminalSize
        return sIn