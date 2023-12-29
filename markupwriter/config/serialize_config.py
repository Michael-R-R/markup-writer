#!/usr/bin/python

from .app_config import AppConfig
from .highlighter_config import HighlighterConfig
from .hotkey_config import HotkeyConfig
from markupwriter.util import (serialize, deserialize)

def writeConfig():
    serialize(AppConfig.INI_PATH, AppConfig())
    serialize(HighlighterConfig.INI_PATH, HighlighterConfig())
    serialize(HotkeyConfig.INI_PATH, HotkeyConfig())

def readConfig():
    deserialize(AppConfig, AppConfig.INI_PATH)
    deserialize(HighlighterConfig, HighlighterConfig.INI_PATH)
    deserialize(HotkeyConfig, HotkeyConfig.INI_PATH)
    