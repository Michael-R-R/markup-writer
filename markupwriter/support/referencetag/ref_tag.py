#!/usr/bin/python

from __future__ import annotations

from markupwriter.util import getHash

class RefTag(object):
    def __init__(self, path: str, name: str) -> None:
        self.__path = path
        self.__name = name
        self.__aliasDict: dict[str, AliasTag] = dict()
        self.__docRefSet: set[str] = set()

    def __eq__(self, other: RefTag | None) -> bool:
        if other is None:
            return False
        return self.__path == other.__path
    
    def __ne__(self, other: RefTag | None) -> bool:
        if other is None:
            return True
        return self.__path != other.__path

    def __lt__(self, other: RefTag | None) -> bool:
        if other is None:
            return False
        return self.__path < other.__path
    
    def __hash__(self) -> int:
        return getHash(self.__path)
    
    def path(self) -> str:
        return self.__path
    
    def name(self) -> str:
        return self.__name
    
    def aliasDict(self) -> dict[str, AliasTag]:
        return self.__aliasDict
    
    def docRefSet(self) -> set[str]:
        return self.__docRefSet
    
    def addAlias(self, name: str) -> bool:
        if name in self.__aliasDict:
            return False
        self.__aliasDict[name] = AliasTag(self, name)
        return True
    
    def removeAlias(self, name: str) -> bool:
        if not name in self.__aliasDict:
            return False
        self.__aliasDict.pop(name)
        return True
    
    def getAlias(self, name: str) -> AliasTag | None:
        if not name in self.__aliasDict:
            return None
        
        return self.__aliasDict[name]
    
    def addDocRef(self, path: str) -> bool:
        if path in self.__docRefSet:
            return False
        self.__docRefSet.add(path)
        return True
    
    def removeDocRef(self, path: str) -> bool:
        if not path in self.__docRefSet:
            return False
        self.__docRefSet.remove(path)
        return True
    
    def hasAlias(self, name: str) -> bool:
        return name in self.__aliasDict
    
    def hasDocRef(self, name: str) -> bool:
        return name in self.__docRefSet
    
class AliasTag(object):
    def __init__(self, parent: RefTag, name: str) -> None:
        self._parent = parent
        self._name = name
    
    def parent(self) -> RefTag:
        return self._parent
    
    def name(self) -> str:
        return self._name