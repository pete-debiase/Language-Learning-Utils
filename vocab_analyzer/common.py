#!/usr/bin/env python3
"""Common utilities for analyzing text"""

import re

import zhon.hanzi as zh


def is_cjk_ideograph(char: str):
    ideographs = re.findall(rf'[{zh.characters}]', char)
    return bool(ideographs)
