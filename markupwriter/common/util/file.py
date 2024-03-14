#!/usr/bin/python

from distutils.dir_util import copy_tree

from PyQt6.QtCore import (
    QFile,
    QFileInfo,
    QDir,
    QIODevice,
    QTextStream,
)

class File(object):
    def read(path: str) -> str | None:
        try:
            info = QFile(path)
            if not info.open(QIODevice.OpenModeFlag.ReadOnly):
                return None

            return str(info.readAll(), "utf-8")
        except Exception as e:
            print(str(e))
            return None

    def write(path: str, content: str) -> bool:
        info = QFile(path)
        if not info.open(QIODevice.OpenModeFlag.WriteOnly):
            return False
        
        stream = QTextStream(info)
        stream << content

        return True
    
    def mkdir(path: str) -> bool:
        dir = QDir()
        return dir.mkdir(path)
    
    def cpdir(src: str, dst: str) -> bool:
        try:
            copy_tree(src, dst)
        except Exception as e:
            print(str(e))
            return False
        finally:
            return True
    
    def findAllFiles(path: str) -> list[str]:
        info = QFileInfo(path)
        if not info.isDir():
            return list()
        
        qinfo = QDir(path)
        return qinfo.entryList(QDir.Filter.Files)
    
    def remove(path: str) -> bool:
        return QFile.remove(path)
    
    def exists(path: str) -> bool:
        info = QFile(path)
        return info.exists()
    
    def fileName(path: str) -> str:
        info = QFileInfo(path)
        return info.fileName()
    
    def fileExtension(path: str) -> str | None:
        info = QFileInfo(path)
        if info.isDir():
            return None
        return info.suffix()
