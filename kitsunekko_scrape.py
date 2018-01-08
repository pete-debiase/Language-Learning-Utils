#!/usr/bin/python
"""Scrape list of shows with links for items of interest."""
# Pete Adriano DeBiase
# Created: 2017/12/18

from lxml import html
from bs4 import BeautifulSoup
import requests

base_url = 'http://kitsunekko.net'
with open('shows.txt', 'r', encoding='utf-8') as file:
    shows = [base_url + line.rstrip() for line in file]

subs = {}
for i, show in enumerate(shows):
    if i % 100 == 0:
        print(i)
    page = requests.get(show)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    title = soup.title.text.replace(' - Japanese subtitles - kitsunekko.net', '').strip()
    subs[title] = []
    for link in soup.find_all('a'):
        if link.text not in ('kitsunekko.net', 'Japanese subtitles', title, 'File↑', 'Size', 'Date'):
            subs[title].append(link.text.strip())

scraped_data = []
for show, subtitles in subs.items():
    # scraped_data.append('#' + show + '\n\n' + '\n'.join(subtitles) + '\n\n----------')
    scraped_data.append('#' + show + '\n' + '\n'.join(subtitles))

with open('scraped_data.md', 'w+', encoding='utf-8') as file:
    file.write('\n\n'.join(scraped_data))
