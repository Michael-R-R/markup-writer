#!/usr/bin/python

import os

from markupwriter.config import AppConfig
from markupwriter.common.util import File


class HtmlParser(object):
    def __init__(self) -> None:
        pass

    def run(self, body: str) -> str:
        tpath = os.path.join(AppConfig.WORKING_DIR, "resources/html/preview.html")
        template: str = File.read(tpath)
        if template is None:
            return ""
        
        cpath = os.path.join(AppConfig.WORKING_DIR, "resources/css/preview.css")
        css: str = File.read(cpath)
        if css is None:
            return ""
        
        template = template.replace("/*style*/", css)
        template = template.replace("<!--body-->", body)
        
        return template
