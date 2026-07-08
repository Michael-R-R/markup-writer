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
    
    mainWindowSize: QSize = None
    docTreeSize: QSize = None
    docEditorSize: QSize = None
    docPreviewSize: QSize = None
    consoleSize: QSize = None
    openedRecently: [] = None

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
        AppConfig.openedRecently = []

    def reset(wd: str):
        AppConfig.init(wd)

    def mkWindowTitle(projectName: str | None) -> str:
        return "{} - {}".format(AppConfig.APP_NAME, projectName)

    def updateOpenRecently(path: str):
        path = path.strip()

        try:
            AppConfig.openedRecently.remove(path)
        except:
            print(path, "not in opened recently list")

        size = len(AppConfig.openedRecently)
        if size < 5:
            AppConfig.openedRecently.insert(0, path)
        else:
            AppConfig.openedRecently.insert(0, path)
            AppConfig.openedRecently.pop()

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut << AppConfig.mainWindowSize
        sOut << AppConfig.docTreeSize
        sOut << AppConfig.docEditorSize
        sOut << AppConfig.docPreviewSize
        sOut << AppConfig.consoleSize

        sOut.writeInt(len(AppConfig.openedRecently))
        for path in AppConfig.openedRecently:
            sOut.writeQString(path)

        return sOut

    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        sIn >> AppConfig.mainWindowSize
        sIn >> AppConfig.docTreeSize
        sIn >> AppConfig.docEditorSize
        sIn >> AppConfig.docPreviewSize
        sIn >> AppConfig.consoleSize

        recentlyOpenedSize = sIn.readInt()
        for _ in range(recentlyOpenedSize):
            path = sIn.readQString()
            AppConfig.openedRecently.append(path)

        return sIn
