#!/usr/bin/env python3
"""Process annotated extensive reading text into Anki cards"""

import json
import re

from airium import Airium

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
SOURCE = '我們是朋友嗎？'
INPUT_FILE = r'C:\Users\pete\Dropbox\Just Friends.read'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Business
# └─────────────────────────────────────────────────────────────────────────────
filename = r'C:\Users\pete\ALL\Languages\ZH\CEDICT\cedict_ts.json'
with open(filename, 'r', encoding='utf-8') as f:
    cedict = json.load(f)

def build_cedict_table(word: str) -> str:
    """Build a nice HTML table for the specified string."""
    try:
        cedict_entries = cedict[word]
        trad = cedict_entries[0]['t']
        simp = cedict_entries[0]['s']

        word = '<br>'.join(list(dict.fromkeys([trad, simp])))
        pinyins = [entry['p'] for entry in cedict_entries]
        defs = [entry['d'] for entry in cedict_entries]

        a = Airium()
        with a.table():
            for p, d in zip(pinyins, defs):
                cells = [word, p, d]
                with a.tr():
                    [a.td(_t=cell) for cell in cells]

        table = str(a)
        table = table.replace('\n', '')
        table = re.sub(r'>\s+<', '><', table)
    except KeyError:
        table = 'none'
    return table


with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    text = [line.strip() for line in f]
text = [_ for _ in text if _ and '{' in _ and '}' in _]

tsv_anki = []
for sentence in text:
    targets = re.findall(r'\{(.*?)\}', sentence)
    for target in targets:
        sentence2 = sentence.replace(f'{{{target}}}', f'<span class="target">{target}</span>')
        sentence2 = sentence2.replace('{', '').replace('}', '')

        cedict_table = build_cedict_table(target)

        tsv = f'{sentence2}\t\t{cedict_table}\t\t\t\t{SOURCE}'
        tsv_anki.append(tsv)

with open('temp.tsv', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(tsv_anki))
