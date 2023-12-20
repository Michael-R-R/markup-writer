#!/usr/bin/python

from .ref_tag import RefTag

class RefTagManager:
    def __init__(self) -> None:
        self.__refTagDict: dict[str, RefTag] = dict()

    def addRefTag(self, path: str, name: str) -> bool:
        if path in self.__refTagDict:
            return False
        self.__refTagDict[path] = RefTag(path, name)
        return True
    
    def removeRefTag(self, path: str) -> bool:
        if not path in self.__refTagDict:
            return False
        self.__refTagDict.pop(path)
        return True
    
    def getRefTag(self, path: str) -> RefTag | None:
        if not path in self.__refTagDict:
            return None
        return self.__refTagDict[path]
    
    def hasRefTag(self, path: str) -> bool:
        return path in self.__refTagDict
    
    def addDocToTag(self, tagPath: str, docPath: str) -> bool:
        if not tagPath in self.__refTagDict:
            return False
        refTag = self.__refTagDict[tagPath]
        return refTag.addDocRef(docPath)
    
    def removeDocFromTag(self, tagPath: str, docPath: str) -> bool:
        if not tagPath in self.__refTagDict:
            return False
        refTag = self.__refTagDict[tagPath]
        return refTag.removeDocRef(docPath)
    
    def refTagDict(self) -> dict[str, RefTag]:
        return self.__refTagDict