#!/usr/bin/python

import os
import re
import shutil
import textwrap
import shutil

from PyQt6.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
)

from markupwriter.config import AppConfig, ProjectConfig
from markupwriter.common.util import File
from markupwriter.gui.dialogs.modal import ExportDialog, ErrorDialog
from markupwriter.common.tokenizers import XHtmlExportTokenizer
from markupwriter.common.parsers import XHtmlParser

import markupwriter.gui.widgets as w


class EpubExporter(object):
    def __init__(self) -> None:
        self.wd = ""
        self.exportDir = ""
        self.metaPath = ""
        self.oebpsPath = ""
        self.cssPath = ""
        self.fontsPath = ""
        self.imgPath = ""

    def export(self, tw: w.DocumentTreeWidget, parent: QWidget | None):
        widget = ExportDialog(tw, parent)
        if widget.exec() != 1:
            return

        exportDir = widget.dir
        item = widget.value
        if item is None:
            ErrorDialog.run("Error: selected item is 'None'", None)
            return

        self._setupPaths(exportDir)
        self._mkDirectories()
        self._mkFiles()
        self._create(tw, item)

    def _setupPaths(self, rootDir: str):
        self.wd = AppConfig.WORKING_DIR
        self.rootDir = rootDir
        self.exportDir = os.path.join(rootDir, "data")
        self.metaPath = os.path.join(self.exportDir, "META-INF")
        self.oebpsPath = os.path.join(self.exportDir, "OEBPS")
        self.cssPath = os.path.join(self.oebpsPath, "css")
        self.fontsPath = os.path.join(self.oebpsPath, "fonts")
        self.imgPath = os.path.join(self.oebpsPath, "images")
        self.textPath = os.path.join(self.oebpsPath, "text")

    def _mkDirectories(self):
        File.mkdir(self.exportDir)
        File.mkdir(self.metaPath)
        File.mkdir(self.oebpsPath)
        File.mkdir(self.cssPath)
        File.mkdir(self.fontsPath)
        File.mkdir(self.imgPath)
        File.mkdir(self.textPath)

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

    def _create(self, tw: w.DocumentTreeWidget, item: QTreeWidgetItem):
        contentPath = ProjectConfig.contentPath()
        manifest = ""
        spine = ""
        count = 0

        buildList = tw.buildExportList(item)
        for c in buildList:
            # Make xhtml body
            cbody = ""
            for file in c:
                path = os.path.join(contentPath, file.UUID())
                text = File.read(path)
                if text is None:
                    continue

                tokenizer = XHtmlExportTokenizer(text, None)
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
            manifest += self._parsePageManifest(title)
            spine += self._parseSpine(title)
            count += 1

        self._mkContentOPF(manifest, spine)
        self._mkEPUB3()

    def _mkPage(self, body: str) -> str:
        tpath = "resources/templates/xhtml/export.xhtml"
        path = os.path.join(self.wd, tpath)
        template: str = File.read(path)
        if template is None:
            return ""

        body = textwrap.indent(body, "\t" * 2)
        template = template.replace("<!--body-->", body)

        return template

    def _mkPageResources(self, title: str, page: str):
        # parse images
        srcRegex = re.compile(r"(?<=').*?(?=')")
        imgRegex = re.compile(r"<img src='.*?'\s")
        it = imgRegex.finditer(page)
        for found in it:
            tag = found.group(0)
            src = srcRegex.search(tag)
            if src is None:
                continue
            src = src.group(0)
            name = File.fileName(src)
            page = page.replace(tag, "<img src='../images/{}' ".format(name))
            path = os.path.join(self.imgPath, name)
            if File.exists(path):
                continue
            shutil.copyfile(src, path)

        # write page to disk
        fName = "{}.xhtml".format(title)
        path = os.path.join(self.textPath, fName)
        File.write(path, page)

    def _parsePageManifest(self, title: str) -> str:
        return "<item id='{}' href='text/{}.xhtml' media-type='application/xhtml+xml'/>\n".format(
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
            manifest += "<item id='{}' href='images/{}' media-type='image/{}'/>\n".format(
                n, n, ext
            )

        manifest = textwrap.indent(manifest, "\t")
        spine = textwrap.indent(spine, "\t")

        # create content.opf
        tpath = os.path.join(self.wd, "resources/templates/OEBPS/content.opf")
        opf: str = File.read(tpath)
        opf = opf.replace(r"%manifest%", manifest)
        opf = opf.replace(r"%spine%", spine)

        wpath = os.path.join(self.oebpsPath, "content.opf")
        File.write(wpath, opf)

    def _mkEPUB3(self):
        try:
            zipPath = os.path.join(self.rootDir, "novel")
            shutil.make_archive(zipPath, "zip", self.exportDir)
            os.rename(zipPath + ".zip", zipPath + ".epub")

        except Exception as e:
            ErrorDialog.run(str(e), None)
