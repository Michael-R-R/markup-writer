from PyQt6.QtCore import (
    QDataStream, 
    QFile, 
    QIODevice,
)

from typing import (
    TypeVar,
    Type
)

class Serialize:
    T = TypeVar('T')

    qtVersion = QDataStream.Version.Qt_6_6
    masterFormat = 0x00000001
    masterVersion = 1

    def write(path: str, data) -> bool:
        outFile = QFile(path)
        if not outFile.open(QIODevice.OpenModeFlag.WriteOnly):
            return False
        
        outStream = QDataStream(outFile)
        outStream.writeInt(Serialize.masterFormat)
        outStream.writeInt(Serialize.masterVersion)
        outStream.setVersion(Serialize.qtVersion)
        outStream << data

        outFile.close()

        return True
    
    def read(classType: Type[T], path: str) -> T | None:
        inFile = QFile(path)
        if not inFile.open(QIODevice.OpenModeFlag.ReadOnly):
            return None
        
        inStream = QDataStream(inFile)

        # Check if the format is supported
        format = inStream.readInt()
        if format != Serialize.masterFormat:
            return None
        
        # Check if the version is supported
        version = inStream.readInt()
        if version != Serialize.masterVersion:
            return None
        
        inStream.setVersion(Serialize.qtVersion)

        obj = classType()
        inStream >> obj

        inFile.close()

        return obj