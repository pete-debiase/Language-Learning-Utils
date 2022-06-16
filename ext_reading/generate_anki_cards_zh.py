#!/usr/bin/env python3
"""Generate Anki cards from annotated extensive reading text"""

import json
import re

from airium import Airium

from pinyin_tools import tonetag

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
SOURCE = '我的老師是火星人'
INPUT_FILE = r'C:\~\Media\Books\Reads In Progress\My Teacher Is a Martian.rd_cjk'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ CEDICT Lookup
# └─────────────────────────────────────────────────────────────────────────────
filename = r'C:\~\Languages\ZH\CEDICT\cedict_ts.json'
with open(filename, 'r', encoding='utf-8') as f:
    cedict = json.load(f)

def build_cedict_table(word: str) -> str:
    """Build a nice HTML table for the specified string."""
    try:
        # Look up in CEDICT
        cedict_entries = cedict[word]
        trad = cedict_entries[0]['t']
        simp = cedict_entries[0]['s']

        word = '<br>'.join(list(dict.fromkeys([trad, simp]))) # Preserve order
        pinyins_accented = [entry['p'] for entry in cedict_entries]
        defs = [entry['d'] for entry in cedict_entries]

        # Tonetag pinyin
        pinyins_tagged = []
        for p in pinyins_accented:
            p_tagged = tonetag(p)[0]
            pinyins_tagged.append(p_tagged)

        # Generate/format HTML table
        a = Airium()
        with a.table():
            for p, d in zip(pinyins_tagged, defs):
                td_cells = [word, p, d]
                with a.tr():
                    [a.td(_t=cell) for cell in td_cells]
        table = str(a)
        table = re.sub(r'(\n\s+|\n)', '', table) # Unindent/unwrap
    except KeyError:
        table = 'none'
    return table

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Process Input Text and Generate Anki TSV
# └─────────────────────────────────────────────────────────────────────────────
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    sentences = [line.strip() for line in f]
sentences = [_ for _ in sentences if _ and '{' in _ and '}' in _] # Sentences with {unknown words}

tsv_anki = []
for sentence in sentences:
    targets = re.findall(r'\{(.*?)\}', sentence)
    for target in targets:
        sentence_new = sentence.replace(f'{{{target}}}', f'<span class="target">{target}</span>')
        sentence_new = sentence_new.replace('{', '').replace('}', '')

        cedict_table = build_cedict_table(target)

        tsv = f'{sentence_new}\t\t{cedict_table}\t\t\t\t{SOURCE}'
        tsv_anki.append(tsv)

with open('temp.tsv', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(tsv_anki))
