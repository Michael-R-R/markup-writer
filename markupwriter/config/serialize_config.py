#!/usr/bin/python

from .app import AppConfig
from .highlighter import HighlighterConfig
from markupwriter.util import (serialize, deserialize)

def writeConfig():
    serialize(AppConfig.INI_PATH, AppConfig())
    serialize(HighlighterConfig.INI_PATH, HighlighterConfig())

def readConfig():
    deserialize(AppConfig, AppConfig.INI_PATH)
    deserialize(HighlighterConfig, HighlighterConfig.INI_PATH)
    