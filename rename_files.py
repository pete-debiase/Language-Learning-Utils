#!/usr/bin/python
"""For batch-renaming files."""
# Pete Adriano DeBiase
# Created: 2018/01/10

import os
import re

root = r'C:\Users\pete\ALL\Language\JA\SUBS2SRS\Movies and Shows\Hana Yori Dango\subs_ja'
os.chdir(root)

match_pattern = '.srt'
filenames = [f for f in os.listdir() if match_pattern in f]

find = r'\.srt'
replace = r'_ja.srt'
for f in filenames:
    print(re.sub(find, replace, f))
    os.rename(f, re.sub(find, replace, f))
