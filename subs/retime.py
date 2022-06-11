#!/usr/bin/env python3
"""Retime SRT files"""
import os

import pysrt

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Individual
# └─────────────────────────────────────────────────────────────────────────────
# filename = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Ajin\subs_ja\retimed2\Ajin_S01E05_ja.srt'
# srt = pysrt.open(filename)
# srt.shift(seconds=-0.7)
# srt.save(filename.replace('retimed', 'retimedwell'), encoding='utf-8')

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Directory
# └─────────────────────────────────────────────────────────────────────────────
start_dir = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Ajin\subs_ja\retimed2\\'
for root, dirs, files in os.walk(start_dir):
    my_files = [root + f for f in files]

for file in my_files:
    srt = pysrt.open(file)
    srt.shift(seconds=-12.9)
    srt.save(file, encoding='utf-8')
