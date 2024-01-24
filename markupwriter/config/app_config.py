#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QDataStream,
    QSize,
)

from .base_config import BaseConfig


class AppConfig(BaseConfig):
    WORKING_DIR: str = None
    INI_PATH: str = None
    APP_NAME: str = None
    APP_EXTENSION: str = None
    ICON_SIZE: QSize = None
    projectName: str = None
    projectDir: str = None
    mainWindowSize: QSize = None
    docTreeSize: QSize = None
    docEditorSize: QSize = None
    docPreviewSize: QSize = None
    consoleSize: QSize = None

    def init(wd: str):
        if AppConfig.WORKING_DIR is None:
            AppConfig.WORKING_DIR = wd
        
        AppConfig.INI_PATH = os.path.join(wd, "resources/configs/app.ini")
        AppConfig.APP_NAME = "Markup Writer"
        AppConfig.APP_EXTENSION = ".mwf"
        AppConfig.ICON_SIZE = QSize(18, 18)
        AppConfig.mainWindowSize = QSize(800, 600)
        AppConfig.docTreeSize = QSize(100, 100)
        AppConfig.docEditorSize = QSize(100, 100)
        AppConfig.docPreviewSize = QSize(100, 100)
        AppConfig.consoleSize = QSize(100, 100)

    def reset():
        AppConfig.init()

    def hasActiveProject() -> bool:
        return AppConfig.projectDir is not None

    def fullWindowTitle() -> str:
        return "{} - {}".format(AppConfig.APP_NAME, AppConfig.projectName)

    def projectFilePath() -> str | None:
        if AppConfig.projectDir is None:
            return None
        return os.path.join(AppConfig.projectDir, AppConfig.projectName)

    def projectContentPath() -> str | None:
        if AppConfig.projectDir is None:
            return None
        return os.path.join(AppConfig.projectDir, "data/content/")

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << AppConfig.mainWindowSize
        sOut << AppConfig.docTreeSize
        sOut << AppConfig.docEditorSize
        sOut << AppConfig.docPreviewSize
        sOut << AppConfig.consoleSize
        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> AppConfig.mainWindowSize
        sIn >> AppConfig.docTreeSize
        sIn >> AppConfig.docEditorSize
        sIn >> AppConfig.docPreviewSize
        sIn >> AppConfig.consoleSize
        return sIn
