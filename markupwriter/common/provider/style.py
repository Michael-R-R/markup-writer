#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QDir,
)

from markupwriter.common.util import (
    File,
)


class Style(object):
    TREE_VIEW: str = None
    EDITOR_VIEW: str = None
    PREVIEW_VIEW: str = None
    
    def init(wd: str):
        QDir.addSearchPath("styles", os.path.join(wd, "resources/styles/"))

        Style.TREE_VIEW: str = File.read("styles:tree_view.qss")
        Style.EDITOR_VIEW: str = File.read("styles:editor_view.qss")
        Style.PREVIEW_VIEW: str = File.read("styles:preview_view.qss")
