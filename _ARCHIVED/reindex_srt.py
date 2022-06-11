#!/usr/bin/python
"""Reindex SRT files."""
# Pete Adriano DeBiase
# Created: 2018/01/14

import os
import subs

root_path = r'C:\Users\Pete\ALL\Japanese\SUBS2SRS\Movies and Shows\Code Geass\Code Geass Lelouch Of The Rebellion R2\JP Subs'
match_pattern = 'Code_Geass'
os.chdir(root_path)
filenames = os.listdir()
filenames = [filename for filename in filenames if match_pattern in filename]

for filename in filenames:
    with open(filename, 'r', encoding='utf-8') as file:
        subs = file.read()
    subs = list(subs.parse(subs))

    output_path = root_path + '\\' + 'reindexed\\' + filename
    with open(output_path, 'w+', encoding='utf-8') as file:
        file.write(subs.compose(subs))
