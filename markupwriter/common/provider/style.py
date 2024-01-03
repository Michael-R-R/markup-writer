#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
)

from markupwriter.util import (
    File,
)

class Style(object):
    QDir.addSearchPath("styles", "./resources/styles/")  

    EDITOR = File.read("styles:editor.qss")
    TREE_VIEW = File.read("styles:tree_view.qss")
