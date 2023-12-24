#!/usr/bin/python

import re

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

from markupwriter.support.referencetag import (
    RefTagManager,
)

class ActiveEditorParser(object):
    def __init__(self) -> None:
        self.__tokenDict = {
            "@create": CreateToken(),
            "@import": ImportToken(),
        }

    def tokenize(self, doc: PlainDocument, docPath: str, line: str):
        found = re.search("^@(create|import)", line)
        if found is None:
            return

        token = self.__tokenDict.get(found.group(0))
        token.tokenize(doc, docPath, line)


class Token(object):
    def __init__(self) -> None:
        pass

    def tokenize(self, doc: PlainDocument, docPath: str, line: str) -> bool:
        raise NotImplementedError

    
class CreateToken(Token):
    def __init__(self) -> None:
        super().__init__()

    def tokenize(self, doc: PlainDocument, docPath: str, line: str) -> bool:
        tag = re.search("(?<=@create )[a-zA-Z'\s]+(?=@as)?", line)
        if tag is None:
            return False
        
        tag = tag.group(0).strip(" \n\r")

        aliases = re.search("(?<=@as )[a-zA-Z',\s]+", line)
        if aliases is not None:
            aliases = aliases.group(0).strip(" \n\r")

        print("tag:", tag)
        print("aliases:", aliases)

        return True


class ImportToken(Token):
    def __init__(self) -> None:
        super().__init__()

    def tokenize(self, doc: PlainDocument, docPath: str, line: str) -> bool:
        return False