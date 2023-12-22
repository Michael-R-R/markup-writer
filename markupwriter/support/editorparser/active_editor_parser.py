#!/usr/bin/python

import re

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

from markupwriter.support.syntax import (
    Highlighter,
    HighlightWordBehaviour,
)

from markupwriter.support.referencetag import (
    RefTagManager,
)

class ActiveEditorParser(object):
    def __init__(self) -> None:
        self.__tokenList: list[Token] = [CreateToken()]

    def tokenize(self, doc: PlainDocument, docPath: str, line: str):
        if not line.startswith("@"):
            return

        for t in self.__tokenList:
            if t.tokenize(doc, docPath, line):
                return


class Token(object):
    def __init__(self) -> None:
        pass

    def tokenize(self, doc: PlainDocument, docPath: str, line: str) -> bool:
        raise NotImplementedError

    
class CreateToken(Token):
    def __init__(self) -> None:
        super().__init__()

    def tokenize(self, doc: PlainDocument, docPath: str, line: str) -> bool:
        if not line.startswith("@create "):
            return False
        
        tag = re.search("(?<=@create )[a-zA-Z'\s]+(?=@as)", line)
        if tag is None:
            tag = re.search("(?<=@create )[a-zA-Z'\s]+", line)

        if tag is not None:
            print("tag:", tag.group(0))

        aliases = re.search("(?<=@as )[a-zA-Z',\s]+", line)
        if aliases is not None:
            print("aliases:", aliases.group(0))

        return True
