#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from markupwriter.common.util import Serialize

class TestSquare:
    w = 0
    h = 0

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeInt(self.w)
        sOut.writeInt(self.h)
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self.w = sIn.readInt()
        self.h = sIn.readInt()
        return sIn

def testSerialize_write():
    s = TestSquare()
    s.w = 10
    s.h = 10
    assert(Serialize.writeToFile("./resources/.tests/testSerialize.bin", s))

def testSerialize_read():
    s = Serialize.readFromFile(TestSquare, "")
    assert(s == None)

    s = Serialize.readFromFile(TestSquare, "./resources/.tests/testSerialize.bin")
    assert(s != None)
    assert(s.w == 10)
    assert(s.h == 10)
