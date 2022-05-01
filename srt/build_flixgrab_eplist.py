#!/usr/bin/env python3
"""Build eplist for flixgrab"""

START = 70148936
NUM_EPS = 26

entries = []
for i in range(1, NUM_EPS + 1):
    entry = f'{i}\thttps://www.netflix.com/watch/{START + i - 1}?trackId=200257859'
    entries.append(entry)

with open(r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Claymore\flixgrab_eplist.txt', 'a+', newline='\n', encoding='utf-8') as f:
    f.write('\n'.join(entries))
