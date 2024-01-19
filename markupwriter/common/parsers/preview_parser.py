#!/usr/bin/python


class PreviewParser(object):
    def __init__(self, tokens: list[(str, str)]) -> None:
        self.tokens = tokens
        self.html = ""
        
    def run(self):
        for t in self.tokens:
            match t[0]:
                case "p": self._processParagraph(t[1])
                case "# ": self._processHeaderOne(t[1])
                case "## ": self._processHeaderTwo(t[1])
                case "### ": self._processHeaderThree(t[1])
                case "#### ": self._processHeaderFour(t[1])
        
    def _processParagraph(self, line: str):
        self.html += "<p>{}</p>".format(line)
        
    def _processHeaderOne(self, line: str):
        self.html += "<h1>{}</h1>".format(line)
    
    def _processHeaderTwo(self, line: str):
        self.html += "<h2>{}</h2>".format(line)
        
    def _processHeaderThree(self, line: str):
        self.html += "<h3>{}</h3>".format(line)
        
    def _processHeaderFour(self, line: str):
        self.html += "<h4>{}</h4>".format(line)
