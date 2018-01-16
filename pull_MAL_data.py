#!/usr/bin/python
"""Pulls information about shows from myanimelist.net."""
# Pete Adriano DeBiase
# Created: 2018/01/16

from lxml import html
import random
import re
from string import punctuation
import time
from bs4 import BeautifulSoup
import requests

def sanitize(s):
    sanitized = s.replace('(TV)', '')
    sanitized = ''.join(c for c in s if c not in punctuation).lower()
    sanitized = sanitized.replace(' ', '')
    return sanitized

with open('shows_for_MAL_pull.txt', 'r', encoding='utf-8') as file:
    shows = [line.rstrip() for line in file]

with open('scraped_MAL_data.txt', 'r', encoding='utf-8') as file:
    already_scraped_shows = [line.rstrip() for line in file]
    already_scraped_show_titles = [_.split('\t')[0] for _ in already_scraped_shows]

shows = [show for show in shows if show not in already_scraped_show_titles]
print(len(shows))
base_url = 'https://myanimelist.net/search/all?q='
show_queries = [base_url + show for show in shows]

use_show = 'null'
for i, (show, query) in enumerate(zip(shows, show_queries)):
    try:
        print(i, show)
        time.sleep(random.randint(1, 5))
        page = requests.get(query)
        page_content = page.content
        soup = BeautifulSoup(page_content, 'html.parser')
        links = soup.find_all('div', class_="information")
        for link in links:
            show_name = link.a.string
            show_type = link.div.a.string
            if sanitize(show_name) == sanitize(show) and show_type in ('TV', 'OVA'):
                show_details = ''.join([str(item) for item in link.div.contents])
                number_episodes = re.findall(r'\((\d+) eps\)', show_details)[0]
                show_score = re.findall(r'Scored (.*)<br/>', show_details)[0]
                already_scraped_shows.append('\t'.join([show, show_score, number_episodes]))
                break
            elif show_type in ('TV', 'OVA'):
                show_details = ''.join([str(item) for item in link.div.contents])
                number_episodes = re.findall(r'\((\d+) eps\)', show_details)[0]
                show_score = re.findall(r'Scored (.*)<br/>', show_details)[0]
                print(f'{show} | {show_name} | {show_type} | {number_episodes} | {show_score}')
                use_show = input("Use this show? ")
                if use_show == 'Y':
                    already_scraped_shows.append('\t'.join([show, show_score, number_episodes]))
                    break
                elif use_show == 'skip':
                    already_scraped_shows.append('\t'.join([show, "PERFORM_MANUAL_SEARCH"]))
                    break
                elif use_show == 'quit':
                    break
                else:
                    continue
    except:
        already_scraped_shows.append('\t'.join([show, "PERFORM_MANUAL_SEARCH"]))
    if use_show == 'quit':
            break

with open('scraped_MAL_data.txt', 'w+', encoding='utf-8') as file:
    file.write('\n'.join(already_scraped_shows))
