#!/usr/bin/env python3
"""
Generate a picture book for a specific character in a specific visual style.

Usage:
    uv run scripts/gen_book.py <character_id> [--style STYLE] [--message MESSAGE]

Arguments:
    character_id - The character to generate a book for (e.g., cullan, arthur)

Options:
    --style STYLE     - The visual style to use (default: from story/template.yaml)
    --message MESSAGE - Commit message for a new version (required if prompts changed)

Example:
    uv run scripts/gen_book.py cullan
    uv run scripts/gen_book.py cullan --message "Updated story text"
    uv run scripts/gen_book.py arthur --style red_tree

This will:
1. Build all prompts upfront (in memory)
2. Compare prompt hashes against the latest version
3. If prompts changed, require --message to create a new version
4. Save prompt TXT files to out/images/{page_stem}-{hash}.txt
5. Generate images to out/images/{page_stem}-{hash}.jpg (skips if exists)
6. Frame images in-memory and compile into PDF at out/versions/{version}/{character}-book.pdf

Images are stored in a shared out/images/ directory (not per-version).
This allows reusing images across versions when prompts are unchanged.
"""

import sys
import re
import argparse
from pathlib import Path

# Add parent directory to path so we can import from scripts package
sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image
from scripts import gen_image
from scripts import versioning

__all__ = ['generate_book']

STORY_DIR = Path('out/story')


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


def _get_all_pages() -> list[Path]:
    """Get all page files in the story directory."""
    if not STORY_DIR.exists():
        return []
    return sorted(STORY_DIR.glob('p*.yaml'))


def _build_all_prompts(page_files: list[Path], style_id: str) -> dict[str, tuple[str, list[str], list[str], str]]:
    """Build prompts for all pages upfront.

    Args:
        page_files: List of page YAML file paths to process
        style_id: The style identifier (e.g., 'genealogy_witch')

    Returns:
        dict mapping page_stem to tuple of (prompt, ref_images, ref_labels, prompt_hash)
    """
    import yaml

    prompts = {}
    for page_file in page_files:
        with open(page_file) as f:
            page_data = yaml.safe_load(f)
        prompt, ref_images, ref_labels = gen_image.build_prompt(page_data, style_id)
        prompt_hash = versioning.compute_prompt_hash(prompt)
        prompts[page_file.stem] = (prompt, ref_images, ref_labels, prompt_hash)

    return prompts


def _get_hashes_from_prompts(prompts: dict[str, tuple]) -> dict[str, str]:
    """Extract just the hashes from a prompts dict.

    Args:
        prompts: dict from _build_all_prompts()

    Returns:
        dict mapping page_stem to prompt_hash
    """
    return {page_stem: data[3] for page_stem, data in prompts.items()}


def _check_version_needed(current_hashes: dict[str, str], style_id: str, message: str | None) -> int:
    """Check if a new version is needed and return the version to use.

    Logic:
    - If no versions exist, create version 1 (requires --message)
    - If prompts changed since last version, require --message to create new version
    - If prompts unchanged, use existing version

    Args:
        current_hashes: dict mapping page_stem to current prompt_hash
        style_id: The style identifier
        message: User-provided message for new version (None if not provided)

    Returns:
        Version number to use

    Raises:
        SystemExit if prompts changed but no --message provided
    """
    latest_version = versioning.get_latest_version()

    # No versions exist yet
    if latest_version == 0:
        if not message:
            print("No versions exist yet. To create version 01, run:")
            print(f"  gen_book.py <character> --message \"Initial version\"")
            sys.exit(1)
        return versioning.create_new_version(message, style_id)

    # Check if prompts have changed
    manifest = versioning.read_manifest(latest_version)
    if manifest is None:
        # Manifest missing - treat as needing new version
        if not message:
            print(f"Manifest missing for version {latest_version:02d}. To create new version, run:")
            print(f"  gen_book.py <character> --message \"Your description\"")
            sys.exit(1)
        return versioning.create_new_version(message, style_id)

    # Compare current hashes against stored hashes
    stored_hashes = {k: v.get('prompt_hash') for k, v in manifest.get('images', {}).items()}

    # Check if any page's prompt has changed
    prompts_changed = False
    for page_stem, current_hash in current_hashes.items():
        stored_hash = stored_hashes.get(page_stem)
        if stored_hash and stored_hash != current_hash:
            prompts_changed = True
            print(f"Prompt changed for {page_stem}: {stored_hash} -> {current_hash}")

    if prompts_changed:
        if not message:
            new_version = latest_version + 1
            print(f"\nPrompts have changed since v{latest_version:02d}. To create v{new_version:02d}, run:")
            print(f"  gen_book.py <character> --message \"Your description of changes\"")
            sys.exit(1)
        return versioning.create_new_version(message, style_id)

    # Prompts unchanged - use existing version
    print(f"Using existing version {latest_version:02d} (prompts unchanged)")
    return latest_version


