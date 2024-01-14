#!/usr/bin/python

from .ref_tag import RefTag


class RefTagManager:
    def __init__(self) -> None:
        self.refTagDict: dict[str, RefTag] = dict()

    def addRefTag(self, name: str, docUUID: str) -> RefTag | None:
        if name == "":
            return None
        if name in self.refTagDict:
            return None
        refTag = RefTag(docUUID, name)
        self.refTagDict[name] = refTag
        return refTag

    def removeRefTag(self, name: str) -> bool:
        if not name in self.refTagDict:
            return False
        self.refTagDict.pop(name)
        return True

    def getRefTag(self, name: str) -> RefTag | None:
        if not name in self.refTagDict:
            return None
        return self.refTagDict[name]

    def hasRefTag(self, name: str) -> bool:
        return name in self.refTagDict

    def addDocToTag(self, tagName: str, docUUID: str) -> bool:
        if docUUID == "":
            return False
        if not tagName in self.refTagDict:
            return False
        refTag = self.refTagDict[tagName]
        return refTag.addDocRef(docUUID)

    def removeDocFromTag(self, tagName: str, docUUID: str) -> bool:
        if not tagName in self.refTagDict:
            return False
        refTag = self.refTagDict[tagName]
        return refTag.removeDocRef(docUUID)
