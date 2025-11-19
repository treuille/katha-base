#!/usr/bin/env python3
"""
Validation script to check structural integrity of the repository.

NEW STRUCTURE (Post-Refactor):
- Each spread has 2 pages (24 pages total per character)
- Each page has 2 images
- File naming: {char}-{spread}-{page}.yaml (e.g., cu-01-1.yaml)
- Node types: solo, meeting, mirrored, resonant

Checks:
- Pages are well formatted
- All referenced pages exist
- No overlaps on spreads 1, 11, and 12 (these must be character-specific)
- Pages end in .yaml extension
- Pages don't have the pages/ subdirectory prefix
- No missing/stray pages in the pages directory
- At least one character exists
- All YAML files are valid
- Page structure validation (node types, images, etc.)
- Node type metadata validation

Exit codes:
- 0: All tests passed
- 1: One or more tests failed
"""

import sys
import yaml
from pathlib import Path
from collections import defaultdict

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def error(message):
    """Print error message in red."""
    print(f"{RED}✗ ERROR: {message}{RESET}")

def warning(message):
    """Print warning message in yellow."""
    print(f"{YELLOW}⚠ WARNING: {message}{RESET}")

def success(message):
    """Print success message in green."""
    print(f"{GREEN}✓ {message}{RESET}")

def info(message):
    """Print info message."""
    print(f"  {message}")


def load_all_characters():
    """Load all character files."""
    characters_dir = Path('characters')
    if not characters_dir.exists():
        error("Characters directory not found")
        sys.exit(1)

    char_files = list(characters_dir.glob('*.yaml'))
    # Filter out template files
    char_files = [f for f in char_files if 'template' not in f.name and 'example' not in f.name]

    if not char_files:
        error("No character files found in characters directory")
        sys.exit(1)

    characters = {}
    for char_file in char_files:
        try:
            with open(char_file, 'r') as f:
                char_data = yaml.safe_load(f)
                char_id = char_data.get('id')
                if char_id:
                    characters[char_id] = {
                        'file': char_file,
                        'data': char_data,
                        'name': char_data.get('attributes', {}).get('name', 'Unknown')
                    }
        except Exception as e:
            error(f"Failed to load character file {char_file}: {e}")
            sys.exit(1)

    return characters


def test_at_least_one_character(characters):
    """Test that at least one character exists."""
    if len(characters) == 0:
        error("No characters found")
        return False
    success(f"Found {len(characters)} character(s)")
    return True


def test_page_formatting(characters):
    """Test that all page references are properly formatted."""
    errors_found = False

    for char_id, char_info in characters.items():
        pages = char_info['data'].get('story', [])
        char_name = char_info['name']

        for page in pages:
            # Check for pages/ prefix
            if page.startswith('pages/'):
                error(f"{char_name} ({char_id}): Page '{page}' includes 'pages/' prefix - should be just filename")
                errors_found = True

            # Check for .yaml extension
            if not page.endswith('.yaml'):
                error(f"{char_name} ({char_id}): Page '{page}' missing '.yaml' extension")
                errors_found = True

            # Check for path separators
            if '/' in page or '\\' in page:
                error(f"{char_name} ({char_id}): Page '{page}' contains path separator - should be just filename")
                errors_found = True

    if not errors_found:
        success("All page references are properly formatted")
    return not errors_found


def test_pages_exist(characters):
    """Test that all referenced pages exist."""
    errors_found = False
    pages_dir = Path('pages')

    if not pages_dir.exists():
        error("Pages directory not found")
        return False

    for char_id, char_info in characters.items():
        pages = char_info['data'].get('story', [])
        char_name = char_info['name']

        for page in pages:
            page_path = pages_dir / page
            if not page_path.exists():
                error(f"{char_name} ({char_id}): Referenced page '{page}' does not exist")
                errors_found = True

    if not errors_found:
        success("All referenced pages exist")
    return not errors_found


