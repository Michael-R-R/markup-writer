#!/usr/bin/python

from .ref_tag import RefTag

class RefTagManager:
    def __init__(self) -> None:
        self.__refTagDict: dict[str, RefTag] = dict()

    def addRefTag(self, name: str, path: str) -> bool:
        if name in self.__refTagDict:
            return False
        self.__refTagDict[name] = RefTag(path, name)
        return True
    
    def removeRefTag(self, name: str) -> bool:
        if not name in self.__refTagDict:
            return False
        self.__refTagDict.pop(name)
        return True
    
    def renameRefTag(self, old: str, new: str) -> bool:
        if not old in self.__refTagDict:
            return False
        if new in self.__refTagDict:
            return False
        self.__refTagDict[old].rename(new)
        self.__refTagDict[new] = self.__refTagDict.pop(old)
        return True
    
    def getRefTag(self, name: str) -> RefTag | None:
        if not name in self.__refTagDict:
            return None
        return self.__refTagDict[name]
    
    def hasRefTag(self, name: str) -> bool:
        return name in self.__refTagDict
    
    def addDocToTag(self, tagName: str, docPath: str) -> bool:
        if not tagName in self.__refTagDict:
            return False
        refTag = self.__refTagDict[tagName]
        return refTag.addDocRef(docPath)
    
    def removeDocFromTag(self, tagName: str, docPath: str) -> bool:
        if not tagName in self.__refTagDict:
            return False
        refTag = self.__refTagDict[tagName]
        return refTag.removeDocRef(docPath)
    
    def refTagDict(self) -> dict[str, RefTag]:
        return self.__refTagDict