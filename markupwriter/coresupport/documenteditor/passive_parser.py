#!/usr/bin/python

import re

from markupwriter.common.syntax import (
    BEHAVIOUR,
    Highlighter,
    HighlightWordBehaviour,
)

from markupwriter.common.referencetag import (
    RefTagManager,
)

class PassiveParser(object):
    def __init__(self, highlighter: Highlighter, manager: RefTagManager) -> None:
        self._highlighter = highlighter
        self._refTagManager = manager
        self._pattern = re.compile(r"^@(create|import)\s")
        self._prevParsed: list[(str, str)] = list()
        self._tokenDict = {
            "@create ": CreateToken(),
            "@import ": ImportToken(),
        }

    def tokenize(self, docHash: str, text: str):
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
            token.remove(self, prev[1])

        for curr in currParsed:
            token: Token = self._tokenDict.get(curr[0])
            token.add(self, docHash, curr[1])

        self._prevParsed = currParsed

    def reset(self):
        self._prevParsed.clear()


class Token(object):
    def __init__(self) -> None:
        pass

    def add(self, parser: PassiveParser, docHash: str, line: str):
        raise NotImplementedError()
    
    def remove(self, parser: PassiveParser, line: str):
        raise NotImplementedError()

    
class CreateToken(Token):
    def __init__(self) -> None:
        super().__init__()
        self.__tagPattern = re.compile(r"(?<=@create )[\w']+(?=@as)?")
        self.__aliasPattern = re.compile(r"(?<=@as )[\w',]+")

    def add(self, parser: PassiveParser, docHash: str, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return
        
        rtm = parser._refTagManager
        refTag = rtm.addRefTag(tag.group(0), docHash)
        aliases = self.__aliasPattern.search(line)
        if aliases is None:
            return
        
        aliases = aliases.group(0).split(",")
        refTag.addAliases(aliases)

    def remove(self, parser: PassiveParser, line: str):
        tag = self.__tagPattern.search(line)
        if tag is  None:
            return
        
        rtm = parser._refTagManager
        rtm.removeRefTag(tag.group(0))


class ImportToken(Token):
    def __init__(self) -> None:
        super().__init__()
        self.__tagPattern = re.compile(r"(?<=@import )[\w']+(?=@as)?")
        self.__aliasPattern = re.compile(r"(?<=@as )[\w',]+")

    def add(self, parser: PassiveParser, docHash: str, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return
        
        rtm = parser._refTagManager
        refTag = rtm.getRefTag(tag.group(0))
        if refTag is None:
            return
        
        h = parser._highlighter
        refBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.refTag)
        aliasBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.aliasTag)

        refBehaviour.add(refTag.name())
        
        aliases = self.__aliasPattern.search(line)
        if aliases is not None:
            aliases = aliases.group(0).split(",")
            for alias in aliases:
                if not refTag.hasAlias(alias):
                    continue
                aliasBehaviour.add(alias)
        
        h.rehighlight()

    def remove(self, parser: PassiveParser, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return

        h = parser._highlighter
        refBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.refTag)
        aliasBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.aliasTag)

        refBehaviour.remove(tag.group(0))
        
        aliases = self.__aliasPattern.search(line)
        if aliases is not None:
            aliases = aliases.group(0).split(",")
            aliasBehaviour.removeList(aliases)

        h.rehighlight()