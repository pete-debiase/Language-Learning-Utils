#!/usr/bin/env python3
"""Convert VTT to SRT"""

import os
import re

import pysrt
import webvtt

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
LANGUAGE = '_ja'
TITLE = '86 EIGHTY-SIX'
root_orig = rf'C:\~\Languages\JA\SUBS2SRS\{TITLE}\\'
root_vtt = root_orig + 'subs_ja/vtt/'
root_srt = root_orig + 'subs_ja/srt/'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Convert
# └─────────────────────────────────────────────────────────────────────────────
for root, dirs, files in os.walk(root_vtt):
    vtt_files = [root + f for f in files]

for filename in vtt_files:
    vtt = webvtt.read(filename)
    output_filename = root_srt + os.path.basename(filename).replace('.vtt', '.srt')
    with open(output_filename, 'w+', newline='\n', encoding='utf-8') as file:
        vtt.write(file, format='srt')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Clean SRT + Generate Fulltext
# └─────────────────────────────────────────────────────────────────────────────
for root, dirs, files in os.walk(root_srt):
    srt_files = [root + f for f in files if LANGUAGE in f]

fulltext = []
for filename in srt_files:
    srt = pysrt.open(filename)
    for sub in srt:
        sub.text = sub.text_without_tags
        sub.text = sub.text.replace('&lrm;', '')
        sub.text = sub.text.replace('\n', ' ')
        sub.text = re.sub(r'^-', ' ', sub.text)
        sub.text = sub.text.replace(' -', ' ')
        sub.text = sub.text.strip()
    srt.save(filename, encoding='utf-8')
    fulltext.extend([_.text for _ in srt])

with open(root_orig + f'{TITLE}.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(fulltext))
