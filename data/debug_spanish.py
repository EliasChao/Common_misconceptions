#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'https://es.wikipedia.org/wiki/Anexo:Falsos_mitos'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

content = soup.find('div', {'class': 'mw-parser-output'})

if content:
    # Check the meta element
    meta = content.find('meta', {'property': 'mw:PageProp/toc'})
    if meta:
        # Find all lis in meta
        all_lis_in_meta = meta.find_all('li')
        print(f"Total LIs in meta: {len(all_lis_in_meta)}")

        # Find only direct children (UL > LI, not nested in another LI)
        direct_lis = []
        for ul in meta.find_all('ul'):
            # Check if this UL's parent is LI (nested) or something else (direct)
            if ul.parent and ul.parent.name != 'li':
                # This is a top-level UL
                for li in ul.find_all('li', recursive=False):
                    direct_lis.append(li)

        print(f"Direct top-level LIs: {len(direct_lis)}")

        # Sample some direct LIs
        print("\nFirst 5 direct LIs:")
        for i, li in enumerate(direct_lis[:5]):
            print(f"{i+1}. {li.get_text()[:80]}...")
