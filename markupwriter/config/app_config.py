#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
    QSize,
)

from markupwriter.util import File
from .base_config import BaseConfig

class AppConfig(BaseConfig):
    INI_PATH: str = None
    APP_NAME: str = None
    ICON_SIZE: QSize = None
    mainWindowSize: QSize  = None
    docTreeViewSize: QSize  = None
    docEditorSize: QSize  = None
    docPreviewSize: QSize  = None
    terminalSize: QSize  = None

    def init():
        AppConfig.INI_PATH = File.path("./resources/configs/app.ini")
        AppConfig.APP_NAME = "Markup Writer"
        AppConfig.ICON_SIZE = QSize(18, 18)
        AppConfig.mainWindowSize = QSize(800, 600)
        AppConfig.docTreeViewSize = QSize(100, 100)
        AppConfig.docEditorSize = QSize(100, 100)
        AppConfig.docPreviewSize = QSize(100, 100)
        AppConfig.terminalSize = QSize(100, 100)

    def reset():
        AppConfig.init()

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