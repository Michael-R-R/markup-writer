#!/usr/bin/python

from __future__ import annotations

from markupwriter.util import getHash

class RefTag(object):
    def __init__(self, path: str, name: str) -> None:
        self._path = path
        self._name = name
        self._hash = getHash(path)
        self._aliasSet: set[AliasTag] = set()
        self._docRefSet: set[str] = set()

    def __eq__(self, other: RefTag) -> bool:
        return self._hash == other._hash
    
    def __ne__(self, other: RefTag) -> bool:
        return self._hash != other._hash

    def __lt__(self, other: RefTag) -> bool:
        return self._hash < other._hash
    
    def __hash__(self) -> int:
        return self._hash
    
    def path(self) -> str:
        return self._path
    
    def name(self) -> str:
        return self._name
    
    def aliasSet(self) -> set[AliasTag]:
        return self._aliasSet
    
    def docRefSet(self) -> set[str]:
        return self._docRefSet
    
    def addAlias(self, name: str) -> bool:
        if AliasTag(None, name) in self._aliasSet:
            return False
        self._aliasSet.add(AliasTag(self, name))
        return True
    
    def removeAlias(self, name: str) -> bool:
        temp = AliasTag(None, name)
        if not temp in self._aliasSet:
            return False
        self._aliasSet.remove(temp)
        return True
    
    def getAlias(self, name: str) -> AliasTag | None:
        temp = AliasTag(None, name)
        if not temp in self._aliasSet:
            return None
        
        # TODO this doesn't work
        # cannot retrieve values from sets
        # need to change the data structure
        return self._aliasSet[temp]
    
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
        return AliasTag(None, name) in self._aliasSet
    
    def hasDocRef(self, name: str) -> bool:
        return name in self._docRefSet
    
class AliasTag(object):
    def __init__(self, parent: RefTag | None, name: str) -> None:
        self._parent = parent
        self._name = name
        self._hash = getHash(name)

    def __eq__(self, other: AliasTag) -> bool:
        return self._hash == other._hash
    
    def __ne__(self, other: RefTag) -> bool:
        return self._hash != other._hash

    def __lt__(self, other: AliasTag) -> bool:
        return self._hash < other._hash
    
    def __hash__(self) -> int:
        return self._hash
    
    def parent(self) -> RefTag:
        return self._parent
    
    def name(self) -> str:
        return self._name