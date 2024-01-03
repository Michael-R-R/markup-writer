#!/usr/bin/python

from __future__ import annotations

class RefTag(object):
    def __init__(self, docUUID: str, name: str) -> None:
        self._docHash = docUUID
        self._name = name
        self._aliasDict: dict[str, AliasTag] = dict()
        self._docRefSet: set[str] = set()

    def __eq__(self, other: RefTag | None) -> bool:
        if other is None:
            return False
        return (self._docHash == other._docHash and
                self._name == other._name)
    
    def __ne__(self, other: RefTag | None) -> bool:
        return not self.__eq__(other)
    
    def docUUID(self) -> str:
        return self._docHash
    
    def name(self) -> str:
        return self._name
    
    def aliasDict(self) -> dict[str, AliasTag]:
        return self._aliasDict
    
    def docRefSet(self) -> set[str]:
        return self._docRefSet
    
    def rename(self, name: str):
        self._name = name
    
    def addAlias(self, name: str) -> bool:
        if name == "":
            return False
        if name in self._aliasDict:
            return False
        self._aliasDict[name] = AliasTag(self, name)
        return True
    
    def addAliases(self, nameList: list[str]):
        for name in nameList:
            self.addAlias(name)
    
    def removeAlias(self, name: str) -> bool:
        if not name in self._aliasDict:
            return False
        self._aliasDict.pop(name)
        return True
    
    def renameAlias(self, old: str, new: str) -> bool:
        if new == "":
            return False
        if not old in self._aliasDict:
            return False
        if new in self._aliasDict:
            return False
        self._aliasDict[old].rename(new)
        self._aliasDict[new] = self._aliasDict.pop(old)
        return True
    
    def clearAliases(self):
        self._aliasDict.clear()
    
    def getAlias(self, name: str) -> AliasTag | None:
        if not name in self._aliasDict:
            return None
        
        return self._aliasDict[name]
    
    def hasAlias(self, name: str) -> bool:
        return name in self._aliasDict
    
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
    

class AliasTag(object):
    def __init__(self, parent: RefTag, name: str) -> None:
        self._parent = parent
        self._name = name
    
    def parent(self) -> RefTag:
        return self._parent
    
    def name(self) -> str:
        return self._name
    
    def rename(self, name: str):
        self._name = name