#!/usr/bin/python

from markupwriter.common.util import Serialize
from .app_config import AppConfig
from .highlighter_config import HighlighterConfig
from .hotkey_config import HotkeyConfig


class SerializeConfig(object):
    def read():
        Serialize.newRead(AppConfig, AppConfig.INI_PATH)
        Serialize.newRead(HighlighterConfig, HighlighterConfig.INI_PATH)
        Serialize.newRead(HotkeyConfig, HotkeyConfig.INI_PATH)

    def write():
        Serialize.write(AppConfig.INI_PATH, AppConfig())
        Serialize.write(HighlighterConfig.INI_PATH, HighlighterConfig())
        Serialize.write(HotkeyConfig.INI_PATH, HotkeyConfig())
