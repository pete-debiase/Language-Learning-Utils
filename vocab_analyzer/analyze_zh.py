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

with open('seen_chars_zh.json', 'r', encoding='utf-8') as f:
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
filename = r'C:\Users\pete\ALL\Languages\ZH\CEDICT\cedict_ts.json'
with open(filename, 'r', encoding='utf-8') as f:
    cedict = json.load(f)

with open('seen_words_zh.json', 'r', encoding='utf-8') as f:
    seen_words = Counter(json.load(f))

filename = rf'C:\Users\pete\ALL\Languages\ZH\CEDICT\cedict_{CHARSET}_jieba.txt'
jieba.load_userdict(filename)

# Total words
seg_text = list(jieba.cut(fulltext, cut_all=False))
word_list = [word for word in seg_text if word in cedict] # Keep "real" words
word_list_new = [word for word in word_list if word not in seen_words]

# Unique words
seg_counter = Counter(seg_text)
unique_words = {k: v for k, v in Counter(word_list).most_common()}
print([k for k in seg_counter if k not in unique_words], '\n') # Should be mostly mis-segmented words

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

with open('seen_chars_zh.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_chars, f, indent=2, ensure_ascii=False)

with open('seen_words_zh.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_words, f, indent=2, ensure_ascii=False)

# Update seen content records
with open('seen_content_zh.json', 'r', encoding='utf-8') as f:
    seen_content = json.load(f)

new_content = {'time': f'{datetime.now():%Y-%m-%d %H:%M:%S}',
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
seen_content[TITLE] = new_content

with open('seen_content_zh.json', 'w+', newline='\n', encoding='utf-8') as f:
    json.dump(seen_content, f, indent=2, ensure_ascii=False)
