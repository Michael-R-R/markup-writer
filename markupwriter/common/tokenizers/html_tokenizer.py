#!/usr/bin/python

import re


class HtmlTokenizer(object):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.body = ""

        self.parenRegex = re.compile(r"(?<=\().*?(?=\))")
        self.nlParenRegex = re.compile(r"(?<=\()(\n|.)*?(?=\))")

        self.replaceFuncs = {
            r"@bold\((\n|.)*?\)": self._preprocessBold,
            r"@ital\((\n|.)*?\)": self._preprocessItal,
            r"@boldItal\((\n|.)*?\)": self._preprocessBoldItal,
            r"@rename\(.*\)": self._preprocessRename,
            r"@vspace\(.*\)": self._preprocessVSpace
        }

        self.removeFuncs = {
            r"^cpos:.*": self._preprocessRemove,
            r"^@(tag|ref|pov|loc)(\(.*\))": self._preprocessRemove,
            r"%.*": self._preprocessRemove,
            r"<#(\n|.)*?#>": self._preprocessRemove,
        }

        self.processFuncs = {
            r"^@title\(.*\)": self._processTitle,
            r"^@chapter\(.*\)": self._processChapter,
            r"^@scene\(.*\)": self._processScene,
            r"^@section\(.*\)": self._processSection,
            r"@alignL\(.*\)": self._processAlignL,
            r"@alignC\(.*\)": self._processAlignC,
            r"@alignR\(.*\)": self._processAlignR,
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
        self._preprocessFormat(tag, "<b>?</b>")

    def _preprocessItal(self, tag: str):
        self._preprocessFormat(tag, "<i>?</i>")

    def _preprocessBoldItal(self, tag: str):
        self._preprocessFormat(tag, "<b><i>?</i></b>")

    def _preprocessFormat(self, tag: str, htmlTag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            found = found.group(0)
            text = self.nlParenRegex.search(found)
            if text is None:
                continue
            
            htmlText = ""
            lines = text.group(0).splitlines()
            size = len(lines)
            if size > 0:
                for i in range(size-1):
                    if lines[i] == "":
                        continue
                    htmlText += htmlTag.replace("?", lines[i]) + "\n"
                    
                htmlText += htmlTag.replace("?", lines[size-1])
                
            self.text = self.text.replace(found, htmlText)

    def _preprocessRename(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            tag = found.group(0)
            pair = self.nlParenRegex.search(tag)
            if pair is None:
                continue

            pair = pair.group(0).strip().split(",")
            if len(pair) != 2:
                continue

            self.text = self.text.replace(tag, pair[1])
            self.text = self.text.replace(pair[0], pair[1])

    def _preprocessVSpace(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            found = found.group(0)
            text = self.nlParenRegex.search(found)
            text = None if text is None else text.group(0)
            if text is None:
                continue
            if not text.isnumeric():
                continue
            htmlText = "<br>" * int(text)
            self.text = self.text.replace(found, htmlText)

    def _preprocessRemove(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
            self.text = self.text.replace(found.group(0), "")

    def _process(self) -> bool:
        # Process line by line
        for line in self.text.splitlines():
            if line == "":
                continue

            isProcessed = False
            for tag in self.processFuncs:
                if self.processFuncs[tag](tag, line):
                    isProcessed = True
                    break
            
            if not isProcessed:
                self._processParagraph(line)

    def _processTitle(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        htmlText = self.parenRegex.search(found.group(0))
        self.body += "<h1 class='title'>{}</h1>\n".format(htmlText.group(0))
        return True
    
    def _processChapter(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        htmlText = self.parenRegex.search(found.group(0))
        self.body += "<h2 class='chapter'>{}</h2>\n".format(htmlText.group(0))
        return True
    
    def _processScene(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        self.body += "<p class='scene'><br>* * *<br></p>\n"
        return True
    
    def _processSection(self, tag: str, text: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        self.body += "<div class='section'><br><br></div>\n"
        return True
    
    def _processAlignL(self, tag: str, text: str) -> bool:
        return self._processAlign(tag, text, "<p class='alignL'>?</p>\n")
    
    def _processAlignC(self, tag: str, text: str) -> bool:
        return self._processAlign(tag, text, "<p class='alignC'>?</p>\n")
    
    def _processAlignR(self, tag: str, text: str) -> bool:
        return self._processAlign(tag, text, "<p class='alignR'>?</p>\n")
    
    def _processAlign(self, tag: str, text: str, html: str) -> bool:
        found = re.search(tag, text)
        if found is None:
            return False
        found = found.group(0)
        
        alignText = self.parenRegex.search(text)
        if alignText is None:
            return False
        alignText = alignText.group(0)

        html = html.replace("?", alignText)
        
        self.body += html
        
        return True
    
    def _processParagraph(self, text: str):
        if text.startswith("\t"):
            self.body += "<p class='indent'>{}</p>\n".format(text.strip())
        else:
            self.body += "<p class='noindent'>{}</p>\n".format(text)
