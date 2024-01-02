#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
)

from PyQt6.QtGui import (
    QIcon,
)

class Icon(object):
    QDir.addSearchPath("icons", "./resources/icons/")
    
    # Folders
    NOVEL_FOLDER = QIcon("icons:novel.svg")
    PLOT_FOLDER = QIcon("icons:plot.svg")
    TIMELINE_FOLDER = QIcon("icons:timeline.svg")
    CHARACTERS_FOLDER = QIcon("icons:characters.svg")
    LOCATIONS_FOLDER = QIcon("icons:locations.svg")
    OBJECTS_FOLDER = QIcon("icons:folder.svg")
    TRASH_FOLDER = QIcon("icons:folder.svg")
    MISC_FOLDER = QIcon("icons:misc_folder.svg")

    # Files
    TITLE_FILE = QIcon("icons:title_page.svg")
    CHAPTER_FILE = QIcon("icons:chapter.svg")
    SCENE_FILE = QIcon("icons:scene.svg")
    SECTION_FILE = QIcon("icons:section.svg")
    MISC_FILE = QIcon("icons:misc_file.svg")

    # Misc
    CHECK = QIcon("icons:check.svg")
    UNCHECK = QIcon("icons:uncheck.svg")
    UP_ARROW = QIcon("icons:up_arrow.svg")
    DOWN_ARROW = QIcon("icons:down_arrow.svg")
    ADD_ITEM = QIcon("icons:add_item.svg")
    MORE_OPTIONS = QIcon("icons:more_options.svg")