def _create_pdf_from_images(image_paths: list[Path], output_path: Path):
    """Create a PDF from raw images, framing them in-memory.

    Args:
        image_paths: Paths to raw (unframed) images
        output_path: Where to save the PDF
    """
    if not image_paths:
        return

    # Frame each image in-memory and collect
    framed_images = []
    for img_path in image_paths:
        framed = gen_image.frame_image_for_pdf(img_path)
        if framed.mode != 'RGB':
            framed = framed.convert('RGB')
        framed_images.append(framed)

    # Save as PDF
    framed_images[0].save(
        output_path,
        save_all=True,
        append_images=framed_images[1:] if len(framed_images) > 1 else [],
        resolution=100.0
    )


def _save_prompts(prompts: dict[str, tuple[str, list[str], list[str], str]]) -> None:
    """Save prompt text files to out/images/ (if they don't exist).

    Args:
        prompts: dict from _build_all_prompts()
    """
    versioning.IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for page_stem, (prompt, _, _, prompt_hash) in prompts.items():
        prompt_path = versioning.get_prompt_path(page_stem, prompt_hash)
        if not prompt_path.exists():
            prompt_path.write_text(prompt)
            print(f"Saved prompt: {prompt_path}")


def generate_book(character_id: str, style_id: str, prompts: dict[str, tuple], version: int) -> Path:
    """Generate a picture book for a specific character in a specific style.

    Args:
        character_id: The character ID (e.g., 'cullan', 'arthur')
        style_id: The style ID (e.g., 'genealogy_witch', 'red_tree')
        prompts: Pre-built prompts from _build_all_prompts()
        version: The version number to generate into

    Returns:
        Path to the generated PDF file
    """
    print(f"Character: {character_id}")
    print(f"Style: {style_id}")
    print(f"Version: {version:02d}")
    print(f"Pages: {len(prompts)}")
    print()

    # Save prompt TXT files (if not already saved)
    print("Saving prompt files...")
    _save_prompts(prompts)
    print()

    # Generate images for each page (skips if hash matches existing)
    generated_images = []

    for i, (page_stem, (prompt, ref_images, ref_labels, prompt_hash)) in enumerate(prompts.items(), 1):
        print(f"[{i}/{len(prompts)}] Processing {page_stem}...")
        image_path = gen_image.generate_image_from_prompt(
            prompt=prompt,
            ref_images=ref_images,
            ref_labels=ref_labels,
            page_stem=page_stem,
            prompt_hash=prompt_hash
        )
        generated_images.append(image_path)

        # Update manifest with image info
        versioning.update_manifest_image(version, page_stem, image_path.name, prompt_hash)
        print()

    # Create PDF in version folder
    version_path = versioning.get_version_path(version)
    version_path.mkdir(parents=True, exist_ok=True)
    pdf_path = version_path / f'{character_id}-book.pdf'

    print("=" * 60)
    print(f"Creating PDF with {len(generated_images)} page(s)...")
    print("Framing images for print...")
    _create_pdf_from_images(generated_images, pdf_path)
    print(f"Saved book to: {pdf_path}")

    # Update manifest with book info
    versioning.update_manifest_book(version, pdf_path.name)

    print()
    print("=" * 60)
    print(f"Generation complete: {len(prompts)}/{len(prompts)} pages succeeded")

    return pdf_path


def main():
    """Main entry point."""
    default_style = gen_image.get_default_style()

    parser = argparse.ArgumentParser(
        description="Generate a picture book for a specific character.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Default style: {default_style}"
    )
    parser.add_argument("character_id", help="The character to generate a book for (e.g., cullan, arthur)")
    parser.add_argument("--style", default=default_style, help=f"The visual style to use (default: {default_style})")
    parser.add_argument("--message", "-m", help="Commit message for a new version (required if prompts changed)")

    args = parser.parse_args()

    character_id = args.character_id
    style_id = args.style
    message = args.message

    # Validate character_id format (lowercase, underscores allowed)
    if not re.match(r'^[a-z_]+$', character_id):
        parser.error(
            f"Invalid character ID '{character_id}'. "
            "Character IDs should be lowercase letters and underscores only"
        )

    # Validate style_id format (lowercase, underscores allowed)
    if not re.match(r'^[a-z_]+$', style_id):
        parser.error(
            f"Invalid style ID '{style_id}'. "
            "Style IDs should be lowercase letters and underscores only"
        )

    # Step 1: Find pages for this character
    page_files = _get_pages_for_character(character_id)
    if not page_files:
        parser.error(f"No pages found for character '{character_id}' in {STORY_DIR}")

    print(f"Found {len(page_files)} page(s) for {character_id}")

    # Step 2: Build all prompts upfront (in memory)
    print("Building prompts...")
    prompts = _build_all_prompts(page_files, style_id)
    current_hashes = _get_hashes_from_prompts(prompts)
    print(f"Built {len(prompts)} prompt(s)")
    print()

    # Step 3: Check version requirements (uses pre-computed hashes)
    version = _check_version_needed(current_hashes, style_id, message)
    print()

    # Step 4: Generate book (saves prompts, generates images, creates PDF)
    generate_book(character_id, style_id, prompts, version)


if __name__ == '__main__':
    main()
