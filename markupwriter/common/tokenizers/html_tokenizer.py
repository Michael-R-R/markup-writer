#!/usr/bin/python

import re


class HtmlTokenizer(object):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.tokens: list[(str, str)] = list()

        self.renameRegex = re.compile(r"@r\(.*\)", re.MULTILINE)

        self.removeRegexes = [
            re.compile(r"^cpos:.*"), # cursor pos
            re.compile(r"^@(tag|ref|pov|loc)(\(.*\))", re.MULTILINE),  # tags
            re.compile(r"%.*", re.MULTILINE),  # single line comment
            re.compile(r"<#(\n|.)*?#>", re.MULTILINE),  # multi line comment
        ]
        
        self.processRegexes = [
            re.compile(r"^# "),  # title
            re.compile(r"^## "),  # chapter
            re.compile(r"^### "),  # scene
            re.compile(r"^#### "),  # section
        ]

    def run(self) -> list[(str, str)]:
        self._preprocess()
        self._process()

        return self.tokens

    def _preprocess(self):
        # Preprocess replacement tokens
        it = self.renameRegex.finditer(self.text)
        for found in it:
            tag = found.group(0)
            pair = re.search(r"(?<=\().+?(?=\))", tag)
            if pair is None:
                continue
            pair = pair.group(0).strip().split(",")
            if len(pair) != 2:
                continue
            
            self.text = self.text.replace(tag, pair[1])
            self.text = self.text.replace(pair[0], pair[1])
        
        # Preprocess remove tokens
        for pattern in self.removeRegexes:
            it = pattern.finditer(self.text)
            for found in it:
                self.text = self.text.replace(found.group(0), "")

    def _process(self) -> bool:
        # Process line by line
        for line in self.text.splitlines():
            line = line.strip()
            if line == "":
                continue
            
            # Process line for any tokens
            isProcessed = False
            for regex in self.processRegexes:
                found = regex.search(line)
                if found is None:
                    continue

                tag = found.group(0).strip()
                text = line[len(tag) :].strip()
                
                self.tokens.append((tag, text))
                isProcessed = True
                break

            # Not processed, so process as paragraph
            if not isProcessed:
                self.tokens.append(("p", line))
