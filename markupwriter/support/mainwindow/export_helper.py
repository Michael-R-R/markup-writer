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
    wd = ""
    exportDir = ""
    metaPath = ""
    oebpsPath = ""
    cssPath = ""
    imgPath = ""
    
    def exportEPUB3(dtc: wcore.DocumentTreeController, parent: QWidget | None):
        widget = ExportSelectWidget(dtc.view.treewidget, parent)
        if widget.exec() == 1:
            treeItem = widget.value
            if treeItem is None:
                return
            
            ExportHelper._createReqPaths(widget.dir)
            ExportHelper._createReqDirectories()
            ExportHelper._createReqFiles()
            
            if treeItem is not None:
                contentPath = AppConfig.projectContentPath()
                
                count = 0
                buildList = dtc.buildExportTree(treeItem)
                for chapter in buildList:
                    cbody = ""
                    for file in chapter:
                        containerXmlPath = os.path.join(contentPath, file.UUID())
                        text = File.read(containerXmlPath)
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
                    
    def _createReqPaths(exportDir: str):
        ExportHelper.wd = AppConfig.WORKING_DIR
        ExportHelper.exportDir = exportDir
        ExportHelper.metaPath = os.path.join(ExportHelper.exportDir, "META-INF")
        ExportHelper.oebpsPath = os.path.join(ExportHelper.exportDir, "OEBPS")
        ExportHelper.cssPath = os.path.join(ExportHelper.oebpsPath, "css")
        ExportHelper.imgPath = os.path.join(ExportHelper.oebpsPath, "images")           
    
    def _createReqDirectories():
        File.mkdir(ExportHelper.metaPath)
        File.mkdir(ExportHelper.oebpsPath)
        File.mkdir(ExportHelper.cssPath)
        File.mkdir(ExportHelper.imgPath)
        
    def _createReqFiles():
        wd = ExportHelper.wd
        exportDir = ExportHelper.exportDir
        
        mimePath = os.path.join(exportDir, "mimetype")
        File.write(mimePath, "application/epub+zip ")
        
        # container.xml
        containerXML = File.read(os.path.join(wd, "resources/templates/META-INF/container.xml"))
        containerXmlPath = os.path.join(ExportHelper.metaPath, "container.xml")
        File.write(containerXmlPath, containerXML)
        
        # content.opf
        contentOPF = File.read(os.path.join(wd, "resources/templates/OEBPS/content.opf"))
        contentOpfPath = os.path.join(ExportHelper.oebpsPath, "content.opf")
        File.write(contentOpfPath, contentOPF)
        
        # toc.ncx
        tocNCX = File.read(os.path.join(wd, "resources/templates/OEBPS/toc.ncx"))
        tocNcxPath = os.path.join(ExportHelper.oebpsPath, "toc.ncx")
        File.write(tocNcxPath, tocNCX)
        
        # css
        baseCSS = File.read(os.path.join(wd, "resources/templates/css/base.css"))
        baseCssPath = os.path.join(ExportHelper.cssPath, "base.css")
        File.write(baseCssPath, baseCSS)
                    
    def _createHtmlPage(body: str) -> str:
        tpath = "resources/templates/xhtml/export.xhtml"
        path = os.path.join(AppConfig.WORKING_DIR, tpath)
        template: str = File.read(path)
        if template is None:
            return ""

        body = textwrap.indent(body, "\t" * 2)
        template = template.replace("<!--body-->", body)
        
        return template