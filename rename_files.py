#!/usr/bin/python
"""For batch-renaming files."""
# Pete Adriano DeBiase
# Created: 2018/01/10

import os
import re

root_path = r'C:\Users\Pete\ALL-P70\Japanese\SUBS2SRS\Movies and Shows\Code Geass\Code Geass Lelouch Of The Rebellion\JP Subs'
os.chdir(root_path)

filenames = os.listdir()
find = r'\[Coalgirls\]_(.*)_\((.*)\.srt'
replace = r'\1.srt'

for filename in filenames:
    os.rename(filename, re.sub(find, replace, filename))
