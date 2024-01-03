#!/usr/bin/python

from markupwriter.util import Hash

def testHash_emptyIsZero():
    hash1 = Hash.compute("")
    assert(hash1 == 0)

def testHash_hashDontMatch():
    hash1 = Hash.compute("hello")
    hash2 = Hash.compute("goodbye")
    assert(hash1 != hash2)

def testHash_hashDoMatch():

    hash1 = Hash.compute("hello")
    hash2 = Hash.compute("hello")
    assert(hash1 == hash2)

    hash1 = Hash.compute("asdfasdf adf adf adasdfadf ad adfadfa 786876 a8d7f6a 68a7d6 fa8 adf 786a87df")
    hash2 = Hash.compute("asdfasdf adf adf adasdfadf ad adfadfa 786876 a8d7f6a 68a7d6 fa8 adf 786a87df")
    assert(hash1 == hash2)