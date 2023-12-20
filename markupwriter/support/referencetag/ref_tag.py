#!/usr/bin/python

from __future__ import annotations

from markupwriter.util import getHash

class RefTag(object):
    def __init__(self, path: str, name: str) -> None:
        self._path = path
        self._name = name
        self._aliasDict: dict[str, AliasTag] = dict()
        self._docRefSet: set[str] = set()

    def __eq__(self, other: RefTag) -> bool:
        return self._path == other._path
    
    def __ne__(self, other: RefTag) -> bool:
        return self._path != other._path

    def __lt__(self, other: RefTag) -> bool:
        return self._path < other._path
    
    def __hash__(self) -> int:
        return getHash(self._path)
    
    def path(self) -> str:
        return self._path
    
    def name(self) -> str:
        return self._name
    
    def aliasDict(self) -> dict[str, AliasTag]:
        return self._aliasDict
    
    def docRefSet(self) -> set[str]:
        return self._docRefSet
    
    def addAlias(self, name: str) -> bool:
        if name in self._aliasDict:
            return False
        self._aliasDict[name] = AliasTag(self, name)
        return True
    
    def removeAlias(self, name: str) -> bool:
        if not name in self._aliasDict:
            return False
        self._aliasDict.pop(name)
        return True
    
    def getAlias(self, name: str) -> AliasTag | None:
        if not name in self._aliasDict:
            return None
        
        return self._aliasDict[name]
    
    def addDocRef(self, path: str) -> bool:
        if path in self._docRefSet:
            return False
        self._docRefSet.add(path)
        return True
    
    def removeDocRef(self, path: str) -> bool:
        if not path in self._docRefSet:
            return False
        self._docRefSet.remove(path)
        return True
    
    def hasAlias(self, name: str) -> bool:
        return name in self._aliasDict
    
    def hasDocRef(self, name: str) -> bool:
        return name in self._docRefSet
    
class AliasTag(object):
    def __init__(self, parent: RefTag, name: str) -> None:
        self._parent = parent
        self._name = name
    
    def parent(self) -> RefTag:
        return self._parent
    
    def name(self) -> str:
        return self._name