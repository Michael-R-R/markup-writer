#!/usr/bin/python

from re import Match
from typing import Iterator


class PreviewParser(object):
    def __init__(self, text: str, tokens: [str, Iterator[Match[str]]]) -> None:
        self.text = text
        self.tokens = tokens
        
    def run(self) -> str:
        for t in self.tokens:
            pass
        
    def _parseMultiComment(self):
        pass
