# -*- coding: utf-8 -*-

from enum import IntEnum, unique


@unique
class ChunkTypes(IntEnum):
    OLD_PALETTE_4 = 0x0004
    OLD_PALETTE_11 = 0x0011
    LAYER = 0x2004
    CEL = 0x2005
    CEL_EXTRA = 0x2006
    COLOR_PROFILE = 0x2007
    EXTERNAL_FILES = 0x2008
    MASK = 0x2016  # DEPRECATED
    PATH = 0x2017
    TAGS = 0x2018
    PALETTE = 0x2019
    USER_DATA = 0x2020
    SLICE = 0x2022
    TILESET = 0x2023
