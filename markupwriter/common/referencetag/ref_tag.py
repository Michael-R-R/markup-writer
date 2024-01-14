#!/usr/bin/python

from __future__ import annotations


class RefTag(object):
    def __init__(self, docUUID: str, name: str) -> None:
        self._docHash = docUUID
        self._name = name
        self._docRefSet: set[str] = set()

    def __eq__(self, other: RefTag | None) -> bool:
        if other is None:
            return False
        return self._docHash == other._docHash and self._name == other._name

    def __ne__(self, other: RefTag | None) -> bool:
        return not self.__eq__(other)

    def docUUID(self) -> str:
        return self._docHash

    def name(self) -> str:
        return self._name

    def docRefSet(self) -> set[str]:
        return self._docRefSet

    def addDocRef(self, path: str) -> bool:
        if path == "":
            return False
        if path in self._docRefSet:
            return False
        self._docRefSet.add(path)
        return True

    def removeDocRef(self, path: str) -> bool:
        if not path in self._docRefSet:
            return False
        self._docRefSet.remove(path)
        return True

    def clearDocRefs(self):
        self._docRefSet.clear()

    def hasDocRef(self, name: str) -> bool:
        return name in self._docRefSet
