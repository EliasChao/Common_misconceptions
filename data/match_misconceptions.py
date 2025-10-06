#!/usr/bin/env python3
"""
Match English and Spanish misconceptions to use the same IDs.
This script uses fuzzy matching to find similar misconceptions across languages.
"""
import json
from difflib import SequenceMatcher

def similarity(text1, text2):
    """Calculate similarity between two texts (0-1)."""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def normalize_for_matching(text):
    """Normalize text for better matching."""
    # Remove common words and punctuation for better matching
    text = text.lower()
    # Keep only first 200 chars for comparison (to avoid long explanations)
    return text[:200]

def extract_keywords(text):
    """Extract key identifiable terms from text."""
    # Convert to lowercase for matching
    text_lower = text.lower()
    keywords = []

    # Look for recognizable entities and concepts (with Spanish variants)
    entities = [
        ('einstein', 'einstein'),
        ('napoleon', 'napoleón'),
        ('viking', 'vikingo'),
        ('caesar', 'césar'),
        ('columbus', 'colón'),
        ('galileo', 'galileo'),
        ('coca-cola', 'coca-cola'),
        ('pepsi', 'pepsi'),
        ('adidas', 'adidas'),
        ('netflix', 'netflix'),
        ('chevrolet', 'chevrolet'),
        ('ar-15', 'ar-15'),
        ('bermuda', 'bermudas'),
        ('everest', 'everest'),
        ('sahara', 'sáhara'),
        ('great wall', 'gran muralla'),
        ('mozart', 'mozart'),
        ('beethoven', 'beethoven'),
        ('shakespeare', 'shakespeare'),
        ('hemingway', 'hemingway'),
        ('vitamin', 'vitamina'),
        ('sugar', 'azúcar'),
        ('caffeine', 'cafeína'),
        ('alcohol', 'alcohol'),
        ('chocolate', 'chocolate'),
        ('dinosaur', 'dinosaurio'),
        ('evolution', 'evolución'),
        ('black hole', 'agujero negro'),
        ('gravity', 'gravedad'),
        ('goldfish', 'pez dorado'),
        ('chameleon', 'camaleon'),
        ('bat', 'murciélago'),
        ('shark', 'tiburón'),
        ('penguin', 'pingüino'),
        ('ostrich', 'avestruz'),
        ('venus', 'venus'),
        ('mars', 'marte'),
        ('moon', 'luna'),
        ('santa claus', 'papá noel'),
        ('nova', 'nova'),
    ]

    found_keywords = set()
    for en, es in entities:
        if en in text_lower or es in text_lower:
            found_keywords.add(en)  # Use English as canonical form

    return list(found_keywords)

def find_matches(en_data, es_data):
    """Find matching misconceptions between English and Spanish."""
    matches = {}  # Maps en_index -> es_index
    used_es = set()  # Track which Spanish items have been matched

    # First pass: match by shared keywords + text similarity (high confidence)
    for en_idx, en_item in enumerate(en_data):
        en_keywords = extract_keywords(en_item['text'])
        if not en_keywords:
            continue

        best_match_idx = None
        best_score = 0.0

        for es_idx, es_item in enumerate(es_data):
            if es_idx in used_es:
                continue

            es_keywords = extract_keywords(es_item['text'])
            if not es_keywords:
                continue

            # Check for keyword overlap
            common_keywords = set(en_keywords) & set(es_keywords)
            if not common_keywords:
                continue

            # Calculate text similarity as well
            en_text = normalize_for_matching(en_item['text'])
            es_text = normalize_for_matching(es_item['text'])
            text_sim = similarity(en_text, es_text)

            # Score based on keyword overlap and text similarity
            keyword_score = len(common_keywords) / max(len(en_keywords), len(es_keywords))
            combined_score = keyword_score * 0.5 + text_sim * 0.5

            if combined_score > best_score:
                best_score = combined_score
                best_match_idx = es_idx

        # Accept match if score is high enough
        if best_match_idx is not None and best_score > 0.4:
            matches[en_idx] = best_match_idx
            used_es.add(best_match_idx)

    # Second pass: match by text similarity for remaining items
    for en_idx, en_item in enumerate(en_data):
        if en_idx in matches:
            continue

        en_text = normalize_for_matching(en_item['text'])
        best_match_idx = None
        best_score = 0.0

        for es_idx, es_item in enumerate(es_data):
            if es_idx in used_es:
                continue

            es_text = normalize_for_matching(es_item['text'])

            # Calculate similarity
            text_sim = similarity(en_text, es_text)

            if text_sim > best_score:
                best_score = text_sim
                best_match_idx = es_idx

        # Only accept very high similarity matches
        if best_match_idx is not None and best_score > 0.6:
            matches[en_idx] = best_match_idx
            used_es.add(best_match_idx)

    return matches

def main():
    # Load data
    with open('misconceptions_en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    with open('misconceptions_es.json', 'r', encoding='utf-8') as f:
        es_data = json.load(f)

    print(f"English misconceptions: {len(en_data)}")
    print(f"Spanish misconceptions: {len(es_data)}")

    # Find matches
    print("\nMatching misconceptions...")
    matches = find_matches(en_data, es_data)
    print(f"Found {len(matches)} matches")

    # Assign IDs
    # Start with English as the base, assign sequential IDs
    # For matched Spanish items, use the same ID as English
    # For unmatched items, assign new IDs after the English ones

    next_id = 1

    # First, assign IDs to English items
    for en_item in en_data:
        en_item['id'] = next_id
        next_id += 1

    # Create a reverse match map (es_idx -> en_idx)
    es_to_en = {es_idx: en_idx for en_idx, es_idx in matches.items()}

    # Assign IDs to Spanish items
    for es_idx, es_item in enumerate(es_data):
        if es_idx in es_to_en:
            # This Spanish item matches an English item, use the same ID
            en_idx = es_to_en[es_idx]
            es_item['id'] = en_data[en_idx]['id']
        else:
            # This is a Spanish-only item, assign a new ID
            es_item['id'] = next_id
            next_id += 1

    # Sort both by ID
    en_data_sorted = sorted(en_data, key=lambda x: x['id'])
    es_data_sorted = sorted(es_data, key=lambda x: x['id'])

    # Save updated files
    with open('misconceptions_en.json', 'w', encoding='utf-8') as f:
        json.dump(en_data_sorted, f, ensure_ascii=False, indent=2)

    with open('misconceptions_es.json', 'w', encoding='utf-8') as f:
        json.dump(es_data_sorted, f, ensure_ascii=False, indent=2)

    print(f"\nUpdated files saved!")
    print(f"Total unique IDs: {next_id - 1}")
    print(f"Shared IDs (matched): {len(matches)}")
    print(f"English-only IDs: {len(en_data) - len(matches)}")
    print(f"Spanish-only IDs: {len(es_data) - len(matches)}")

    # Show some examples of matches
    print("\nExample matches:")
    for i, (en_idx, es_idx) in enumerate(list(matches.items())[:5]):
        en = en_data[en_idx]
        es = es_data_sorted[es_idx]
        print(f"\nID {en['id']}:")
        print(f"  EN ({en['category']}): {en['text'][:80]}...")
        print(f"  ES ({es['category']}): {es['text'][:80]}...")

if __name__ == '__main__':
    main()
