#!/usr/bin/python

import re

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

from markupwriter.support.syntax import (
    BEHAVIOUR,
    HighlightWordBehaviour,
)

class PassiveDocumentParser(object):
    def __init__(self, doc: PlainDocument) -> None:
        self._doc = doc
        self._pattern = re.compile(r"^@(create|import)\s")
        self._prevParsed: list[(str, str)] = list()
        self._tokenDict = {
            "@create ": CreateToken(),
            "@import ": ImportToken(),
        }

    def tokenize(self, path: str, text: str):
        currParsed: list[(str, str)] = list()
        index = 0
        while index > -1:
            index = text.find("\n")
            line = text[:index+1].strip()
            text = text[index+1:]
            if line == "":
                continue

            found = self._pattern.search(line)
            if found is None:
                break

            currParsed.append((found.group(0), line))

        if currParsed == self._prevParsed:
            return

        for prev in self._prevParsed:
            token: Token = self._tokenDict.get(prev[0])
            token.remove(self._doc, prev[1])

        for curr in currParsed:
            token: Token = self._tokenDict.get(curr[0])
            token.add(self._doc, path, curr[1])

        self._prevParsed = currParsed

    def reset(self):
        self._prevParsed.clear()


class Token(object):
    def __init__(self) -> None:
        pass

    def add(self, doc: PlainDocument, path: str, line: str):
        raise NotImplementedError()
    
    def remove(self, doc: PlainDocument, line: str):
        raise NotImplementedError()

    
class CreateToken(Token):
    def __init__(self) -> None:
        super().__init__()
        self.__tagPattern = re.compile(r"(?<=@create )[\w']+(?=@as)?")
        self.__aliasPattern = re.compile(r"(?<=@as )[\w',]+")

    def add(self, doc: PlainDocument, path: str, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return
        
        rtm = doc.refTagManager()
        refTag = rtm.addRefTag(tag.group(0), path)
        aliases = self.__aliasPattern.search(line)
        if aliases is None:
            return
        
        aliases = aliases.group(0).split(",")
        refTag.addAliases(aliases)

    def remove(self, doc: PlainDocument, line: str):
        tag = self.__tagPattern.search(line)
        if tag is  None:
            return
        
        rtm = doc.refTagManager()
        rtm.removeRefTag(tag.group(0))


class ImportToken(Token):
    def __init__(self) -> None:
        super().__init__()
        self.__tagPattern = re.compile(r"(?<=@import )[\w']+(?=@as)?")
        self.__aliasPattern = re.compile(r"(?<=@as )[\w',]+")

    def add(self, doc: PlainDocument, path: str, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return
        
        rtm = doc.refTagManager()
        refTag = rtm.getRefTag(tag.group(0))
        if refTag is None:
            return
        
        h = doc.highlighter()
        refBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.refTag)
        aliasBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.aliasTag)

        refBehaviour.addWord(refTag.name())
        
        aliases = self.__aliasPattern.search(line)
        if aliases is not None:
            aliases = aliases.group(0).split(",")
            for alias in aliases:
                if not refTag.hasAlias(alias):
                    continue
                aliasBehaviour.addWord(alias)
        
        h.rehighlight()

    def remove(self, doc: PlainDocument, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return

        h = doc.highlighter()
        refBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.refTag)
        aliasBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.aliasTag)

        refBehaviour.removeWord(tag.group(0))
        
        aliases = self.__aliasPattern.search(line)
        if aliases is not None:
            aliases = aliases.group(0).split(",")
            aliasBehaviour.removeWords(aliases)

        h.rehighlight()