#!/usr/bin/env python3
"""Post-process TSV file generated by SUBS2SRS"""

import re

from airium import Airium
from jamdict import Jamdict

TARGET_WORD_FILE = r'C:\~\Languages\JA\SUBS2SRS\86 EIGHTY-SIX\target_words.txt'
jam = Jamdict()

def build_jamdict_table(jam: Jamdict, word: str) -> str:
    """Build a nice HTML table for the specified string."""
    lookup_result = jam.lookup(word)
    jam_datas = []
    for entry in lookup_result.entries:
        kanji_forms = '<br>'.join([str(kf) for kf in entry.kanji_forms])
        kana_forms = '<br>'.join([str(kf).strip() for kf in entry.kana_forms])
        senses = [str(s) for s in entry.senses]
        senses = [re.sub(r'\(\((.*)\)\)', '', s).strip() for s in senses]
        jam_datas.append([kanji_forms, kana_forms, senses])

    # Generate/format HTML table
    a = Airium()
    with a.table():
        for jd in jam_datas:
            with a.tr():
                a.td(_t=jd[0])
                a.td(_t=jd[1])

                with a.td():
                    with a.ol():
                        [a.li(_t=_) for _ in jd[2]]

    table = str(a)
    table = re.sub(r'(\n\s+|\n)', '', table)  # Unindent/unwrap
    return table

with open(TARGET_WORD_FILE, 'r', encoding='utf-8') as f:
    words = [line.strip() for line in f]

tables = []
for word in words:
    table = build_jamdict_table(jam, word)
    tables.append(table)

with open('temp_tables.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(tables))
