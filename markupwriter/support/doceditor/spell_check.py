#!/usr/bin/python

import enchant

from PyQt6.QtCore import (
    QDataStream,
)


class SpellCheck(object):
    def __init__(self) -> None:
        self.endict = enchant.Dict("en_US")
        
    def addWord(self, word: str):
        self.endict.add(word)
    
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
    