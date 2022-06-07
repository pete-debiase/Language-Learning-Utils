#!/usr/bin/env python3
"""Programmatic access to Kanken haitou chart"""

import json

def is_jouyou(character: str) -> bool:
    """Determine whether specified character is a jouyou kanji."""
    jouyou = get_haitou()['jouyou']
    return character in jouyou

def is_level_1kj(character: str) -> bool:
    """Determine whether specified character is a jun1kyuu kanji."""
    level_1kj = get_haitou()['1kj']
    return character in level_1kj

def is_level_1k(character: str) -> bool:
    """Determine whether specified character is a 1kyuu kanji."""
    level_1k = get_haitou()['1k']
    return character in level_1k

def is_kanken(character: str) -> bool:
    """Determine whether specified character is a kanken kanji."""
    jouyou = get_haitou()['jouyou']
    level_1kj = get_haitou()['1kj']
    level_1k = get_haitou()['1k']
    all_kanken = jouyou | level_1kj | level_1k
    return character in all_kanken

def get_haitou():
    """Get a copy of the haitou chart."""
    with open('haitou.json', 'r', encoding='utf-8') as f:
        haitou = json.load(f)
    return haitou
