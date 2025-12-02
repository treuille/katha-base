#!/usr/bin/env python3
"""
Print all story text for a character in markdown format.

Usage:
    uv run scripts/print_text.py <character_id>

Examples:
    uv run scripts/print_text.py arthur
    uv run scripts/print_text.py arthur | bat -l md
    uv run scripts/print_text.py hansel | bat --style=plain -l md
"""

import sys
import yaml
from pathlib import Path


def get_story_dir() -> Path:
    return Path(__file__).parent.parent / "out" / "story"


def get_page_number(page_id: str) -> int:
    """Extract numeric page number from id like 'p03'."""
    return int(page_id.lstrip("p"))


def print_character_text(character_id: str) -> None:
    """Print all text for a character in markdown format."""
    story_dir = get_story_dir()

    # Find all yaml files containing this character
    pages = []
    for yaml_file in story_dir.glob("*.yaml"):
        # Check if character is in filename
        if character_id not in yaml_file.stem:
            continue

        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        # Verify character is actually in the characters list
        characters = data.get("characters", [])
        if character_id not in characters:
            continue

        page_id = data.get("id", "")
        text = data.get("text", "").strip()

        if text:
            pages.append((get_page_number(page_id), page_id, text))

    if not pages:
        print(f"No text found for character: {character_id}", file=sys.stderr)
        sys.exit(1)

    # Sort by page number
    pages.sort(key=lambda x: x[0])

    # Output markdown
    print(f"# {character_id.title()}'s Story\n")

    for page_num, page_id, text in pages:
        print(f"### Page {page_num}\n")
        print(text)
        print()


def main():
    if len(sys.argv) != 2:
        print("Usage: uv run scripts/print_text.py <character_id>", file=sys.stderr)
        print("\nAvailable characters: arthur, cullan, emer, hansel, henry, james", file=sys.stderr)
        sys.exit(1)

    character_id = sys.argv[1].lower()
    print_character_text(character_id)


if __name__ == "__main__":
    main()
