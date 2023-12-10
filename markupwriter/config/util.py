#!/usr/bin/python

from markupwriter.util.serialize import Serialize
from .app import AppConfig
from .highlighter import HighlighterConfig

def readConfig():
    Serialize.read(AppConfig, AppConfig.INI_PATH)
    Serialize.read(HighlighterConfig, HighlighterConfig.INI_PATH)

def writeConfig():
    Serialize.write(AppConfig.INI_PATH, AppConfig())
    Serialize.write(HighlighterConfig.INI_PATH, HighlighterConfig())