#!/usr/bin/python

import os

from PyQt6.QtGui import (
    QIcon,
)


class Icon(object):
    # Common
    PLACE_HOLDER: QIcon = None
    BOOKS: QIcon = None
    CHECK: QIcon = None
    UNCHECK: QIcon = None
    UP_ARROW: QIcon = None
    DOWN_ARROW: QIcon = None
    ADD_ITEM: QIcon = None
    MORE_OPTIONS: QIcon = None
    FILTER: QIcon = None

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
    
    def init(wd: str):
        dir = os.path.join(wd, "resources/icons/")
        
        Icon.PLACE_HOLDER = QIcon(os.path.join(dir, "common/holder.svg"))

        # Common
        Icon.BOOKS = QIcon(os.path.join(dir, "common/books.svg"))
        Icon.CHECK = QIcon(os.path.join(dir, "common/check.svg"))
        Icon.UNCHECK = QIcon(os.path.join(dir, "common/uncheck.svg"))
        Icon.UP_ARROW = QIcon(os.path.join(dir, "common/up_arrow.svg"))
        Icon.DOWN_ARROW = QIcon(os.path.join(dir, "common/down_arrow.svg"))
        Icon.ADD_ITEM = QIcon(os.path.join(dir, "common/add_item.svg"))
        Icon.MORE_OPTIONS = QIcon(os.path.join(dir, "common/more_options.svg"))
        Icon.FILTER = QIcon(os.path.join(dir, "common/filter.svg"))

        # Folders
        Icon.NOVEL_FOLDER = QIcon(os.path.join(dir, "folder/novel.svg"))
        Icon.PLOT_FOLDER = QIcon(os.path.join(dir, "folder/plot.svg"))
        Icon.TIMELINE_FOLDER = QIcon(os.path.join(dir, "folder/timeline.svg"))
        Icon.CHARACTERS_FOLDER = QIcon(os.path.join(dir, "folder/characters.svg"))
        Icon.LOCATIONS_FOLDER = QIcon(os.path.join(dir, "folder/locations.svg"))
        Icon.OBJECTS_FOLDER = QIcon(os.path.join(dir, "folder/objects.svg"))
        Icon.TRASH_FOLDER = QIcon(os.path.join(dir, "folder/trash.svg"))
        Icon.MISC_FOLDER = QIcon(os.path.join(dir, "folder/misc_folder.svg"))

        # Files
        Icon.TITLE_FILE = QIcon(os.path.join(dir, "file/title_page.svg"))
        Icon.CHAPTER_FILE = QIcon(os.path.join(dir, "file/chapter.svg"))
        Icon.SCENE_FILE = QIcon(os.path.join(dir, "file/scene.svg"))
        Icon.SECTION_FILE = QIcon(os.path.join(dir, "file/section.svg"))
        Icon.MISC_FILE = QIcon(os.path.join(dir, "file/misc_file.svg"))
