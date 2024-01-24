#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QDir,
)

from PyQt6.QtGui import (
    QIcon,
)


class Icon(object):
    # Common
    BOOKS: QIcon = None
    CHECK: QIcon = None
    UNCHECK: QIcon = None
    UP_ARROW: QIcon = None
    DOWN_ARROW: QIcon = None
    ADD_ITEM: QIcon = None
    MORE_OPTIONS: QIcon = None

    # Folders
    NOVEL_FOLDER: QIcon = None
    PLOT_FOLDER: QIcon = None
    TIMELINE_FOLDER: QIcon = None
    CHARACTERS_FOLDER: QIcon = None
    LOCATIONS_FOLDER: QIcon = None
    OBJECTS_FOLDER: QIcon = None
    TRASH_FOLDER: QIcon = None
    MISC_FOLDER: QIcon = None

    # Files
    TITLE_FILE: QIcon = None
    CHAPTER_FILE: QIcon = None
    SCENE_FILE: QIcon = None
    SECTION_FILE: QIcon = None
    MISC_FILE: QIcon = None
    
    def init(workingDir: str):
        QDir.addSearchPath("icons", os.path.join(workingDir, "resources/icons/"))

        # Common
        Icon.BOOKS = QIcon("icons:common/books.svg")
        Icon.CHECK = QIcon("icons:common/check.svg")
        Icon.UNCHECK = QIcon("icons:common/uncheck.svg")
        Icon.UP_ARROW = QIcon("icons:common/up_arrow.svg")
        Icon.DOWN_ARROW = QIcon("icons:common/down_arrow.svg")
        Icon.ADD_ITEM = QIcon("icons:common/add_item.svg")
        Icon.MORE_OPTIONS = QIcon("icons:common/more_options.svg")

        # Folders
        Icon.NOVEL_FOLDER = QIcon("icons:folder/novel.svg")
        Icon.PLOT_FOLDER = QIcon("icons:folder/plot.svg")
        Icon.TIMELINE_FOLDER = QIcon("icons:folder/timeline.svg")
        Icon.CHARACTERS_FOLDER = QIcon("icons:folder/characters.svg")
        Icon.LOCATIONS_FOLDER = QIcon("icons:folder/locations.svg")
        Icon.OBJECTS_FOLDER = QIcon("icons:folder/objects.svg")
        Icon.TRASH_FOLDER = QIcon("icons:folder/trash.svg")
        Icon.MISC_FOLDER = QIcon("icons:folder/misc_folder.svg")

        # Files
        Icon.TITLE_FILE = QIcon("icons:file/title_page.svg")
        Icon.CHAPTER_FILE = QIcon("icons:file/chapter.svg")
        Icon.SCENE_FILE = QIcon("icons:file/scene.svg")
        Icon.SECTION_FILE = QIcon("icons:file/section.svg")
        Icon.MISC_FILE = QIcon("icons:file/misc_file.svg")
