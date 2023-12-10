#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream, 
    QFile, 
    QIODevice,
)

from typing import (
    TypeVar,
    Type
)

T = TypeVar('T')

__qtVersion = QDataStream.Version.Qt_6_6
__masterFormat = 0x00000001
__masterVersion = 1

def serialize(path: str, data) -> bool:
    outFile = QFile(path)
    if not outFile.open(QIODevice.OpenModeFlag.WriteOnly):
        return False
    
    outStream = QDataStream(outFile)
    outStream.writeInt(__masterFormat)
    outStream.writeInt(__masterVersion)
    outStream.setVersion(__qtVersion)
    outStream << data

    outFile.close()

    return True

def deserialize(classType: Type[T], path: str) -> T | None:
    inFile = QFile(path)
    if not inFile.open(QIODevice.OpenModeFlag.ReadOnly):
        return None
    
    inStream = QDataStream(inFile)

    # Check if the format is supported
    format = inStream.readInt()
    if format != __masterFormat:
        return None
    
    # Check if the version is supported
    version = inStream.readInt()
    if version != __masterVersion:
        return None
    
    inStream.setVersion(__qtVersion)

    obj = classType()
    inStream >> obj

    inFile.close()

    return obj