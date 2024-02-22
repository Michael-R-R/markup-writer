#!/usr/bin/python

from markupwriter.common.util import Serialize
from .app_config import AppConfig
from .highlighter_config import HighlighterConfig
from .hotkey_config import HotkeyConfig


class SerializeConfig(object):
    def read():
        Serialize.readFromFile(AppConfig, AppConfig.INI_PATH)
        Serialize.readFromFile(HighlighterConfig, HighlighterConfig.INI_PATH)
        Serialize.readFromFile(HotkeyConfig, HotkeyConfig.INI_PATH)

    def write():
        Serialize.writeToFile(AppConfig.INI_PATH, AppConfig())
        Serialize.writeToFile(HighlighterConfig.INI_PATH, HighlighterConfig())
        Serialize.writeToFile(HotkeyConfig.INI_PATH, HotkeyConfig())
