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

def scrape_spanish_misconceptions(url):
    """Scrape misconceptions from Spanish Wikipedia page."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    misconceptions = []
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

    # Spanish Wikipedia uses a special <meta> element to contain the main content
    # Find the meta element that contains the misconceptions
    meta_element = content.find('meta', {'property': 'mw:PageProp/toc'})

    # Use the meta element if found, otherwise fallback to content
    search_area = meta_element if meta_element else content

    # First pass: identify sections from headings
    section_map = {}  # Maps elements to their section
    current_section = ""

    for element in search_area.find_all(['h2', 'h3', 'h4']):
        # Update current section - get text directly from heading
        section_text = element.get_text().strip()
        # Remove [editar] suffix if present
        section_text = section_text.replace('[editar]', '').strip()
        # Skip non-content sections
        skip_sections = ['Véase también', 'Referencias', 'Enlaces externos', 'Notas', 'Contenido', 'Leer más', 'Bibliografía']
        if section_text and section_text not in skip_sections:
            current_section = section_text
            section_map[element] = current_section

    # Second pass: find only top-level ULs (those whose parent is not an LI)
    # and extract their direct children LIs
    for ul in search_area.find_all('ul'):
        # Check if this UL's parent is an LI (which would make it nested)
        if ul.parent and ul.parent.name == 'li':
            continue  # Skip nested lists

        # Find the section for this UL by looking backwards for the nearest heading
        section_for_ul = None
        prev = ul.find_previous(['h2', 'h3', 'h4'])
        if prev:
            section_text = prev.get_text().strip().replace('[editar]', '').strip()
            skip_sections = ['Véase también', 'Referencias', 'Enlaces externos', 'Notas', 'Contenido', 'Leer más', 'Bibliografía']
            if section_text not in skip_sections:
                section_for_ul = section_text

        if not section_for_ul:
            continue

        # Get direct children LIs only (not nested)
        for li in ul.find_all('li', recursive=False):
            # Get the text
            text = clean_text(li.get_text())

            # Skip references, empty, very short entries, or navigation items
            if (len(text) > 30 and
                not text.startswith('Artículo principal:') and
                not text.startswith('^') and
                not text.startswith('Véase también:') and
                not text.startswith('Más información:') and
                'ISBN' not in text[:50]):

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
    url = 'https://es.wikipedia.org/wiki/Anexo:Falsos_mitos'

    print(f"Scraping Spanish misconceptions...")
    misconceptions = scrape_spanish_misconceptions(url)
    print(f"  Found {len(misconceptions)} misconceptions")

    # Add IDs
    for i, misconception in enumerate(misconceptions, 1):
        misconception['id'] = i

    # Reorder fields
    final_data = [
        {
            'id': m['id'],
            'text': m['text'],
            'category': m['category'],
            'source_url': m['source_url']
        }
        for m in misconceptions
    ]

    # Save to JSON
    output_file = '/Users/eliashernandezramon/Documents/MBP14-Documents/Webdev Projects/Common_misconceptions/data/misconceptions_es.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"\nTotal: {len(misconceptions)} Spanish misconceptions saved to {output_file}")

if __name__ == '__main__':
    main()
