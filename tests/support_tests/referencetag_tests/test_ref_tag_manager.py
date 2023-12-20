#!/usr/bin/python

from markupwriter.support.referencetag import RefTagManager

def testRefTagManager_addRefTag():
    m = RefTagManager()

    assert(m.addRefTag("fake/path/tag.doc", "Frank Burn"))
    assert(not m.addRefTag("fake/path/tag.doc", "Frank Burn"))
    assert(m.hasRefTag("fake/path/tag.doc"))

def testRefTagManager_removeRefTag():
    m = RefTagManager()

    assert(m.addRefTag("fake/path/tag.doc", "Frank Burn"))
    assert(m.removeRefTag("fake/path/tag.doc"))
    assert(not m.hasRefTag("fake/path/tag.doc"))


def testRefTagManager_addDocToTag():
    m = RefTagManager()

    assert(m.addRefTag("fake/path/tag.doc", "Frank Burn"))
    assert(m.addDocToTag("fake/path/tag.doc", "another/fake/path/ref.doc"))
    assert(not m.addDocToTag("fake/path/tag.doc", "another/fake/path/ref.doc"))

    refTag = m.getRefTag("fake/path/tag.doc")
    assert(refTag != None)
    assert(refTag.hasDocRef("another/fake/path/ref.doc"))

def testRefTagManager_removeDocFromTag():
    m = RefTagManager()

    assert(m.addRefTag("fake/path/tag.doc", "Frank Burn"))
    assert(m.addDocToTag("fake/path/tag.doc", "another/fake/path/ref.doc"))
    assert(not m.addDocToTag("fake/path/tag.doc", "another/fake/path/ref.doc"))
    assert(m.removeDocFromTag("fake/path/tag.doc", "another/fake/path/ref.doc"))

    refTag = m.getRefTag("fake/path/tag.doc")
    assert(refTag != None)
    assert(not refTag.hasDocRef("another/fake/path/ref.doc"))
