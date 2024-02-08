#!/usr/bin/python

import os

from PyQt6.QtWidgets import (
    QWidget,
)

from markupwriter.widgets import (
    ExportSelectWidget,
)

from markupwriter.config import (
    AppConfig
)

from markupwriter.common.util import (
    File,
)

from markupwriter.common.tokenizers import HtmlTokenizer
from markupwriter.common.parsers import HtmlParser

import markupwriter.mvc.controller.corewidgets as wcore


class ExportHelper(object):
    def exportEPUB3(dtc: wcore.DocumentTreeController, parent: QWidget | None):
        widget = ExportSelectWidget(dtc.view.treewidget, parent)
        if widget.exec() == 1:
            item = widget.value
            
            if item is not None:
                contentPath = AppConfig.projectContentPath()
                
                count = 0
                buildList = dtc.buildExportTree(item)
                for chapter in buildList:
                    cbody = ""
                    for file in chapter:
                        path = os.path.join(contentPath, file.UUID())
                        text = File.read(path)
                        if text is None:
                            continue
                        
                        tokenizer = HtmlTokenizer(text, None)
                        tokenizer.run()
                        
                        parser = HtmlParser(tokenizer.tokens, None)
                        parser.run()
                        
                        cbody += parser.body
                    
                    # TODO testing directory
                    npath = os.path.join("./resources/.tests/novel", "{}.html".format(count))
                    page = ExportHelper._createHtmlPage(cbody)
                    File.write(npath, page)
                    count += 1
                    
    def _createHtmlPage(body: str) -> str:
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