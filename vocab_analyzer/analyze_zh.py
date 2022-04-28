#!/usr/bin/env python3
"""Analyze a new piece of Chinese content"""

from collections import Counter
from datetime import datetime
import json
import re

from common import is_cjk_ideograph

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
TITLE = '我們是朋友嗎？'
INPUT_FILE = r'C:\Users\pete\ALL\Languages\ZH\_alltexts\Just Friends.txt'
timestamp = f'{datetime.now():%Y-%m-%d %H:%M:%S}'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Character-Based Analysis
# └─────────────────────────────────────────────────────────────────────────────
# Load up necessary data
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    fulltext = f.read()

with open('known_chars.json', 'r', encoding='utf-8') as f:
    known_chars = json.load(f)

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
