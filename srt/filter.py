#!/usr/bin/env python3
"""Filter subtitles against target words/phrases"""

import os
from statistics import mean

import pysrt

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Setup
# └─────────────────────────────────────────────────────────────────────────────
TARGET_WORD_FILE = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Black Lagoon\target_words.txt'
TARGET_DURATION_MS = 11000

root_orig = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Black Lagoon\\'
root_srt = root_orig + 'subs_ja/srt/'
root_filtered = root_orig + 'subs_ja/filtered/'

# ┌─────────────────────────────────────────────────────────────────────────────
# │ Filter
# └─────────────────────────────────────────────────────────────────────────────
# Load up target words and SRT files
with open(TARGET_WORD_FILE, 'r', encoding='utf-8') as f:
    target_words = [line.strip() for line in f]

for root, dirs, files in os.walk(root_srt):
    srt_files = files

# Filter SRT files against target words
def glue_subs(index: int, buffer: list[pysrt.SubRipItem]) -> pysrt.SubRipItem:
    start, end = buffer[0].start, buffer[-1].end
    text = ' '.join([sub.text_without_tags for sub in buffer])
    glued = pysrt.SubRipItem(index, start, end, text)
    return glued

def build_out_context(srt: pysrt.SubRipFile, i: int, main_index: int) -> pysrt.SubRipItem:
    """Bi-directionally expand subs around srt[i] until duration > TARGET_DURATION_MS."""
    working_sub = srt[i]

    j, oscillator, sub_buffer, process_buffer_flag = 0, [0, 0], [srt[i]], False
    while sub_buffer[-1].end.ordinal - sub_buffer[0].start.ordinal <= TARGET_DURATION_MS:
        if j % 2 == 0:
            oscillator[0] -= 1
            oscillator[1] += 1
            k = oscillator[0]
        else:
            k = oscillator[1]
        j += 1

        # Handle BOF/EOF issues
        try:
            candidate_sub = srt[i + k]
        except IndexError:
            continue

        # Handle deadtime issues
        if k < 0:
            deadtime = sub_buffer[0].start.ordinal - candidate_sub.end.ordinal
        else:
            deadtime = candidate_sub.start.ordinal - sub_buffer[-1].end.ordinal
        if deadtime >= 7500: continue

        # Build out context in appropriate direction
        if k < 0:
            sub_buffer.insert(0, candidate_sub)
        else:
            sub_buffer.append(candidate_sub)


    new_sub = glue_subs(main_index, sub_buffer)
    return new_sub

# Main loop
for filename in srt_files:
    filtered_subs = []
    srt = pysrt.open(root_srt + filename)

    main_index = 1
    for i, sub in enumerate(srt):
        sub.text = sub.text_without_tags.replace('\n', '')
        for word in target_words:
            if word in sub.text:
                target_words.remove(word)
                new_sub = build_out_context(srt, i, main_index)
                filtered_subs.append(new_sub)
                main_index += 1

    if filtered_subs:
        srt.data = filtered_subs
        output_filename = root_filtered + filename
        srt.save(output_filename, encoding='utf-8')
        mean_duration = mean([sub.end.ordinal - sub.start.ordinal for sub in filtered_subs])

print(target_words)
print(mean_duration)
