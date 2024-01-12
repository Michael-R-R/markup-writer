#!/usr/bin/python

from markupwriter.support.doctree.item import (
    BaseTreeItem,
    ChapterFileItem,
    MiscFileItem,
    SceneFileItem,
    SectionFileItem,
    TitleFileItem,
    CharsFolderItem,
    LocFolderItem,
    MiscFolderItem,
    NovelFolderItem,
    ObjFolderItem,
    PlotFolderItem,
    TimelineFolderItem,
    TrashFolderItem,
)


class TreeItemFactory(object):
    def make(type: str) -> BaseTreeItem:
        match type:
            case TitleFileItem.__name__:
                return TitleFileItem()
            case ChapterFileItem.__name__:
                return ChapterFileItem()
            case SceneFileItem.__name__:
                return SceneFileItem()
            case SectionFileItem.__name__:
                return SectionFileItem()
            case MiscFileItem.__name__:
                return MiscFileItem()
            case NovelFolderItem.__name__:
                return NovelFolderItem()
            case CharsFolderItem.__name__:
                return CharsFolderItem()
            case LocFolderItem.__name__:
                return LocFolderItem()
            case ObjFolderItem.__name__:
                return ObjFolderItem()
            case PlotFolderItem.__name__:
                return PlotFolderItem()
            case TimelineFolderItem.__name__:
                return TimelineFolderItem()
            case TrashFolderItem.__name__:
                return TrashFolderItem()
            case MiscFolderItem.__name__:
                return MiscFolderItem()
            case _:
                return None
