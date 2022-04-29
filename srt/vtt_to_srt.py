#!/usr/bin/env python3
"""Scratch"""

import os
import re

import pysrt
import webvtt

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
TITLE = 'Ajin'
root_orig = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Ajin\\'
root_vtt = root_orig + 'subs_ja/vtt/'
root_srt = root_orig + 'subs_ja/srt/'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Convert
# └─────────────────────────────────────────────────────────────────────────────
for root, dirs, files in os.walk(root_vtt):
    vtt_files = [root + f for f in files]

for filename in vtt_files:
    season_ep = re.findall(r'_(S.*?)_', filename)[0]
    vtt = webvtt.read(filename)

    output_filename = root_srt + f'{TITLE}_{season_ep}_ja.srt'
    with open(output_filename, 'w+', newline='\n', encoding='utf-8') as file:
        vtt.write(file, format='srt')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Generate Fulltext
# └─────────────────────────────────────────────────────────────────────────────
for root, dirs, files in os.walk(root_srt):
    srt_files = [root + f for f in files]

fulltext = []
for filename in srt_files:
    srt = pysrt.open(filename)
    fulltext.extend([_.text.replace('\n', '') for _ in srt])

with open(f'{TITLE}.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(fulltext))
