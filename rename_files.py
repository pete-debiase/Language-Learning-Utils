#!/usr/bin/env python3
"""Batch-rename files in a directory (2018/01/10)"""

import os
import re

root = r'C:\Users\pete\ALL\Languages\JA\SUBS2SRS\Claymore\mp4'
os.chdir(root)

match_pattern = '.mp4'
filenames = [f for f in os.listdir() if match_pattern in f]

find = r'\[(.*?)\.(.*?)\](.*).mp4'
replace = r'Claymore_\1\2.mp4'
for f in filenames:
    print(re.sub(find, replace, f))
    os.rename(f, re.sub(find, replace, f))
