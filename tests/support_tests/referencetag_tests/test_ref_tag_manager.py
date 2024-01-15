#!/usr/bin/python

from markupwriter.common.referencetag import RefTagManager

def testRefTagManager_addRefTag():
    m = RefTagManager()

    assert(m.addTag("Frank Burn", "fake/path/tag.doc"))
    assert(not m.addTag("Frank Burn", "fake/path/tag.doc"))
    assert(m.hasTag("Frank Burn"))

def testRefTagManager_removeRefTag():
    m = RefTagManager()

    assert(m.addTag("Frank Burn", "fake/path/tag.doc"))
    assert(m.removeTag("Frank Burn"))
    assert(not m.hasTag("Frank Burn"))


def testRefTagManager_addDocToTag():
    m = RefTagManager()

    assert(m.addTag("Frank Burn", "fake/path/tag.doc"))
    assert(m.addDocToTag("Frank Burn", "another/fake/path/ref.doc"))
    assert(not m.addDocToTag("Frank Burn", "another/fake/path/ref.doc"))

    refTag = m.getTag("Frank Burn")
    assert(refTag != None)
    assert(refTag.hasDocRef("another/fake/path/ref.doc"))

def testRefTagManager_removeDocFromTag():
    m = RefTagManager()

    assert(m.addTag("Frank Burn", "fake/path/tag.doc"))
    assert(m.addDocToTag("Frank Burn", "another/fake/path/ref.doc"))
    assert(not m.addDocToTag("Frank Burn", "another/fake/path/ref.doc"))
    assert(m.removeDocFromTag("Frank Burn", "another/fake/path/ref.doc"))

    refTag = m.getTag("Frank Burn")
    assert(refTag != None)
    assert(not refTag.hasDocRef("another/fake/path/ref.doc"))
