#!/usr/bin/env python3
"""Glue together subtitles to facilitate study in Anki (2018/01/10)"""

import os
from statistics import mean

import pysrt

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
root = r'C:\~\Languages\ES\SUBS2SRS\El Bar'
root_srt = root + '/subs/srt/'
root_glued = root + '/subs/glued/'
TARGET_DURATION_MS = 12000

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Glue SRT
# └─────────────────────────────────────────────────────────────────────────────
def glue_subs(index: int, buffer: list[pysrt.SubRipItem]) -> pysrt.SubRipItem:
    start, end = buffer[0].start, buffer[-1].end
    text = ' '.join([sub.text_without_tags for sub in buffer])
    glued = pysrt.SubRipItem(index, start, end, text)
    return glued

srt_files = [f for f in os.listdir(root_srt) if 'glued' not in f]
for filename in srt_files:
    srt = pysrt.open(root_srt + filename)

    subs_glued, sub_buffer, index, process_buffer_flag = [], [], 1, False
    for i, sub in enumerate(srt):
        sub_buffer.append(sub)

        # Too much deadtime until next sub
        if i < len(srt) - 1:
            deadtime = srt[i + 1].start.ordinal - sub.end.ordinal
            if deadtime >= 7500: process_buffer_flag = True

        # Sub buffer exceeds target duration
        duration = sub_buffer[-1].end.ordinal - sub_buffer[0].start.ordinal
        if duration >= TARGET_DURATION_MS: process_buffer_flag = True

        # Process buffer
        if process_buffer_flag:
            new_sub = glue_subs(index, sub_buffer)
            subs_glued.append(new_sub)
            process_buffer_flag = False
            sub_buffer.clear()
            index += 1

    # Display stats
    durations = [_.duration.ordinal / 1000 for _ in subs_glued]
    print(filename)
    print(f'mean_duration: {mean(durations):.1f}')
    print(f'max_duration: {max(durations):.1f}')
    print(f'min_duration: {min(durations):.1f}\n')

    # Output glued files
    srt.data = subs_glued
    output_filename = root_glued + filename
    srt.save(output_filename, encoding='utf-8')
