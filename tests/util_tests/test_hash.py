#!/usr/bin/python

from markupwriter.util import getHash

def testHash_emptyIsZero():
    hash1 = getHash("")
    assert(hash1 == 0)

def testHash_hashDontMatch():
    hash1 = getHash("hello")
    hash2 = getHash("goodbye")
    assert(hash1 != hash2)

def testHash_hashDoMatch():

    hash1 = getHash("hello")
    hash2 = getHash("hello")
    assert(hash1 == hash2)

    hash1 = getHash("asdfasdf adf adf adasdfadf ad adfadfa 786876 a8d7f6a 68a7d6 fa8 adf 786a87df")
    hash2 = getHash("asdfasdf adf adf adasdfadf ad adfadfa 786876 a8d7f6a 68a7d6 fa8 adf 786a87df")
    assert(hash1 == hash2)