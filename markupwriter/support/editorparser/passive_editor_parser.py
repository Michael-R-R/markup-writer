#!/usr/bin/python

import re

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

from markupwriter.support.syntax import (
    BEHAVIOUR,
    HighlightWordBehaviour,
)

from markupwriter.support.referencetag import (
    AliasTag,
)

class PassiveEditorParser(object):
    def __init__(self) -> None:
        self.__pattern = re.compile(r"^@(create|import)\s")
        self.__prevParsed: list[(str, str)] = list()
        self.__tokenDict = {
            "@create ": CreateToken(),
            "@import ": ImportToken(),
        }

    def tokenize(self, doc: PlainDocument, docPath: str, text: str):
        currParsed: list[(str, str)] = list()
        index = 0
        while index > -1:
            index = text.find("\n")
            line = text[:index+1].strip()
            text = text[index+1:]
            if line == "":
                continue

            found = self.__pattern.search(line)
            if found is None:
                break

            currParsed.append((found.group(0), line))

        if currParsed == self.__prevParsed:
            return

        for prev in self.__prevParsed:
            token: Token = self.__tokenDict.get(prev[0])
            token.remove(doc, prev[1])

        for curr in currParsed:
            token: Token = self.__tokenDict.get(curr[0])
            token.add(doc, docPath, curr[1])

        self.__prevParsed = currParsed

    def reset(self):
        self.__prevParsed.clear()


class Token(object):
    def __init__(self) -> None:
        pass

    def add(self, doc: PlainDocument, docPath: str, line: str):
        raise NotImplementedError()
    
    def remove(self, doc: PlainDocument, line: str):
        raise NotImplementedError()

    
class CreateToken(Token):
    def __init__(self) -> None:
        super().__init__()
        self.__tagPattern = re.compile(r"(?<=@create )[\w']+(?=@as)?")
        self.__aliasPattern = re.compile(r"(?<=@as )[\w',]+")

    def add(self, doc: PlainDocument, docPath: str, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return
        
        rtm = doc.refTagManager()
        refTag = rtm.addRefTag(tag.group(0), docPath)
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

    def add(self, doc: PlainDocument, docPath: str, line: str):
        tag = self.__tagPattern.search(line)
        if tag is None:
            return
        tag = tag.group(0)
        
        rtm = doc.refTagManager()
        refTag = rtm.getRefTag(tag)
        if refTag is None:
            return
        
        h = doc.highlighter()
        refBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.refTag)
        aliasBehaviour: HighlightWordBehaviour = h.getBehaviour(BEHAVIOUR.aliasTag)

        refBehaviour.addWord(refTag.name())
        
        aliases = self.__aliasPattern.search(line)
        if aliases is not None:
            aliases = aliases.group(0).split(",")
            aliasTags: list[AliasTag] = list()
            for alias in aliases:
                aliasTag = refTag.getAlias(alias)
                if aliasTag is None:
                    continue
                aliasTags.append(aliasTag)
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