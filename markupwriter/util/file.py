#!/usr/bin/python

from PyQt6.QtCore import (
    QFile,
    QFileInfo,
    QIODevice,
    QTextStream,
)

class File(object):
    def read(path: str) -> str | None:
        info = QFile(path)
        if not info.open(QIODevice.OpenModeFlag.ReadOnly):
            return None

        return str(info.readAll(), "utf-8")

    def write(path: str, content: str) -> bool:
        info = QFile(path)
        if not info.open(QIODevice.OpenModeFlag.WriteOnly):
            return False
        
        stream = QTextStream(info)
        stream << content

        return True
    
    def exists(path: str) -> bool:
        info = QFile(path)
        return info.exists()
    
    def path(path: str) -> str:
        info = QFileInfo(path)
        if info.isDir():
            return info.canonicalPath()
        else:
            return info.canonicalFilePath()
