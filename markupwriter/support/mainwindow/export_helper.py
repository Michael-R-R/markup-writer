#!/usr/bin/python

import os
import textwrap

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

from markupwriter.common.tokenizers import XHtmlTokenizer
from markupwriter.common.parsers import XHtmlParser

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
                        
                        tokenizer = XHtmlTokenizer(text, None)
                        tokenizer.run()
                        
                        parser = XHtmlParser(tokenizer.tokens, None)
                        parser.run()
                        
                        cbody += parser.body
                    
                    # TODO write to directory
                    page = ExportHelper._createHtmlPage(cbody)
                    count += 1
                    
    def _createHtmlPage(body: str) -> str:
        tpath = "resources/templates/xhtml/export.xhtml"
        path = os.path.join(AppConfig.WORKING_DIR, tpath)
        template: str = File.read(path)
        if template is None:
            return ""

        body = textwrap.indent(body, "\t" * 2)
        template = template.replace("<!--body-->", body)
        
        return template