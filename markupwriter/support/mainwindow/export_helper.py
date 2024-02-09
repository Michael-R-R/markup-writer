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
            item = widget.value
            if item is None:
                return

            ExportHelper._createReqPaths(widget.dir)
            ExportHelper._createReqDirectories()
            ExportHelper._createReqFiles()

            pages: list[(str, str)] = ExportHelper._createPages(dtc, item)

            ExportHelper._createResources(pages)
            ExportHelper._createContentOPF(pages)

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

        # mimetype
        mimePath = os.path.join(exportDir, "mimetype")
        File.write(mimePath, "application/epub+zip ")

        # container.xml
        src = os.path.join(wd, "resources/templates/META-INF/container.xml")
        dst = os.path.join(ExportHelper.metaPath, "container.xml")
        shutil.copyfile(src, dst)

        # css
        src = os.path.join(wd, "resources/templates/css/base.css")
        dst = os.path.join(ExportHelper.cssPath, "base.css")
        shutil.copyfile(src, dst)

    def _createPages(
        dtc: wcore.DocumentTreeController, item: QTreeWidgetItem
    ) -> list[str]:
        pages: list[(str, str)] = list()

        if item is not None:
            contentPath = AppConfig.projectContentPath()

            count = 0
            buildList = dtc.buildExportTree(item)
            for c in buildList:
                title = ""
                cbody = ""

                if len(c) > 0:
                    title = "{}_{}".format(count, c[0].title())
                    count += 1

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

                page = ExportHelper._createXHtmlPage(cbody)

                pages.append((title, page))

        return pages

    def _createResources(pages: list[(str, str)]):
        # TODO create css/img/etc. resources

        for p in pages:
            fName = "{}.xhtml".format(p[0])
            path = os.path.join(ExportHelper.oebpsPath, fName)
            File.write(path, p[1])

    def _createContentOPF(pages: list[(str, str)]):
        tpath = os.path.join(ExportHelper.wd, "resources/templates/OEBPS/content.opf")
        opf: str = File.read(tpath)

        # TODO replace metadata

        spine = ""
        manifest = "<item id='base-css' href='css/base.css' media-type='text/css'/>\n"

        # TODO add img items

        for p in pages:
            itemRef = "<itemref idref='{}'/>\n".format(p[0])
            item = "<item id='{}' href='{}.xhtml' media-type='application/xhtml+xml'/>\n".format(
                p[0], p[0]
            )

            spine += itemRef
            manifest += item

        manifest = textwrap.indent(manifest, "\t")
        spine = textwrap.indent(spine, "\t")

        opf = opf.replace(r"%manifest%", manifest)
        opf = opf.replace(r"%spine%", spine)

        wpath = os.path.join(ExportHelper.oebpsPath, "content.opf")
        File.write(wpath, opf)

    def _createXHtmlPage(body: str) -> str:
        tpath = "resources/templates/xhtml/export.xhtml"
        path = os.path.join(AppConfig.WORKING_DIR, tpath)
        template: str = File.read(path)
        if template is None:
            return ""

        body = textwrap.indent(body, "\t" * 2)
        template = template.replace("<!--body-->", body)

        return template
