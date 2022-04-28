#!/usr/bin/env python3
"""Generate Anki cards from annotated extensive reading text"""

import json
import re

from airium import Airium

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
SOURCE = '我們是朋友嗎？'
INPUT_FILE = r'C:\Users\pete\Dropbox\Just Friends.read'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ CEDICT Lookup
# └─────────────────────────────────────────────────────────────────────────────
filename = r'C:\Users\pete\ALL\Languages\ZH\CEDICT\cedict_ts.json'
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
        pinyins_unicode = [entry['p'] for entry in cedict_entries]
        pinyins_numeric = [entry['p#'] for entry in cedict_entries]
        defs = [entry['d'] for entry in cedict_entries]

        # Tag pinyin
        pinyins_tagged = []
        for pu, pn in zip(pinyins_unicode, pinyins_numeric):
            pinyin_tagged = tonetag_pinyin(pu, pn)
            pinyins_tagged.append(pinyin_tagged)

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

def tonetag_pinyin(pinyin_unicode: str, pinyin_numeric: str) -> str:
    """Span-tag pinyin by tone (for displaying pinyin with color)."""
    syllables_tagged = []
    syllables_u, syllables_n = pinyin_unicode.split(' '), pinyin_numeric.split(' ')
    for syllable_u, syllable_n in zip(syllables_u, syllables_n):
        tone = re.findall(r'\d', syllable_n)[0]
        syllable_tagged = f'<span class="tone{tone}">{syllable_u}</span>'
        syllables_tagged.append(syllable_tagged)
    tagged_text = ' '.join(syllables_tagged)
    return tagged_text

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
        sentence = sentence.replace(f'{{{target}}}', f'<span class="target">{target}</span>')
        sentence = sentence.replace('{', '').replace('}', '')

        cedict_table = build_cedict_table(target)

        tsv = f'{sentence}\t\t{cedict_table}\t\t\t\t{SOURCE}'
        tsv_anki.append(tsv)

with open('temp.tsv', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(tsv_anki))
