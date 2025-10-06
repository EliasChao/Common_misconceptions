#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import re

def clean_text(text):
    """Clean and normalize text."""
    # Remove citation brackets like [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Strip whitespace
    return text.strip()

def scrape_misconceptions(url, base_category):
    """Scrape misconceptions from a Wikipedia page."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    misconceptions = []
    current_category = base_category
    current_section = ""

    # Find the main content - try different selectors
    content = soup.find('div', {'id': 'mw-content-text'})
    if not content:
        content = soup.find('div', {'class': 'mw-parser-output'})
    if not content:
        content = soup.find('div', {'id': 'bodyContent'})

    if not content:
        print(f"  Warning: Could not find content div for {url}")
        return misconceptions

    # Find only top-level ULs (those whose parent is not an LI)
    # and extract their direct children LIs
    for ul in content.find_all('ul'):
        # Check if this UL's parent is an LI (which would make it nested)
        if ul.parent and ul.parent.name == 'li':
            continue  # Skip nested lists

        # Find the section for this UL by looking backwards for the nearest heading
        section_for_ul = None
        prev = ul.find_previous(['h2', 'h3', 'h4'])
        if prev:
            section_text = prev.get_text().strip().replace('[edit]', '').strip()
            skip_sections = ['See also', 'References', 'External links', 'Notes', 'Contents']
            if section_text not in skip_sections:
                section_for_ul = section_text

        if not section_for_ul:
            continue

        # Get direct children LIs only (not nested)
        for li in ul.find_all('li', recursive=False):
            # Skip if this is inside a references section
            if li.find_parent(class_='reflist'):
                continue

            # Get the text
            text = clean_text(li.get_text())

            # Skip references, empty, very short entries, or navigation items
            if (len(text) > 20 and
                not text.startswith('Main article:') and
                not text.startswith('^') and
                not text.startswith('See also:') and
                not text.startswith('Further information:')):

                # Create section anchor
                section_anchor = section_for_ul.replace(' ', '_')
                source_url = f"{url}#{section_anchor}"

                misconceptions.append({
                    'text': text,
                    'category': section_for_ul,
                    'source_url': source_url
                })

    return misconceptions

def main():
    # URLs to scrape
    urls = [
        ('https://en.wikipedia.org/wiki/List_of_common_misconceptions_about_arts_and_culture', 'Arts and Culture'),
        ('https://en.wikipedia.org/wiki/List_of_common_misconceptions_about_history', 'History'),
        ('https://en.wikipedia.org/wiki/List_of_common_misconceptions_about_science,_technology,_and_mathematics', 'Science, Technology, and Mathematics')
    ]

    all_misconceptions = []

    for url, category in urls:
        print(f"Scraping {category}...")
        misconceptions = scrape_misconceptions(url, category)
        print(f"  Found {len(misconceptions)} misconceptions")
        all_misconceptions.extend(misconceptions)

    # Add IDs
    for i, misconception in enumerate(all_misconceptions, 1):
        misconception['id'] = i

    # Reorder fields
    final_data = [
        {
            'id': m['id'],
            'text': m['text'],
            'category': m['category'],
            'source_url': m['source_url']
        }
        for m in all_misconceptions
    ]

    # Save to JSON
    output_file = '/Users/eliashernandezramon/Documents/MBP14-Documents/Webdev Projects/Common_misconceptions/data/misconceptions_en.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"\nTotal: {len(all_misconceptions)} English misconceptions saved to {output_file}")

if __name__ == '__main__':
    main()
