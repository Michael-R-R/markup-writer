#!/usr/bin/python

from .ref_tag import RefTag


class RefTagManager:
    def __init__(self) -> None:
        self.refTagDict: dict[str, RefTag] = dict()

    def addTag(self, name: str, docUUID: str) -> RefTag | None:
        if name == "":
            return None
        if name in self.refTagDict:
            return None
        refTag = RefTag(docUUID, name)
        self.refTagDict[name] = refTag
        return refTag

    def removeTag(self, name: str) -> bool:
        if not name in self.refTagDict:
            return False
        self.refTagDict.pop(name)
        return True

    def getTag(self, name: str) -> RefTag | None:
        if not name in self.refTagDict:
            return None
        return self.refTagDict[name]

    def hasTag(self, name: str) -> bool:
        return name in self.refTagDict
