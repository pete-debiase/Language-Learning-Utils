#!/usr/bin/python
"""Glue together subtitles to facilitate study in Anki."""
# Pete Adriano DeBiase
# Created: 2018/01/10

import datetime
import os
import srt # https://github.com/cdown/srt

root_path = r'C:\Users\Pete\ALL-P70\Japanese\SUBS2SRS\Movies and Shows\FLCL\JP Subs'
match_pattern = 'FLCL'
os.chdir(root_path)
filenames = os.listdir()
filenames = [filename for filename in filenames if match_pattern in filename]

all_subs = []
total_subs_length = 0
unique_subs_length = 0
glued_subs_length = 0
for filename in filenames:
    with open(filename, 'r', encoding='utf-8') as file:
        subs = file.read()
    subs = list(srt.parse(subs))
    total_subs_length += len(subs)
    for sub in subs:
        sub.content = sub.content.replace('\n', '')

    # subs = [sub for sub in subs if sub.content not in all_subs]
    unique_subs_length += len(subs)
    all_subs.extend([sub.content for sub in subs])

    # average_duration = sum([(sub.end - sub.start) for sub in subs], datetime.timedelta())/len(subs)
    # print(average_duration)

    temp_sub = srt.Subtitle(1, datetime.timedelta(0, 0, 0), datetime.timedelta(0, 0, 0), '')
    glued_subs = []
    for i, sub in enumerate(subs):
        if temp_sub.start == datetime.timedelta(0, 0, 0):
            temp_sub.index = sub.index
            temp_sub.start = sub.start

        if i < len(subs) - 1:
            if (subs[i+1].start - sub.end) >= datetime.timedelta(0, 10, 0): # Avoid dead space.
                temp_sub.end = sub.end
                temp_sub.content += sub.content + '   '
                glued_subs.append(temp_sub)
                temp_sub = srt.Subtitle(1, datetime.timedelta(0, 0, 0), datetime.timedelta(0, 0, 0), '')
                continue

        temp_sub.end = sub.end
        temp_sub.content += sub.content + '   '

        if temp_sub.end - temp_sub.start >= datetime.timedelta(0, 34, 0):
            glued_subs.append(temp_sub)
            temp_sub = srt.Subtitle(1, datetime.timedelta(0, 0, 0), datetime.timedelta(0, 0, 0), '')

        if i == len(subs) - 1:
            glued_subs.append(temp_sub)
            temp_sub = srt.Subtitle(1, datetime.timedelta(0, 0, 0), datetime.timedelta(0, 0, 0), '')

    for sub in glued_subs:
        sub.content = sub.content.strip()
    glued_subs_length += len(glued_subs)

    output_path = root_path + '\\' + 'Glued\\' + filename
    with open(output_path, 'w+', encoding='utf-8') as file:
        file.write(srt.compose(glued_subs))

print(f"Total Subs: {total_subs_length}")
print(f"Unique Subs: {unique_subs_length}")
print(f"Glued Subs: {glued_subs_length}")
