#!/usr/bin/env python3
"""Convert VTT to SRT"""

import os

import pysrt
import webvtt

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
LANGUAGE = '_es'
TITLE = 'Contratiempo'
root_orig = r'C:\~\Languages\ES\SUBS2SRS\Contratiempo\\'
root_vtt = root_orig + 'subs/vtt/'
root_srt = root_orig + 'subs/srt/'

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
        sub.text = sub.text.replace('&lrm;', '').replace('\n', ' ')
    srt.save(filename, encoding='utf-8')
    fulltext.extend([_.text for _ in srt])

with open(root_orig + f'{TITLE}.txt', 'w+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(fulltext))
