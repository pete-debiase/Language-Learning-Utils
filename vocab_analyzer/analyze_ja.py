#!/usr/bin/env python3
"""Analyze a new piece of Japanese content"""

from collections import Counter
from datetime import datetime
import json
import re

import fugashi

from common import is_cjk_ideograph

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
TITLE = 'FLCL'
INPUT_FILE = r'C:\Users\pete\ALL\Languages\JA\_fulltexts\FLCL.txt'
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
print(f'total_chars: {total_chars}')
print(f'unique_chars: {len(unique_chars)}')
print(f'new_chars: {len(new_chars)}')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Word-Based Analysis
# └─────────────────────────────────────────────────────────────────────────────
# Load up necessary files
with open('seen_words_ja.json', 'r', encoding='utf-8') as f:
    seen_words = Counter(json.load(f))

# Total words
tagger = fugashi.Tagger()
word_list = [word.feature.lemma for word in tagger(fulltext) if word.feature.lemma]
word_list_new = [word for word in word_list if word not in seen_words]

# Unique words
unique_words = Counter(word_list)

# New words
new_words = [k for k in unique_words if k not in seen_words]

# Display stats
print(f'unique_words: {len(unique_words)}')
print(f'new_words: {len(new_words)}')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Update Records
# └─────────────────────────────────────────────────────────────────────────────
# Update seen characters and words
seen_chars += Counter(unique_chars)
seen_words += Counter(unique_words)
seen_chars = dict(seen_chars.most_common()) # Keep sorted by freq
seen_words = dict(seen_words.most_common()) # Keep sorted by freq

with open('seen_chars_ja.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_chars, f, indent=2, ensure_ascii=False)

with open('seen_words_ja.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_words, f, indent=2, ensure_ascii=False)

# Update seen content records
with open('seen_content_ja.json', 'r', encoding='utf-8') as f:
    seen_content = json.load(f)

content_summary = {'time': f'{datetime.now():%Y-%m-%d %H:%M:%S}',
                   'type': CONTENT_TYPE,
                   '#c': total_chars,
                   '#cn': len(new_chars),
                   '#wn': len(new_words),
                   '%cn': round(len(new_chars) / len(unique_chars), 2),
                   '%wn': round(len(word_list_new) / len(word_list), 2),
                   '#cq': len(unique_chars),
                   '#wq': len(unique_words),
                   'cn': ''.join(new_chars),
                   'wn': '|'.join(new_words),
                   'cq': ''.join(unique_chars.keys()),
                   'wq': '|'.join(unique_words.keys()),
                   }
seen_content[TITLE] = content_summary

with open('seen_content_ja.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_content, f, indent=2, ensure_ascii=False)
