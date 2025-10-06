#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions_about_arts_and_culture'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Try different content selectors
content = soup.find('div', {'class': 'mw-parser-output'})

if content:
    print("Found content div")

    # Find first few headings and list items
    headings = content.find_all(['h2', 'h3'], limit=10)
    print(f"\nFound {len(headings)} headings")
    for h in headings:
        print(f"  Tag: {h.name}, Text: {h.get_text()[:50]}")
        span = h.find('span')
        if span:
            print(f"    Span: {span.get('id')}, {span.get_text()}")

    # Check for sections with class
    sections = content.find_all(class_='mw-heading')
    print(f"\nFound {len(sections)} mw-heading sections")
    for s in sections[:5]:
        print(f"  - {s.get_text()[:50]}")

    # Find first few list items
    list_items = content.find_all('li', limit=10)
    print(f"\nFirst {len(list_items)} list items:")
    for li in list_items[:3]:
        text = li.get_text()[:100]
        print(f"  - {text}...")
else:
    print("Could not find content")
