#!/usr/bin/env python3
"""Process annotated extensive reading text into Anki cards"""

import json
import re

source = '我們是朋友嗎？'

with open('../ZH/CEDICT/cedict_ts.json', 'r', encoding='utf-8') as f:
    cedict = json.load(f)

filename = r'C:\Users\pete\Dropbox\Just Friends.read'
with open(filename, 'r', encoding='utf-8') as f:
    text = [line.strip() for line in f]
text = [_ for _ in text if _ and '{' in _ and '}' in _]

tsv_anki = []
for sentence in text:
    targets = re.findall(r'\{(.*?)\}', sentence)
    for target in targets:
        sentence2 = sentence.replace(f'{{{target}}}', f'<span class="target">{target}</span>')
        sentence2 = sentence2.replace('{', '').replace('}', '')
        try:
            trad = cedict[target]['trad']
            simp = cedict[target]['simp']
            pinyin = cedict[target]['pinyin']
            defs = cedict[target]['defs']
        except KeyError:
            trad = simp = pinyin = 'none'
            defs = ''

        tsv = f'{sentence2}\t\t{trad}<br>{simp}<br>{pinyin}\t{defs}\t\t\t{source}'
        tsv_anki.append(tsv)


with open('../ZH/CEDICT/temp.tsv', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(tsv_anki))
