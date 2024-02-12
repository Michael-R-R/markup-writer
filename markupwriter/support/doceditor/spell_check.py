#!/usr/bin/python

import enchant

from PyQt6.QtCore import (
    QDataStream,
)


class SpellCheck(object):
    def __init__(self) -> None:
        self.endict = enchant.Dict("en_US")
        self._sessionSet = set()
        
    def addWord(self, word: str):
        if word in self._sessionSet:
            return
        self._sessionSet.add(word)
        self.endict.add_to_session(word)
        
    def removeWord(self, word: str):
        if not word in self._sessionSet:
            return
        self._sessionSet.remove(word)
        self.endict.remove_from_session(word)
    
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout.writeInt(len(self._sessionSet))
        for w in self._sessionSet:
            sout.writeQString(w)
            
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        count = sin.readInt()
        for i in range(count):
            self.addWord(sin.readQString())
            
        return sin
    