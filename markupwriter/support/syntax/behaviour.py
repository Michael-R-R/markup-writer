#!/usr/bin/python

from enum import Enum, auto

class BEHAVIOUR(Enum):
    refTag = auto()
    aliasTag = auto()
    comment = auto()
    keyword = auto()