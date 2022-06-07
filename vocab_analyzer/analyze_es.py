#!/usr/bin/env python3
"""Analyze a new piece of Spanish content"""

from collections import Counter
from datetime import datetime
import json
import re

import spacy

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
TITLE = 'Contratiempo'
INPUT_FILE = r'C:\~\Languages\ES\_fulltexts\Contratiempo.txt'
CONTENT_TYPE = 'movie'

NONLEMMAS = {'.', '[', ']', ',', '?', '¿', '-', '¡', '!', '…', '“', '”'}

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Lemma-Based Analysis
# └─────────────────────────────────────────────────────────────────────────────
# Load up necessary files
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    fulltext = f.read().lower()
    fulltext = re.sub(r'( |\.|,)\d+( |\.|,)', ' ', fulltext) # Discard stand-alone numbers.
    fulltext = fulltext.replace('\n', ' ')

with open('seen_lemmas_es.json', 'r', encoding='utf-8') as f:
    seen_lemmas = Counter(json.load(f))

# Total lemmas
nlp = spacy.load('es_dep_news_trf')

tokens = nlp(fulltext)
lemmas = [t.lemma_ for t in tokens]
lemmas = [l.strip() for l in lemmas if l and l not in NONLEMMAS]

lemmas_new = [l for l in lemmas if l not in seen_lemmas]

# Unique lemmas
lemmas_unique = Counter(lemmas)
lemmas_new_unique = Counter(lemmas_new)

# Display stats
print(f'total_lemmas: {len(lemmas)}')
print(f'new_lemmas: {len(lemmas_new_unique)}')
print(f'unique_lemmas: {len(lemmas_unique)}')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Create Vocab Candidate List
# └─────────────────────────────────────────────────────────────────────────────
# TODO later...

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Update Records
# └─────────────────────────────────────────────────────────────────────────────
# Update seen characters and lemmas
seen_lemmas += lemmas_unique
seen_lemmas = dict(seen_lemmas.most_common()) # Keep sorted by freq

with open('seen_lemmas_es.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_lemmas, f, indent=2, ensure_ascii=False)

# Update seen content records
with open('seen_content_es.json', 'r', encoding='utf-8') as f:
    seen_content = json.load(f)

content_summary = {'time': f'{datetime.now():%Y-%m-%d %H:%M:%S}',
                   'type': CONTENT_TYPE,
                   '#l': len(lemmas),
                   '%ln': round(len(lemmas_new) / len(lemmas), 2),
                   '#ln': len(lemmas_new_unique),
                   '#lq': len(lemmas_unique),
                   'ln': '|'.join(lemmas_new_unique.keys()),
                   'lq': '|'.join(lemmas_unique.keys()),
                   }
seen_content[TITLE] = content_summary

with open('seen_content_es.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_content, f, indent=2, ensure_ascii=False)
