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
        self.__pattern = re.compile(r"^@(create|import)\s")
        self.__prevParsed: list[(str, str)] = list()
        self.__tokenDict = {
            "@create ": CreateToken(),
            "@import ": ImportToken(),
        }

    def tokenize(self, doc: PlainDocument, docPath: str, text: str):
        currParsed: list[(str, str)] = list()
        lineIndex = 0
        while lineIndex > -1:
            lineIndex = text.find("\n")
            line = text[:lineIndex+1].strip()
            text = text[lineIndex+1:]
            if line == "":
                continue

            found = self.__pattern.search(line)
            if found is None:
                break

            currParsed.append((found.group(0), line))

        if currParsed == self.__prevParsed:
            return

        for prev in self.__prevParsed:
            prevLine = prev[1]
            token: Token = self.__tokenDict.get(prev[0])
            token.tokenize(doc, docPath, prevLine, "")

        for curr in currParsed:
            currLine = curr[1]
            token: Token = self.__tokenDict.get(curr[0])
            token.tokenize(doc, docPath, "", currLine)

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

        rtm = doc.refTagManager()

        # remove operation
        if prevTag is not None:
            rtm.removeRefTag(prevTag.group(0))

        # add operation
        if currTag is not None:
            refTag = rtm.addRefTag(currTag.group(0), docPath)
            aliasPattern = re.compile(r"(?<=@as )[\w',]+")
            aliases = re.findall(aliasPattern, currLine)
            refTag.addAliases(aliases)
            print(refTag.aliasDict())


class ImportToken(Token):
    def __init__(self) -> None:
        super().__init__()

    def tokenize(self, doc: PlainDocument, docPath: str, prevLine: str, currLine: str):
        pass