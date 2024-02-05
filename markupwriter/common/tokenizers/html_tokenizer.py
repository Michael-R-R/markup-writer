#!/usr/bin/python

import re


class HtmlTokenizer(object):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.body = ""

        self.parenRegex = re.compile(r"(?<=\().+?(?=\))")

        self.replaceFuncs = {
            r"@bold\(.*\)": self._preprocessBold,
            r"@ital\(.*\)": self._preprocessItal,
            r"@boldItal\(.*\)": self._preprocessBoldItal,
            r"@r\(.*\)": self._preprocessRename,
        }

        self.removeFuncs = {
            r"^cpos:.*": self._preprocessRemove,
            r"^@(tag|ref|pov|loc)(\(.*\))": self._preprocessRemove,
            r"%.*": self._preprocessRemove,
            r"<#(\n|.)*?#>": self._preprocessRemove,
        }

        self.processFuncs = {
            r"^# ": self._processHeader1,
            r"^## ": self._processHeader2,
            r"^### ": self._processHeader3,
            r"^#### ": self._processHeader4,
        }

    def run(self) -> str:
        self._preprocess()
        self._process()

        return self.body

    def _preprocess(self):
        for tag in self.replaceFuncs:
            self.replaceFuncs[tag](tag)
            
        for tag in self.removeFuncs:
            self.removeFuncs[tag](tag)

    def _preprocessBold(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
        
            found = found.group(0)
            text = self.parenRegex.search(found)
            if text is None:
                continue
            
            text = text.group(0)
            htmlText = "<b>{}</b>".format(text)
            
            self.text = self.text.replace(found, htmlText)

    def _preprocessItal(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
        
            found = found.group(0)
            text = self.parenRegex.search(found)
            if text is None:
                continue
            
            text = text.group(0)
            htmlText = "<i>{}</i>".format(text)
            
            self.text = self.text.replace(found, htmlText)

    def _preprocessBoldItal(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
        
            found = found.group(0)
            text = self.parenRegex.search(found)
            if text is None:
                continue
            
            text = text.group(0)
            htmlText = "<b><i>{}</i></b>".format(text)
            
            self.text = self.text.replace(found, htmlText)

    def _preprocessRename(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            tag = found.group(0)
            pair = self.parenRegex.search(tag)
            if pair is None:
                continue

            pair = pair.group(0).strip().split(",")
            if len(pair) != 2:
                continue

            self.text = self.text.replace(tag, pair[1])
            self.text = self.text.replace(pair[0], pair[1])

    def _preprocessRemove(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
            self.text = self.text.replace(found.group(0), "")

    def _process(self) -> bool:
        # Process line by line
        for line in self.text.splitlines():
            line = line.strip()
            if line == "":
                continue

            isProcessed = False
            for tag in self.processFuncs:
                if self.processFuncs[tag](tag, line):
                    isProcessed = True
                    break
            
            if not isProcessed:
                self._processParagraph(line)

    def _processHeader1(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        text = text[found.end():]
        self.body += "<h1 class='title'>{}</h1>\n".format(text)
        return True
    
    def _processHeader2(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        text = text[found.end():]
        self.body += "<h2 class='chapter'>{}</h2>\n".format(text)
        return True
    
    def _processHeader3(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        self.body += "<p class='scene'>* * *</p>\n"
        return True
    
    def _processHeader4(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        self.body += "<div class='section'><br><br></div>\n"
        return True
    
    def _processParagraph(self, text: str):
        self.body += "<p class='paragraph'>{}</p>\n".format(text)
