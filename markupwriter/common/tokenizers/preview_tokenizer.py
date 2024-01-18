#!/usr/bin/python

import re
from typing import Iterator


class PreviewTokenizer(object):
    def __init__(self, text: str) -> None:
        self.text = text
        self.patternList = {
            "comment": re.compile(r"#(.*)"),
            "multicomment": re.compile(r"<%(\n|.)*?%>")
        }

    def run(self) -> dict[str, Iterator[re.Match[str]]]:
        results: dict[str, Iterator[re.Match[str]]] = dict()
        
        for key in self.patternList:
            results[key] = self.patternList[key].finditer(self.text)
            
        # Test
        for mc in results["multicomment"]:
            print(mc.start(), mc.end(), mc.group(0))
        
        return results