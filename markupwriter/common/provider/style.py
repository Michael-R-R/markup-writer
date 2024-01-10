#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
)

from markupwriter.common.util import (
    File,
)

class Style(object):
    QDir.addSearchPath("styles", "./resources/styles/")  

    EDITOR_VIEW: str = File.read("styles:editor_view.qss")
    TREE_VIEW: str = File.read("styles:tree_view.qss")
