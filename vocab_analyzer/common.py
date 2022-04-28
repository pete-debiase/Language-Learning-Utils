#!/usr/bin/env python3
"""Common utilities for analyzing text"""

def is_cjk_ideograph(char: str):
    ranges = [
        {'from': ord(u'\u3300'), 'to': ord(u'\u33ff')},  # compatibility ideographs
        {'from': ord(u'\ufe30'), 'to': ord(u'\ufe4f')},  # compatibility ideographs
        {'from': ord(u'\uf900'), 'to': ord(u'\ufaff')},  # compatibility ideographs
        {'from': ord(u'\U0002F800'), 'to': ord(u'\U0002fa1f')},  # compatibility ideographs
        # {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},  # Japanese Hiragana
        # {'from': ord(u'\u30a0'), 'to': ord(u'\u30ff')},  # Japanese Katakana
        {'from': ord(u'\u2e80'), 'to': ord(u'\u2eff')},  # cjk radicals supplement
        {'from': ord(u'\u4e00'), 'to': ord(u'\u9fff')},
        {'from': ord(u'\u3400'), 'to': ord(u'\u4dbf')},
        {'from': ord(u'\U00020000'), 'to': ord(u'\U0002a6df')},
        {'from': ord(u'\U0002a700'), 'to': ord(u'\U0002b73f')},
        {'from': ord(u'\U0002b740'), 'to': ord(u'\U0002b81f')},
        {'from': ord(u'\U0002b820'), 'to': ord(u'\U0002ceaf')}  # included as of Unicode 8.0
    ]
    return any([r['from'] <= ord(char) <= r['to'] for r in ranges])
