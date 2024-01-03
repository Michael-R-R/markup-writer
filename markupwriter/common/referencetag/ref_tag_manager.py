#!/usr/bin/python

from .ref_tag import RefTag

class RefTagManager:
    def __init__(self) -> None:
        self._refTagDict: dict[str, RefTag] = dict()

    def addRefTag(self, name: str, docUUID: str) -> RefTag | None:
        if name == "":
            return None
        if name in self._refTagDict:
            return None
        refTag = RefTag(docUUID, name)
        self._refTagDict[name] = refTag
        return refTag
    
    def removeRefTag(self, name: str) -> bool:
        if not name in self._refTagDict:
            return False
        self._refTagDict.pop(name)
        return True
    
    def renameRefTag(self, old: str, new: str) -> RefTag | None:
        if new == "":
            return None
        if not old in self._refTagDict:
            return None
        if new in self._refTagDict:
            return None
        refTag = self._refTagDict.pop(old)
        refTag.rename(new)
        self._refTagDict[new] = refTag
        return refTag
    
    def getRefTag(self, name: str) -> RefTag | None:
        if not name in self._refTagDict:
            return None
        return self._refTagDict[name]
    
    def hasRefTag(self, name: str) -> bool:
        return name in self._refTagDict
    
    def addDocToTag(self, tagName: str, docUUID: str) -> bool:
        if docUUID == "":
            return False
        if not tagName in self._refTagDict:
            return False
        refTag = self._refTagDict[tagName]
        return refTag.addDocRef(docUUID)
    
    def removeDocFromTag(self, tagName: str, docUUID: str) -> bool:
        if not tagName in self._refTagDict:
            return False
        refTag = self._refTagDict[tagName]
        return refTag.removeDocRef(docUUID)
    
    def refTagDict(self) -> dict[str, RefTag]:
        return self._refTagDict