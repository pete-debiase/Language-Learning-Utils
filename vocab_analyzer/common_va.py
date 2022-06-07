#!/usr/bin/env python3
"""Common utilities for analyzing text"""

import re

import zhon.hanzi as zh

from haitou import Haitou


def is_cjk_ideograph(char: str):
    ideographs = re.findall(rf'[{zh.characters}]', char)
    return bool(ideographs)

def kanken_analysis_relative(chars) -> str:
    """Analyze relative distribution of specified kanji by kanken level."""
    ht = Haitou()
    n_total = len(chars)
    n_jouyou = len([c for c in chars if ht.is_jouyou(c)])
    n_level1kj = len([c for c in chars if ht.is_level_1kj(c)])
    n_level1k = len([c for c in chars if ht.is_level_1k(c)])
    n_other = len([c for c in chars if not ht.is_kanken(c)])

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
    ht = Haitou()
    n_local = len(chars)
    n_jouyou = len([c for c in chars if ht.is_jouyou(c)])
    n_level1kj = len([c for c in chars if ht.is_level_1kj(c)])
    n_level1k = len([c for c in chars if ht.is_level_1k(c)])
    n_other = len([c for c in chars if not ht.is_kanken(c)])

    p_all = n_local / len(ht.all_kanken)
    p_jouyou = n_jouyou / len(ht.jouyou)
    p_level1kj = n_level1kj / len(ht.level_1kj)
    p_level1k = n_level1k / len(ht.level_1k)

    r = f'{n_local} ({p_all:.0%}) ' \
        f'[{n_jouyou} ({p_jouyou:.0%}) | ' \
        f'{n_level1kj} ({p_level1kj:.0%}) | ' \
        f'{n_level1k} ({p_level1k:.0%}) | ' \
        f'{n_other} ]'

    return r