def test_no_overlaps_on_required_solo_spreads(characters):
    """Test that spreads 1, 11, and 12 have no overlaps (are character-specific)."""
    errors_found = False
    required_solo_spreads = [1, 11, 12]

    for char_id, char_info in characters.items():
        pages = char_info['data'].get('story', [])
        char_name = char_info['name']

        for page in pages:
            # Extract page ID (filename without .yaml)
            page_id = page.replace('.yaml', '')

            # Parse new format: {char}-{spread}-{page}.yaml or {char1}-{char2}-{spread}-{page}.yaml
            parts = page_id.split('-')

            # Check if page contains multiple character codes
            char_codes = [p for p in parts if len(p) == 2 and p.isalpha()]

            # Extract spread number (should be second-to-last or third-to-last part)
            spread_num = None
            if len(parts) >= 3:
                try:
                    # Try second-to-last position (for single char: cu-01-1)
                    spread_num = int(parts[-2])
                except ValueError:
                    # Try third-to-last position (for multi char: cu-ma-01-1)
                    if len(parts) >= 4:
                        try:
                            spread_num = int(parts[-2])
                        except ValueError:
                            pass

            if spread_num in required_solo_spreads and len(char_codes) > 1:
                error(f"{char_name} ({char_id}): Spread {spread_num} ('{page}') is a joint page with {char_codes} - spreads 1, 11, 12 must be character-specific")
                errors_found = True

    if not errors_found:
        success("Spreads 1, 11, and 12 are all character-specific (no overlaps)")
    return not errors_found


def test_no_stray_pages(characters):
    """Test that all pages in the pages directory are referenced by at least one character."""
    pages_dir = Path('pages')

    if not pages_dir.exists():
        error("Pages directory not found")
        return False

    # Collect all referenced pages
    referenced_pages = set()
    for char_id, char_info in characters.items():
        pages = char_info['data'].get('story', [])
        referenced_pages.update(pages)

    # Get all actual page files
    all_page_files = set(p.name for p in pages_dir.glob('*.yaml'))

    # Find stray pages
    stray_pages = all_page_files - referenced_pages

    if stray_pages:
        error(f"Found {len(stray_pages)} stray page(s) not referenced by any character:")
        for page in sorted(stray_pages):
            info(f"  - {page}")
        return False

    success("No stray pages found - all pages are referenced")
    return True


def test_missing_pages(characters):
    """Test for any missing pages in character stories (e.g., gaps in numbering)."""
    warnings_found = False

    for char_id, char_info in characters.items():
        pages = char_info['data'].get('story', [])
        char_name = char_info['name']

        # Expected: 24 pages (12 spreads × 2 pages per spread)
        if len(pages) != 24:
            warning(f"{char_name} ({char_id}): Has {len(pages)} pages, expected 24 (12 spreads × 2 pages)")
            warnings_found = True

        # Check for sequential spread-page numbering
        # Expected pattern: spread 1-12, page 1-2 for each spread
        expected_pages = []
        for spread in range(1, 13):
            for page in range(1, 3):
                expected_pages.append((spread, page))

        # Extract actual spread-page numbers
        actual_pages = []
        for page in pages:
            page_id = page.replace('.yaml', '')
            parts = page_id.split('-')

            # Try to extract spread and page numbers
            try:
                # For format: cu-01-1.yaml or cu-ma-01-1.yaml
                if len(parts) >= 3:
                    spread_num = int(parts[-2])
                    page_num = int(parts[-1])
                    actual_pages.append((spread_num, page_num))
            except ValueError:
                warning(f"{char_name} ({char_id}): Unable to parse page format: {page}")

        if actual_pages and actual_pages != expected_pages:
            info(f"{char_name} ({char_id}): Page sequence differs from expected")

    if not warnings_found:
        success("All characters have 24 pages (12 spreads × 2 pages)")

    return True  # Warnings don't fail the test


