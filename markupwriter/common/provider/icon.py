#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
)

from PyQt6.QtGui import (
    QIcon,
)


class Icon(object):
    QDir.addSearchPath("icons", "./resources/icons/")

    # Common
    BOOKS = QIcon("icons:common/books.svg")
    CHECK = QIcon("icons:common/check.svg")
    UNCHECK = QIcon("icons:common/uncheck.svg")
    UP_ARROW = QIcon("icons:common/up_arrow.svg")
    DOWN_ARROW = QIcon("icons:common/down_arrow.svg")
    ADD_ITEM = QIcon("icons:common/add_item.svg")
    MORE_OPTIONS = QIcon("icons:common/more_options.svg")

    # Folders
    NOVEL_FOLDER = QIcon("icons:folder/novel.svg")
    PLOT_FOLDER = QIcon("icons:folder/plot.svg")
    TIMELINE_FOLDER = QIcon("icons:folder/timeline.svg")
    CHARACTERS_FOLDER = QIcon("icons:folder/characters.svg")
    LOCATIONS_FOLDER = QIcon("icons:folder/locations.svg")
    OBJECTS_FOLDER = QIcon("icons:folder/objects.svg")
    TRASH_FOLDER = QIcon("icons:folder/trash.svg")
    MISC_FOLDER = QIcon("icons:folder/misc_folder.svg")

    # Files
    TITLE_FILE = QIcon("icons:file/title_page.svg")
    CHAPTER_FILE = QIcon("icons:file/chapter.svg")
    SCENE_FILE = QIcon("icons:file/scene.svg")
    SECTION_FILE = QIcon("icons:file/section.svg")
    MISC_FILE = QIcon("icons:file/misc_file.svg")
