#!/usr/bin/python

import re

class Regex(object):
    def findDocumentConfig(text: str) -> re.Match[str] | None:
        found = re.search(r"\[CONFIG\](.*?)\[CONFIG END\]", text, re.DOTALL)
        if found is not None:
            return found
        
        return None
    
    def findCPos(text: str) -> re.Match[str] | None:
        found = re.search(r"^cpos:.+", text, re.MULTILINE)
        if found is not None:
            return found
        
        return None
