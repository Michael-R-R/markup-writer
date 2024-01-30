#!/usr/bin/python

import os

from markupwriter.common.util import (
    File,
)


class Style(object):
    MAIN_WINDOW: str = None
    TREE_VIEW: str = None
    EDITOR_VIEW: str = None
    PREVIEW_VIEW: str = None
    
    def init(wd: str):
        directory = os.path.join(wd, "resources/styles/")

        Style.MAIN_WINDOW: str = File.read(os.path.join(directory, "main_window.qss"))
        Style.TREE_VIEW: str = File.read(os.path.join(directory, "tree_view.qss"))
        Style.EDITOR_VIEW: str = File.read(os.path.join(directory, "editor_view.qss"))
        Style.PREVIEW_VIEW: str = File.read(os.path.join(directory, "preview_view.qss"))
