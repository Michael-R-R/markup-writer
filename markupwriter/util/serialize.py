#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream, 
    QFile, 
    QIODevice,
)

from typing import (
    TypeVar,
    Type,
)

class Serialize(object):
    T = TypeVar('T')

    _qtVersion = QDataStream.Version.Qt_6_6
    _masterFormat = 0x00000001
    _masterVersion = 1

    def read(type: Type[T], path: str) -> T | None:
        inFile = QFile(path)
        if not inFile.open(QIODevice.OpenModeFlag.ReadOnly):
            return None
        
        inStream = QDataStream(inFile)

        # Check if the format is supported
        format = inStream.readInt()
        if format != Serialize._masterFormat:
            return None
        
        # Check if the version is supported
        version = inStream.readInt()
        if version != Serialize._masterVersion:
            return None
        
        inStream.setVersion(Serialize._qtVersion)

        obj = type()
        inStream >> obj

        inFile.close()

        return obj

    def write(path: str, data) -> bool:
        outFile = QFile(path)
        if not outFile.open(QIODevice.OpenModeFlag.WriteOnly):
            return False
        
        outStream = QDataStream(outFile)
        outStream.writeInt(Serialize._masterFormat)
        outStream.writeInt(Serialize._masterVersion)
        outStream.setVersion(Serialize._qtVersion)
        outStream << data

        outFile.close()

        return True
