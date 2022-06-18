#!/usr/bin/env python3
"""Batch-rename files in a directory (2018/01/10)"""

import os
import re

root = r'C:\~\Languages\JA\SUBS2SRS\Neon Genesis Evangelion\subs_ja\vtt'
os.chdir(root)

match_pattern = '.vtt'
filenames = [f for f in os.listdir() if match_pattern in f]

find = r'Neon\.Genesis\.Evangelion\.(.*?)\.(.*)'
replace = r'Neon Genesis Evangelion_\1_ja.vtt'
for f in filenames:
    print(re.sub(find, replace, f))
    os.rename(f, re.sub(find, replace, f))
