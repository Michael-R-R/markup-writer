#!/usr/bin/python


class RefTagManager:
    def __init__(self) -> None:
        self._refTagDict: dict[str, str] = dict()  # <tag, uuid>

    def addTag(self, tag: str, uuid: str) -> bool:
        if tag == "":
            return False

        if tag in self._refTagDict:
            return False

        self._refTagDict[tag] = uuid

        return True

    def removeTag(self, tag: str, uuid: str) -> bool:
        if not tag in self._refTagDict:
            return False
        
        if uuid != self._refTagDict[tag]:
            return False

        self._refTagDict.pop(tag)

        return True

    def findUUID(self, tag: str) -> str | None:
        if not tag in self._refTagDict:
            return None

        return self._refTagDict[tag]

    def tagExists(self, tag: str) -> bool:
        return tag in self._refTagDict
