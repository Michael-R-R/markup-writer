#!/usr/bin/python

import re


class HtmlTokenizer(object):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.body = ""

        self.parenRegex = re.compile(r"(?<=\().*?(?=\))")
        self.nlParenRegex = re.compile(r"(?<=\()(\n|.)*?(?=\))")
        self.tokenRegex = re.compile(r"^@.*(?=\()")

        self.replaceDict = {
            r"@bold\((\n|.)*?\)": self._preprocessBold,
            r"@ital\((\n|.)*?\)": self._preprocessItal,
            r"@boldItal\((\n|.)*?\)": self._preprocessBoldItal,
        }

        self.removeDict = {
            r"^cpos:.*": self._preprocessRemove,
            r"^@(tag|ref|pov|loc)(\(.*\))": self._preprocessRemove,
            r"%.*": self._preprocessRemove,
            r"<#(\n|.)*?#>": self._preprocessRemove,
        }

        self.tokenDict = {
            r"@title": self._processTitle,
            r"@chapter": self._processChapter,
            r"@scene": self._processScene,
            r"@section": self._processSection,
            r"@alignL": self._processAlignL,
            r"@alignC": self._processAlignC,
            r"@alignR": self._processAlignR,
            r"@vspace": self._preprocessVSpace,
        }

    def run(self) -> str:
        self._preprocess()
        self._process()

        return self.body

    def _preprocess(self):
        for tag in self.replaceDict:
            self.replaceDict[tag](tag)
            
        for tag in self.removeDict:
            self.removeDict[tag](tag)

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

    def _preprocessRemove(self, tag: str):
        it = re.finditer(tag, self.text, re.MULTILINE)
        for found in it:
            if found is None:
                continue
            self.text = self.text.replace(found.group(0), "")

    def _process(self):
        # Process line by line
        for line in self.text.splitlines():
            if line == "":
                continue

            token = self.tokenRegex.search(line)
            if token is not None:
                token = token.group(0)
                self.tokenDict[token](line)
            else:
                self._processParagraph(line)

    def _processTitle(self, text: str) -> bool:
        found = self.parenRegex.search(text)
        if found is None:
            return False
        htmlText = found.group(0)
        self.body += "<h1 class='title'>{}</h1>\n".format(htmlText)
        return True
    
    def _processChapter(self, text: str) -> bool:
        found = self.parenRegex.search(text)
        if found is None:
            return False
        htmlText = found.group(0)
        self.body += "<h2 class='chapter'>{}</h2>\n".format(htmlText)
        return True
    
    def _processScene(self, text: str) -> bool:
        found = self.parenRegex.search(text)
        if found is None:
            return False
        self.body += "<p class='scene'><br>* * *<br></p>\n"
        return True
    
    def _processSection(self, text: str) -> bool:
        found = self.parenRegex.search(text)
        if found is None:
            return False
        self.body += "<div class='section'><br><br></div>\n"
        return True
    
    def _processAlignL(self, text: str) -> bool:
        return self._processAlign(text, "<p class='alignL'>?</p>\n")
    
    def _processAlignC(self, text: str) -> bool:
        return self._processAlign(text, "<p class='alignC'>?</p>\n")
    
    def _processAlignR(self, text: str) -> bool:
        return self._processAlign(text, "<p class='alignR'>?</p>\n")
    
    def _processAlign(self, text: str, html: str) -> bool:
        found = self.parenRegex.search(text)
        if found is None:
            return False
        found = found.group(0)

        html = html.replace("?", found)
        
        self.body += html
        
        return True
    
    def _preprocessVSpace(self, text: str) -> bool:
        found = self.parenRegex.search(text)
        if found is None:
            return False
        found = found.group(0)
        if not found.isnumeric():
            return False
        
        htmlText = "<br>" * int(found)
        
        self.body += "<p class='vspace'>{}</p>".format(htmlText)
        
        return True
    
    def _processParagraph(self, text: str):
        if text.startswith("\t"):
            self.body += "<p class='indent'>{}</p>\n".format(text.strip())
        else:
            self.body += "<p class='noindent'>{}</p>\n".format(text)
