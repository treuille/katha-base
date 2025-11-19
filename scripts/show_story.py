#!/usr/bin/env python3
"""
Show the full story for a character given their two-letter code.

NEW STRUCTURE (Post-Refactor):
- Each spread has 2 pages (24 pages total)
- Each page has 2 images
- File naming: {char}-{spread}-{page}.yaml
- Displays node types and metadata

Usage:
    python3 scripts/show_story.py <character-code>

Example:
    python3 scripts/show_story.py cu
"""

import sys
import yaml
from pathlib import Path


def get_other_characters(page_id, main_char_code):
    """Extract other character codes from a page ID."""
    # Split by hyphens and filter out numbers and the main character code
    parts = page_id.split('-')
    chars = [p for p in parts if len(p) == 2 and p.isalpha() and p != main_char_code]
    return chars


def load_character(char_code):
    """Load character data from the YAML file."""
    char_file = Path('characters') / f'{char_code}-*.yaml'
    matches = list(Path('characters').glob(f'{char_code}-*.yaml'))

    if not matches:
        print(f"Error: No character file found for code '{char_code}'")
        sys.exit(1)

    with open(matches[0], 'r') as f:
        return yaml.safe_load(f)


def load_page(page_filename):
    """Load page data from the YAML file."""
    page_path = Path('pages') / page_filename

    if not page_path.exists():
        print(f"Warning: Page file not found: {page_filename}")
        return None

    with open(page_path, 'r') as f:
        return yaml.safe_load(f)


def show_page(page_filename, char_code, level=3):
    """Display a single page with the specified heading level.

    Supports both old and new page structures.
    """
    page_data = load_page(page_filename)
    if not page_data:
        return None

    # Extract page ID (filename without .yaml)
    page_id = page_filename.replace('.yaml', '')

    # Check if this is a joint page
    other_chars = get_other_characters(page_id, char_code)
    joint_note = f" (joint with {', '.join(other_chars).upper()})" if other_chars else ""

    # Determine heading symbols based on level
    page_heading = '#' * level
    content_heading = '#' * (level + 1)
    image_heading = '#' * (level + 2)

    # Display page information
    print(f"{page_heading} Page {page_filename}{joint_note}\n")

    # Node type (new structure)
    node_type = page_data.get('node_type', None)
    if node_type:
        node_emoji = {
            'solo': '👤',
            'meeting': '🤝',
            'mirrored': '🪞',
            'resonant': '✨'
        }
        emoji = node_emoji.get(node_type, '')
        print(f"**Node Type:** {emoji} {node_type.capitalize()}\n")

    # Description
    description = page_data.get('description', 'No description available')
    print(f"{content_heading} Description\n")
    print(f"{description}\n")

    # Check for new or old structure
    if 'images' in page_data:
        # New structure: multiple images
        images = page_data['images']
        print(f"{content_heading} Images ({len(images)} total)\n")

        for i, img_data in enumerate(images, 1):
            print(f"{image_heading} Image {i}\n")

            # Visual
            visual = img_data.get('visual', 'No visual description available')
            print(f"**Visual:**\n")
            if isinstance(visual, str):
                print(f"{visual.strip()}\n")
            else:
                print(f"{visual}\n")

            # Text
            text = img_data.get('text', 'No text available')
            print(f"**Text:**\n")
            if isinstance(text, str):
                print(f"{text.strip()}\n")
            else:
                print(f"{text}\n")
    else:
        # Old structure: single visual/text fields
        print(f"{content_heading} Visual\n")
        visual = page_data.get('visual', 'No visual description available')
        if isinstance(visual, str):
            print(f"{visual.strip()}\n")
        else:
            print(f"{visual}\n")

        print(f"{content_heading} Text\n")
        text = page_data.get('text', 'No text available')
        if isinstance(text, str):
            print(f"{text.strip()}\n")
        else:
            print(f"{text}\n")

    # Show node-specific metadata if present
    if node_type == 'meeting' and 'meeting_data' in page_data:
        print(f"{content_heading} Meeting Data\n")
        meeting_data = page_data['meeting_data']
        print(f"**Location:** {meeting_data.get('location', 'N/A')}\n")
        print(f"**Shared Action:** {meeting_data.get('shared_action', 'N/A')}\n")

    if node_type == 'mirrored' and 'mirrored_data' in page_data:
        print(f"{content_heading} Mirrored Data\n")
        mirrored_data = page_data['mirrored_data']
        print(f"**Shared Theme:** {mirrored_data.get('shared_theme', 'N/A')}\n")
        print(f"**Symbolic Motif:** {mirrored_data.get('symbolic_motif', 'N/A')}\n")

    if node_type == 'resonant' and 'resonant_data' in page_data:
        print(f"{content_heading} Resonant Data\n")
        resonant_data = page_data['resonant_data']
        print(f"**Ripple Effect:** {resonant_data.get('ripple_effect', 'N/A')}\n")

    return other_chars


def get_surrounding_pages(page_filename, other_char_code):
    """Get the preceding and succeeding pages from another character's story."""
    other_char_data = load_character(other_char_code)
    other_pages = other_char_data.get('story', [])

    try:
        idx = other_pages.index(page_filename)
        preceding = other_pages[idx - 1] if idx > 0 else None
        succeeding = other_pages[idx + 1] if idx < len(other_pages) - 1 else None
        return preceding, succeeding
    except ValueError:
        # Page not found in other character's story
        return None, None


def show_story(char_code):
    """Display the full story for a character."""
    # Load character data
    char_data = load_character(char_code)
    char_name = char_data['attributes']['name']
    pages = char_data.get('story', [])

    print(f"# {char_name}'s Story\n")
    print(f"## Story\n")

    # Track overlapping pages
    overlaps = []

    for page_filename in pages:
        other_chars = show_page(page_filename, char_code, level=3)
        if other_chars:
            overlaps.append((page_filename, other_chars))

    # Show overlaps section
    if overlaps:
        print(f"## Overlaps\n")
        for page_filename, other_chars in overlaps:
            for other_char_code in other_chars:
                # Get surrounding pages from the other character's story
                preceding, succeeding = get_surrounding_pages(page_filename, other_char_code)

                other_char_data = load_character(other_char_code)
                other_char_name = other_char_data['attributes']['name']

                print(f"### Overlap with {other_char_name} ({other_char_code.upper()})\n")

                # Show preceding page
                if preceding:
                    print(f"#### Before (from {other_char_name}'s story)\n")
                    show_page(preceding, other_char_code, level=5)

                # Show the overlap page
                print(f"#### Overlap page\n")
                show_page(page_filename, char_code, level=5)

                # Show succeeding page
                if succeeding:
                    print(f"#### After (from {other_char_name}'s story)\n")
                    show_page(succeeding, other_char_code, level=5)


def main():
    if len(sys.argv) != 2:
        print("Usage: python show_story.py <character-code>")
        print("Example: python show_story.py cu")
        sys.exit(1)

    char_code = sys.argv[1].lower()

    if len(char_code) != 2:
        print("Error: Character code must be exactly 2 characters")
        sys.exit(1)

    show_story(char_code)


if __name__ == '__main__':
    main()
