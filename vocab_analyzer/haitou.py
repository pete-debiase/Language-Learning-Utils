#!/usr/bin/env python3
"""Programmatic access to Kanken haitou chart"""

import json


class Haitou:
    """The Kanken haitou chart."""
    def __init__(self):
        haitou = self.get_haitou()
        self.jouyou = haitou['jouyou']
        self.level_1kj = haitou['1kj']
        self.level_1k = haitou['1k']
        self.all_kanken = self.jouyou | self.level_1kj | self.level_1k

    def is_jouyou(self, character: str) -> bool:
        """Determine whether specified character is a jouyou kanji."""
        return character in self.jouyou

    def is_level_1kj(self, character: str) -> bool:
        """Determine whether specified character is a jun1kyuu kanji."""
        return character in self.level_1kj

    def is_level_1k(self, character: str) -> bool:
        """Determine whether specified character is a 1kyuu kanji."""
        return character in self.level_1k

    def is_kanken(self, character: str) -> bool:
        """Determine whether specified character is a kanken kanji."""
        return character in self.all_kanken

    def get_haitou(self):
        """Get a working copy of the haitou chart."""
        with open('haitou.json', 'r', encoding='utf-8') as f:
            haitou = json.load(f)
        return haitou
