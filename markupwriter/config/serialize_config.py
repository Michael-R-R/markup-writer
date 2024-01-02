#!/usr/bin/python

from .app_config import AppConfig
from .highlighter_config import HighlighterConfig
from .hotkey_config import HotkeyConfig
from markupwriter.util import Serialize

def writeConfig():
    Serialize.write(AppConfig.INI_PATH, AppConfig())
    Serialize.write(HighlighterConfig.INI_PATH, HighlighterConfig())
    Serialize.write(HotkeyConfig.INI_PATH, HotkeyConfig())

def readConfig():
    Serialize.read(AppConfig, AppConfig.INI_PATH)
    Serialize.read(HighlighterConfig, HighlighterConfig.INI_PATH)
    Serialize.read(HotkeyConfig, HotkeyConfig.INI_PATH)
    