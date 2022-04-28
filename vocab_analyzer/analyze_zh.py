#!/usr/bin/env python3
"""Analyze a new piece of Chinese content"""

from collections import Counter
from datetime import datetime
import json
import re

import jieba

from common import is_cjk_ideograph

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
TITLE = '我們是朋友嗎？'
INPUT_FILE = r'C:\Users\pete\ALL\Languages\ZH\_alltexts\Just Friends.txt'
CHARSET = 't' # t = traditional, s = simplified

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Character-Based Analysis
# └─────────────────────────────────────────────────────────────────────────────
# Load up necessary files
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    fulltext = f.read()

with open('known_chars.json', 'r', encoding='utf-8') as f:
    known_chars = Counter(json.load(f))

# Total characters
text_no_whitespace = re.sub(r'\s', '', fulltext)
total_chars = len(text_no_whitespace)

# Unique characters
counter = Counter(fulltext)
unique_chars = {k: v for k, v in counter.most_common() if is_cjk_ideograph(k)}
print([k for k in counter if k not in unique_chars], '\n') # Should only be [a-zA-Z0-9] plus punctuation

# Unknown characters
unknown_chars = [k for k in unique_chars if k not in known_chars]

# Display stats
print(f'total_chars: {total_chars}')
print(f'unique_chars: {len(unique_chars)}')
print(f'unknown_chars: {len(unknown_chars)}')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Word-Based Analysis
# └─────────────────────────────────────────────────────────────────────────────
# Load up necessary files
filename = r'C:\Users\pete\ALL\Languages\ZH\CEDICT\cedict_ts.json'
with open(filename, 'r', encoding='utf-8') as f:
    cedict = json.load(f)

with open('known_words.json', 'r', encoding='utf-8') as f:
    known_words = Counter(json.load(f))

filename = rf'C:\Users\pete\ALL\Languages\ZH\CEDICT\cedict_{CHARSET}_jieba.txt'
jieba.load_userdict(filename)

# Total words
seg_text = list(jieba.cut(fulltext, cut_all=False))
word_list = [word for word in seg_text if word in cedict] # Keep "real" words
word_list_unknown = [word for word in word_list if word not in known_words]

# Unique words
seg_counter = Counter(seg_text)
unique_words = {k: v for k, v in Counter(word_list).most_common()}
print([k for k in seg_counter if k not in unique_words], '\n') # Should be mostly mis-segmented words

# Unknown words
unknown_words = [k for k in unique_words if k not in known_words]

# Display stats
print(f'unique_words: {len(unique_words)}')
print(f'unknown_words: {len(unknown_words)}')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Update Records
# └─────────────────────────────────────────────────────────────────────────────
# Update known characters and words
known_chars += Counter(unique_chars)
known_words += Counter(unique_words)

with open('known_chars.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(known_chars, f, indent=2, ensure_ascii=False)

with open('known_words.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(known_words, f, indent=2, ensure_ascii=False)

# Update known content records
with open('known_content.json', 'r', encoding='utf-8') as f:
    known_content = json.load(f)

new_content = {'time': f'{datetime.now():%Y-%m-%d %H:%M:%S}',
               '#c': total_chars,
               '#cu': len(unknown_chars),
               '%cu': round(len(unknown_chars) / len(unique_chars), 2),
               '#wu': len(unknown_words),
               '%wu': round(len(word_list_unknown) / len(word_list), 2),
               '#cq': len(unique_chars),
               '#wq': len(unique_words),
               'cu': ''.join(unknown_chars),
               'wu': '|'.join(unknown_words),
               'cq': ''.join(unique_chars.keys()),
               'wq': '|'.join(unique_words.keys()),
               }
known_content[TITLE] = new_content

with open('known_content.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(known_content, f, indent=2, ensure_ascii=False)
