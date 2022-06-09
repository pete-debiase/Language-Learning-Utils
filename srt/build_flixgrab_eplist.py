#!/usr/bin/env python3
"""Build eplist for flixgrab"""

START = 80204507
NUM_EPS = 13

entries = []
for i in range(1, NUM_EPS + 1):
    entry = f'{i}\thttps://www.netflix.com/watch/{START + i - 1}?trackId=200257859'
    entries.append(entry)

with open(r'C:\~\Languages\JA\SUBS2SRS\Violet Evergarden\flixgrab_eplist.txt', 'a+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(entries))
