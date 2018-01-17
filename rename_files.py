#!/usr/bin/python
"""For batch-renaming files."""
# Pete Adriano DeBiase
# Created: 2018/01/10

import os
import re

root_path = r'C:\Users\Pete\ALL-P70\Japanese\SUBS2SRS\Movies and Shows\FLCL\JP Subs'
match_pattern = 'FLCL'
os.chdir(root_path)
filenames = os.listdir()
filenames = [filename for filename in filenames if match_pattern in filename]

find = r'FLCL_(.*)\.srt'
replace = r'FLCL_\1_JP.srt'

for filename in filenames:
    os.rename(filename, re.sub(find, replace, filename))