def test_page_yaml_validity(characters):
    """Test that all page YAML files are valid."""
    errors_found = False
    pages_dir = Path('pages')

    # Collect all referenced pages
    all_pages = set()
    for char_id, char_info in characters.items():
        pages = char_info['data'].get('story', [])
        all_pages.update(pages)

    for page in all_pages:
        page_path = pages_dir / page
        if page_path.exists():
            try:
                with open(page_path, 'r') as f:
                    yaml.safe_load(f)
            except Exception as e:
                error(f"Page '{page}' is not valid YAML: {e}")
                errors_found = True

    if not errors_found:
        success("All page YAML files are valid")
    return not errors_found


def test_page_structure(characters):
    """Test that pages have proper structure (node type, images, etc.)."""
    errors_found = False
    warnings_found = False
    pages_dir = Path('pages')

    # Collect all referenced pages
    all_pages = set()
    for char_id, char_info in characters.items():
        pages = char_info['data'].get('story', [])
        all_pages.update(pages)

    for page in all_pages:
        page_path = pages_dir / page
        if page_path.exists():
            try:
                with open(page_path, 'r') as f:
                    page_data = yaml.safe_load(f)

                # Check for required fields
                if 'node_type' not in page_data:
                    warning(f"Page '{page}' missing 'node_type' field")
                    warnings_found = True
                elif page_data['node_type'] not in ['solo', 'meeting', 'mirrored', 'resonant']:
                    error(f"Page '{page}' has invalid node_type: {page_data['node_type']}")
                    errors_found = True

                # Check for images array
                if 'images' not in page_data:
                    warning(f"Page '{page}' missing 'images' array (new structure requires 2 images per page)")
                    warnings_found = True
                else:
                    images = page_data['images']
                    if not isinstance(images, list):
                        error(f"Page '{page}' 'images' field is not a list")
                        errors_found = True
                    elif len(images) != 2:
                        warning(f"Page '{page}' has {len(images)} images, expected 2")
                        warnings_found = True
                    else:
                        # Check each image structure
                        for i, img in enumerate(images, 1):
                            if 'visual' not in img:
                                error(f"Page '{page}' image {i} missing 'visual' field")
                                errors_found = True
                            if 'text' not in img:
                                error(f"Page '{page}' image {i} missing 'text' field")
                                errors_found = True

                # Validate node-specific metadata
                node_type = page_data.get('node_type')
                if node_type == 'meeting' and 'meeting_data' not in page_data:
                    warning(f"Page '{page}' is a meeting node but missing 'meeting_data'")
                    warnings_found = True
                if node_type == 'mirrored' and 'mirrored_data' not in page_data:
                    warning(f"Page '{page}' is a mirrored node but missing 'mirrored_data'")
                    warnings_found = True
                if node_type == 'resonant' and 'resonant_data' not in page_data:
                    warning(f"Page '{page}' is a resonant node but missing 'resonant_data'")
                    warnings_found = True

            except Exception as e:
                # Skip if already caught by YAML validity test
                pass

    if not errors_found and not warnings_found:
        success("All pages have proper structure")
    elif not errors_found:
        success("Page structure validation passed (with warnings)")

    return not errors_found


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("REPOSITORY STRUCTURE VALIDATION")
    print("="*80 + "\n")

    # Load all characters
    try:
        characters = load_all_characters()
    except SystemExit:
        return 1

    # Run all tests
    tests = [
        ("At least one character exists", lambda: test_at_least_one_character(characters)),
        ("Page formatting is correct", lambda: test_page_formatting(characters)),
        ("All referenced pages exist", lambda: test_pages_exist(characters)),
        ("Spreads 1, 11, 12 are character-specific", lambda: test_no_overlaps_on_required_solo_spreads(characters)),
        ("No stray pages in pages directory", lambda: test_no_stray_pages(characters)),
        ("Page YAML files are valid", lambda: test_page_yaml_validity(characters)),
        ("Page structure validation", lambda: test_page_structure(characters)),
        ("Check for missing pages", lambda: test_missing_pages(characters)),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        print("-" * 80)
        result = test_func()
        results.append(result)

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(results)
    total = len(results)

    if all(results):
        success(f"All {total} tests passed!")
        print()
        return 0
    else:
        error(f"{total - passed} out of {total} tests failed")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
