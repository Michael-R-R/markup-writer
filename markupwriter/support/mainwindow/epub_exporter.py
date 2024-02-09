#!/usr/bin/python

import os
import shutil
import textwrap

from PyQt6.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File
from markupwriter.widgets import ExportSelectWidget
from markupwriter.common.tokenizers import XHtmlTokenizer
from markupwriter.common.parsers import XHtmlParser

import markupwriter.mvc.controller.corewidgets as wcore


class EpubExporter(object):
    def __init__(self) -> None:
        self.wd = ""
        self.exportDir = ""
        self.metaPath = ""
        self.oebpsPath = ""
        self.cssPath = ""
        self.imgPath = ""

    def export(self, dtc: wcore.DocumentTreeController, parent: QWidget | None):
        widget = ExportSelectWidget(dtc.view.treewidget, parent)
        if widget.exec() != 1:
            return

        exportDir = widget.dir
        item = widget.value
        if item is None:
            return

        self._setupPaths(exportDir)
        self._mkDirectories()
        self._mkFiles()
        self._createPages(dtc, item)

    def _setupPaths(self, exportDir: str):
        self.wd = AppConfig.WORKING_DIR
        self.exportDir = exportDir
        self.metaPath = os.path.join(exportDir, "META-INF")
        self.oebpsPath = os.path.join(exportDir, "OEBPS")
        self.cssPath = os.path.join(self.oebpsPath, "css")
        self.imgPath = os.path.join(self.oebpsPath, "images")

    def _mkDirectories(self):
        File.mkdir(self.metaPath)
        File.mkdir(self.oebpsPath)
        File.mkdir(self.cssPath)
        File.mkdir(self.imgPath)

    def _mkFiles(self):
        # mimetype
        mimePath = os.path.join(self.exportDir, "mimetype")
        File.write(mimePath, "application/epub+zip ")

        # container.xml
        src = os.path.join(self.wd, "resources/templates/META-INF/container.xml")
        dst = os.path.join(self.metaPath, "container.xml")
        shutil.copyfile(src, dst)

        # css
        src = os.path.join(self.wd, "resources/templates/css/base.css")
        dst = os.path.join(self.cssPath, "base.css")
        shutil.copyfile(src, dst)

    def _createPages(self, dtc: wcore.DocumentTreeController, item: QTreeWidgetItem):
        if item is None:
            return

        contentPath = AppConfig.projectContentPath()
        manifest = ""
        spine = ""
        count = 0

        buildList = dtc.buildExportTree(item)
        for c in buildList:
            # Make xhtml body
            cbody = ""
            for file in c:
                path = os.path.join(contentPath, file.UUID())
                text = File.read(path)
                if text is None:
                    continue

                tokenizer = XHtmlTokenizer(text, None)
                tokenizer.run()

                parser = XHtmlParser(tokenizer.tokens, None)
                parser.run()

                cbody += parser.body

            # Process xhtml body
            title = "{}_{}".format(count, c[0].title()) if len(c) > 0 else ""
            if title == "":
                continue
            page = self._mkPage(cbody)
            self._mkPageResources(title, page)
            manifest += self._parseManifest(title)
            spine += self._parseSpine(title)
            self._mkContentOPF(manifest, spine)
            count += 1

    def _mkPage(self, body: str) -> str:
        tpath = "resources/templates/xhtml/export.xhtml"
        path = os.path.join(self.wd, tpath)
        template: str = File.read(path)
        if template is None:
            return ""

        body = textwrap.indent(body, "\t" * 3)
        template = template.replace("<!--body-->", body)

        return template

    def _mkPageResources(self, title: str, page: str):
        # TODO parse page for css/img/etc. resources

        # write page to disk
        fName = "{}.xhtml".format(title)
        path = os.path.join(self.oebpsPath, fName)
        File.write(path, page)

    def _parseManifest(self, title: str) -> str:
        return "<item id='{}' href='{}.xhtml' media-type='application/xhtml+xml'/>\n".format(
            title, title
        )

    def _parseSpine(self, title: str) -> str:
        return "<itemref idref='{}'/>\n".format(title)

    def _mkContentOPF(self, manifest: str, spine: str):
        # add css resources to manifest
        names = File.findAllFiles(self.cssPath)
        for n in names:
            manifest += "<item id='{}' href='css/{}' media-type='text/css'/>\n".format(
                n, n
            )
            
        # add img resources to manifest
        names = File.findAllFiles(self.imgPath)
        for n in names:
            ext = File.fileExtension(n)
            manifest += "<item id='{}' href='images/{}' media-type='image/{}'/>".format(n, n, ext)
            
        # TODO replace metadata
            
        manifest = textwrap.indent(manifest, "\t")
        spine = textwrap.indent(spine, "\t")
        
        # create content.opf
        tpath = os.path.join(self.wd, "resources/templates/OEBPS/content.opf")
        opf: str = File.read(tpath)
        opf = opf.replace(r"%manifest%", manifest)
        opf = opf.replace(r"%spine%", spine)
        
        wpath = os.path.join(self.oebpsPath, "content.opf")
        File.write(wpath, opf)
