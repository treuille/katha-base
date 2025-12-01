#!/usr/bin/env python3
"""
Generate a picture book for a specific character.

Usage:
    uv run scripts/gen_book.py <character_id>

Arguments:
    character_id - The character to generate a book for (e.g., cullan, arthur)

Example:
    uv run scripts/gen_book.py cullan
    uv run scripts/gen_book.py arthur

This will:
1. Find all pages featuring the character
2. Generate images for each page
3. Compile images into a PDF at out/books/{character}-{version}.pdf
"""

import sys
import re
from pathlib import Path

# Add parent directory to path so we can import from scripts package
sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image
from scripts import gen_image

__all__ = ['generate_book']

STORY_DIR = Path('out/story')
IMAGES_DIR = Path('out/images')
BOOKS_DIR = Path('out/books')


def _get_pages_for_character(character_id: str) -> list[Path]:
    """Find all page files that feature the given character.

    Page filenames follow the pattern: p{number}-{char1}-{char2}-{...}.yaml
    """
    if not STORY_DIR.exists():
        return []

    pages = []
    for page_file in sorted(STORY_DIR.glob('p*.yaml')):
        # Extract character list from filename (everything after p##-)
        stem = page_file.stem  # e.g., "p09-arthur-cullan"
        match = re.match(r'p\d+-(.+)$', stem)
        if match:
            chars_part = match.group(1)  # e.g., "arthur-cullan"
            characters = chars_part.split('-')
            if character_id in characters:
                pages.append(page_file)

    return pages


def _get_next_book_version(character_id: str) -> int:
    """Get the next version number for a character's book."""
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)

    existing = list(BOOKS_DIR.glob(f'{character_id}-*.pdf'))
    if not existing:
        return 1

    # Extract version numbers and find the max
    max_version = 0
    for book_path in existing:
        match = re.match(rf'{character_id}-(\d+)\.pdf$', book_path.name)
        if match:
            version = int(match.group(1))
            max_version = max(max_version, version)

    return max_version + 1


def _create_pdf(image_paths: list[Path], output_path: Path):
    """Create a PDF from a list of images."""
    if not image_paths:
        return

    # Load all images and convert to RGB (required for PDF)
    images = []
    for img_path in image_paths:
        img = Image.open(img_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)

    # Save as PDF
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:] if len(images) > 1 else [],
        resolution=100.0
    )


def generate_book(character_id: str) -> Path:
    """Generate a picture book for a specific character.

    Args:
        character_id: The character ID (e.g., 'cullan', 'arthur')

    Returns:
        Path to the generated PDF file
    """
    # Find pages for this character
    page_files = _get_pages_for_character(character_id)

    if not page_files:
        raise ValueError(f"No pages found for character '{character_id}' in {STORY_DIR}")

    print(f"Found {len(page_files)} page(s) for {character_id}")
    print()

    # Generate images for each page
    generated_images = []

    for i, page_file in enumerate(page_files, 1):
        print(f"[{i}/{len(page_files)}] Processing {page_file.name}...")
        image_path = gen_image.generate_image(str(page_file))
        generated_images.append(image_path)
        print()

    # Create PDF
    version = _get_next_book_version(character_id)
    pdf_path = BOOKS_DIR / f'{character_id}-{version:02d}.pdf'

    print("=" * 60)
    print(f"Creating PDF with {len(generated_images)} page(s)...")
    _create_pdf(generated_images, pdf_path)
    print(f"Saved book to: {pdf_path}")

    print()
    print("=" * 60)
    print(f"Generation complete: {len(page_files)}/{len(page_files)} pages succeeded")

    return pdf_path


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    character_id = sys.argv[1]

    # Validate character_id format (lowercase, underscores allowed)
    if not re.match(r'^[a-z_]+$', character_id):
        print(f"Error: Invalid character ID '{character_id}'")
        print("Character IDs should be lowercase letters and underscores only")
        sys.exit(1)

    generate_book(character_id)


if __name__ == '__main__':
    main()
