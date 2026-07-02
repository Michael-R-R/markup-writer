#!/usr/bin/python

import re

class Regex(object):
    def getDocumentConfig(text: str) -> str | None:
        match = Regex._findDocumentConfig(text)
        if match is not None:
            return match.group(1)

        return None

    def getCPos(text: str) -> int:
        match = Regex._findCPos(text)
        if match is not None:
            return int(match.group(0)[5:])
        
        return 0

    def getDocumentText(text: str) -> str | None:
        match = Regex._findDocumentConfig(text)
        if match is not None:
            return text[match.end() + 1 :]

        return text
    
    def _findDocumentConfig(text: str) -> re.Match[str] | None:
        found = re.search(r"\[CONFIG\](.*?)\[CONFIG END\]", text, re.DOTALL)
        if found is not None:
            return found
        
        return None
    
    def _findCPos(text: str) -> re.Match[str] | None:
        found = re.search(r"^cpos:.+", text, re.MULTILINE)
        if found is not None:
            return found
        
        return None