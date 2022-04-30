#!/usr/bin/env python3
"""Analyze a new piece of Japanese content"""

from collections import Counter
from datetime import datetime
import json

import fugashi

from common_va import *
import haitou as ht

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
TITLE = 'Ghost in the Shell: Stand Alone Complex 1/2'
INPUT_FILE = r'C:\Users\pete\ALL\Languages\JA\_fulltexts\GITS_SAC.txt'
CONTENT_TYPE = 'show'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Character-Based Analysis
# └─────────────────────────────────────────────────────────────────────────────
# Load up necessary files
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    fulltext = f.read()

with open('seen_chars_ja.json', 'r', encoding='utf-8') as f:
    seen_chars = Counter(json.load(f))

# Total characters
text_no_whitespace = re.sub(r'\s', '', fulltext)
total_chars = len(text_no_whitespace)

# Unique characters
counter = Counter(fulltext)
unique_chars = {k: v for k, v in counter.most_common() if is_cjk_ideograph(k)}
print([k for k in counter if k not in unique_chars], '\n') # Should only be [a-zA-Z0-9] plus punctuation

# New characters
new_chars = [k for k in unique_chars if k not in seen_chars]

# Display stats
unique_char_report = kanken_analysis_relative(unique_chars)
new_char_report = kanken_analysis_relative(new_chars)

print(f'total_chars: {total_chars}')
print(new_char_report)
print(unique_char_report)

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Lemma-Based Analysis
# └─────────────────────────────────────────────────────────────────────────────
# Load up necessary files
with open('seen_lemmas_ja.json', 'r', encoding='utf-8') as f:
    seen_lemmas = Counter(json.load(f))

# Total lemmas/words
tagger = fugashi.Tagger()
word_list = [word.surface for word in tagger(fulltext)]
lemma_list = [word.feature.lemma for word in tagger(fulltext) if word.feature.lemma]
lemma_list_new = [lemma for lemma in lemma_list if lemma not in seen_lemmas]

# Unique lemmas/words
unique_lemmas = Counter(lemma_list)
unique_words = Counter(word_list)

# New lemmas
new_lemmas = [k for k in unique_lemmas if k not in seen_lemmas]

# Display stats
print(f'new_lemmas: {len(new_lemmas)}')
print(f'unique_lemmas: {len(unique_lemmas)}')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Create Vocab Candidate List
# └─────────────────────────────────────────────────────────────────────────────
# Find fancy words that contain non-jouyou kanji
vocab = []
fancy_kanji = [c for c in unique_chars if not ht.is_jouyou(c)]
for word in unique_words:
    contains_fanciness = any([c in word for c in fancy_kanji])
    if contains_fanciness: vocab.append(word)
print(vocab)

with open('vocab_raw.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(vocab))

# Find associated fancy contexts
contexts = []
for line in fulltext.split('\n'):
    for word in vocab:
        if word in line:
            context = line.replace(word, f'[{word}]')
            contexts.append(context)
            vocab.remove(word)

print(vocab)
with open('vocab_with_context.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(contexts))

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Update Records
# └─────────────────────────────────────────────────────────────────────────────
# Update seen characters and lemmas
seen_chars += Counter(unique_chars)
seen_lemmas += Counter(unique_lemmas)
seen_chars = dict(seen_chars.most_common()) # Keep sorted by freq
seen_lemmas = dict(seen_lemmas.most_common()) # Keep sorted by freq

with open('seen_chars_ja.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_chars, f, indent=2, ensure_ascii=False)

with open('seen_lemmas_ja.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_lemmas, f, indent=2, ensure_ascii=False)

# Update seen content records
with open('seen_content_ja.json', 'r', encoding='utf-8') as f:
    seen_content = json.load(f)

all_char_report = kanken_analysis_absolute(seen_chars)
non_kanken_chars = ''.join([c for c in unique_chars if not ht.is_kanken(c)])
content_summary = {'time': f'{datetime.now():%Y-%m-%d %H:%M:%S}',
                   'type': CONTENT_TYPE,
                   '#c': total_chars,
                   '%cn': round(len(new_chars) / len(unique_chars), 2),
                   '%ln': round(len(lemma_list_new) / len(lemma_list), 2),
                   '#cn': new_char_report,
                   '#ln': len(new_lemmas),
                   '#cq': unique_char_report,
                   '#lq': len(unique_lemmas),
                   'cn': ''.join(new_chars),
                   'ln': '|'.join(new_lemmas),
                   'cq': ''.join(unique_chars.keys()),
                   'lq': '|'.join(unique_lemmas.keys()),
                   'KK': all_char_report,
                   'NK': non_kanken_chars,
                   }
seen_content[TITLE] = content_summary

with open('seen_content_ja.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_content, f, indent=2, ensure_ascii=False)
