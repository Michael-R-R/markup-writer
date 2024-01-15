#!/usr/bin/python

from __future__ import annotations


class RefTag(object):
    def __init__(self, docUUID: str, name: str) -> None:
        self._docUUID = docUUID
        self._name = name

    def __eq__(self, other: RefTag | None) -> bool:
        if other is None:
            return False
        return self._docUUID == other._docUUID and self._name == other._name

    def __ne__(self, other: RefTag | None) -> bool:
        return not self.__eq__(other)

    def docUUID(self) -> str:
        return self._docUUID

    def name(self) -> str:
        return self._name
    
    def __str__(self) -> str:
        return self._name
    
    def __repr__(self) -> str:
        return self.__str__()
