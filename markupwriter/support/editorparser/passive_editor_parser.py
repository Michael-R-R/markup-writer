#!/usr/bin/python

import re

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

from markupwriter.support.referencetag import (
    RefTagManager,
)

class PassiveEditorParser(object):
    def __init__(self) -> None:
        self.__prevParsed: dict[int, (str, str)] = dict()
        self.__tokenDict = {
            "@create ": CreateToken(),
            "@import ": ImportToken(),
        }

    def tokenize(self, doc: PlainDocument, docPath: str, text: str):
        currParsed: dict[int, (str, str)] = dict()
        textList = text.split("\n")
        for i in range(len(textList)):
            line = textList[i]
            found = re.search("^@(create|import) ", line)
            if found is None:
                continue

            currParsed[i] = (found.group(0), line)

        for key, val in currParsed.items():
            prevLine = ""
            currLine = val[1]
            if key in self.__prevParsed:
                temp = self.__prevParsed.pop(key)
                prevLine = temp[1]
            
            token: Token = self.__tokenDict.get(val[0])
            token.tokenize(doc, docPath, prevLine, currLine)

        for key, val in self.__prevParsed.items():
            prevLine = val[1]
            currLine = ""

            token: Token = self.__tokenDict.get(val[0])
            token.tokenize(doc, docPath, prevLine, currLine)

        self.__prevParsed = currParsed

    def clear(self):
        self.__prevParsed.clear()


class Token(object):
    def __init__(self) -> None:
        pass

    def tokenize(self, doc: PlainDocument, docPath: str, prevLine: str, currLine: str):
        raise NotImplementedError

    
class CreateToken(Token):
    def __init__(self) -> None:
        super().__init__()

    def tokenize(self, doc: PlainDocument, docPath: str, prevLine: str, currLine: str):
        if prevLine == currLine:
            return
        
        tagPattern = re.compile(r"(?<=@create )[\w']+(?=@as)?")
        prevTag = re.search(tagPattern, prevLine)
        currTag = re.search(tagPattern, currLine)
        if prevTag is None and currTag is None:
            return

        rtm = doc.refTagManager()

        if prevTag is None:
            currTag = currTag.group(0)
            refTag = rtm.addRefTag(currTag, docPath)
        elif currTag is None:
            prevTag = prevTag.group(0)
            rtm.removeRefTag(prevTag)
            return
        else:
            prevTag = prevTag.group(0)
            currTag = currTag.group(0)
            refTag = rtm.renameRefTag(prevTag, currTag)

        if refTag is not None:
            aliasPattern = re.compile(r"(?<=@as )[\w',]+")
            aliases = re.findall(aliasPattern, currLine)
            print(aliases)
            refTag.clearAliases()
            for alias in aliases:
                refTag.addAlias(alias)

        # TODO aliases are getting checked


class ImportToken(Token):
    def __init__(self) -> None:
        super().__init__()

    def tokenize(self, doc: PlainDocument, docPath: str, prevLine: str, currLine: str):
        pass