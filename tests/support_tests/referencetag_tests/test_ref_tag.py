from markupwriter.support.referencetag import RefTag

def testRefTag_tagsMatch():
    t1 = RefTag("fake/path/test.doc", "Frank")
    t2 = RefTag("fake/path/test.doc", "Frank")
    assert(t1 == t2)

def testRefTag_tagsDoNotMatch():
    t1 = RefTag("fake/path/test.doc", "Frank")
    t2 = RefTag("fake/path/path/test.doc", "Frank")
    assert(t1 != t2)

def testRefTag_addAlias():
    t1 = RefTag("fake/path/test.doc", "Frank")
    assert(t1.addAlias("Franky"))
    assert(t1.hasAlias("Franky"))
    assert(not t1.hasAlias("Frank"))

def testRefTag_removeAlias():
    t1 = RefTag("fake/path/test.doc", "Frank")
    assert(t1.addAlias("Franky"))
    assert(t1.hasAlias("Franky"))
    assert(t1.removeAlias("Franky"))
    assert(not t1.hasAlias("Franky"))

def testRefTag_getAliasTag():
    t1 = RefTag("fake/path/test.doc", "Frank")
    assert(t1.addAlias("Franky"))

    a1 = t1.getAlias("Franky")
    assert(a1 != None)
    assert(a1.parent() == t1)

def testRefTag_hasAlias(): 
    t1 = RefTag("fake/path/test.doc", "Frank")
    assert(t1.addAlias("Bob"))
    assert(t1.addAlias("Bobby"))
    assert(t1.addAlias("Larry"))

    assert(t1.hasAlias("Bob"))
    assert(not t1.hasAlias("bob"))

    assert(t1.hasAlias("Bobby"))
    assert(not t1.hasAlias("bobby"))

    assert(t1.hasAlias("Larry"))
    assert(not t1.hasAlias("larry"))

def testRefTag_hasDocRef(): 
    t1 = RefTag("fake/path/test.doc", "Frank")
    assert(t1.addDocRef("fake/path/name.doc"))
    assert(t1.addDocRef("another/path/name.doc"))
    assert(t1.addDocRef("test/fake/path/name.doc"))

    assert(t1.hasDocRef("fake/path/name.doc"))
    assert(t1.hasDocRef("another/path/name.doc"))
    assert(t1.hasDocRef("test/fake/path/name.doc"))
    assert(not t1.hasDocRef("test/fake/path/wrong_name.doc"))
