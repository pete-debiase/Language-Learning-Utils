#!/usr/bin/env python3
"""Retime SRT files"""

import pysrt

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
input_filename = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Ajin\subs_ja\srt\Ajin_S01E06_ja.srt'
output_filename = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Ajin\subs_ja\retimed\Ajin_S01E06_ja.srt'
srt = pysrt.open(input_filename)
srt.shift(seconds=12.2)
srt.save(output_filename, encoding='utf-8')
