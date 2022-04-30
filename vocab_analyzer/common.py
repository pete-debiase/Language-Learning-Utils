#!/usr/bin/env python3
"""Common utilities for analyzing text"""

import json
import re

import zhon.hanzi as zh


def is_cjk_ideograph(char: str):
    ideographs = re.findall(rf'[{zh.characters}]', char)
    return bool(ideographs)

def kanken_analysis_relative(chars) -> str:
    """Analyze relative distribution of specified kanji by kanken level."""
    with open(r'C:\Users\pete\ALL\Languages\JA\漢検\haitou\haitou.json', 'r', encoding='utf-8') as f:
        haitou = json.load(f)
        jouyou = haitou['jouyou']
        level1kj = haitou['1kj']
        level1k = haitou['1k']
        all_kanken = jouyou | level1kj | level1k

    n_total = len(chars)
    n_jouyou = len([c for c in chars if c in jouyou])
    n_level1kj = len([c for c in chars if c in level1kj])
    n_level1k = len([c for c in chars if c in level1k])
    n_other = len([c for c in chars if c not in all_kanken])

    p_jouyou = n_jouyou / n_total
    p_level1kj = n_level1kj / n_total
    p_level1k = n_level1k / n_total

    r = f'{n_total} ' \
        f'[{n_jouyou} ({p_jouyou:.0%}) | ' \
        f'{n_level1kj} ({p_level1kj:.0%}) | ' \
        f'{n_level1k} ({p_level1k:.0%}) | ' \
        f'{n_other} ]'

    return r

def kanken_analysis_absolute(chars) -> str:
    """Analyze absolute distribution of specified kanji by kanken level."""
    with open(r'C:\Users\pete\ALL\Languages\JA\漢検\haitou\haitou.json', 'r', encoding='utf-8') as f:
        haitou = json.load(f)
        jouyou = haitou['jouyou']
        level1kj = haitou['1kj']
        level1k = haitou['1k']
        all_kanken = jouyou | level1kj | level1k

    n_local = len(chars)
    n_jouyou = len([c for c in chars if c in jouyou])
    n_level1kj = len([c for c in chars if c in level1kj])
    n_level1k = len([c for c in chars if c in level1k])
    n_other = len([c for c in chars if c not in all_kanken])

    p_all = n_local / len(all_kanken)
    p_jouyou = n_jouyou / len(jouyou)
    p_level1kj = n_level1kj / len(level1kj)
    p_level1k = n_level1k / len(level1k)

    r = f'{n_local} ({p_all:.0%}) ' \
        f'[{n_jouyou} ({p_jouyou:.0%}) | ' \
        f'{n_level1kj} ({p_level1kj:.0%}) | ' \
        f'{n_level1k} ({p_level1k:.0%}) | ' \
        f'{n_other} ]'

    return r
