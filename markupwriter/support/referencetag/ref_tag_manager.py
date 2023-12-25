#!/usr/bin/python

from .ref_tag import RefTag

class RefTagManager:
    def __init__(self) -> None:
        self.__refTagDict: dict[str, RefTag] = dict()

    def addRefTag(self, name: str, path: str) -> RefTag | None:
        if name == "":
            return None
        if name in self.__refTagDict:
            return None
        refTag = RefTag(path, name)
        self.__refTagDict[name] = refTag
        return refTag
    
    def removeRefTag(self, name: str) -> bool:
        if not name in self.__refTagDict:
            return False
        self.__refTagDict.pop(name)
        return True
    
    def renameRefTag(self, old: str, new: str) -> RefTag | None:
        if new == "":
            return None
        if not old in self.__refTagDict:
            return None
        if new in self.__refTagDict:
            return None
        refTag = self.__refTagDict.pop(old)
        refTag.rename(new)
        self.__refTagDict[new] = refTag
        return refTag
    
    def getRefTag(self, name: str) -> RefTag | None:
        if not name in self.__refTagDict:
            return None
        return self.__refTagDict[name]
    
    def hasRefTag(self, name: str) -> bool:
        return name in self.__refTagDict
    
    def addDocToTag(self, tagName: str, docPath: str) -> bool:
        if docPath == "":
            return False
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