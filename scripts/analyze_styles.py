#!/usr/bin/env python3
"""
Analyze visual style images and generate style descriptions for prompts.

Usage:
    uv run scripts/analyze_styles.py [mode] [style_id]

Modes:
    list    - List all available styles and their images
    analyze - Analyze style images and generate descriptions (writes to styles.yaml)
    show    - Show the current styles.yaml content

Arguments:
    style_id - Optional: analyze only a specific style (e.g., 'red_tree')

Example:
    uv run scripts/analyze_styles.py list
    uv run scripts/analyze_styles.py analyze
    uv run scripts/analyze_styles.py analyze red_tree
    uv run scripts/analyze_styles.py show

Requirements:
    - GEMINI_API_KEY must be set in .env file
    - Style images must exist in ref/styles/ with naming convention {style_id}-{##}.jpg
"""

import sys
import yaml
from pathlib import Path
from collections import defaultdict
from google import genai
from google.genai import types
import os
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Style order from README (order of preference)
STYLE_ORDER = [
    "genealogy_witch",
    "donothing_day",
    "red_tree",
    "wolves_walls",
    "witchlings",
    "ghost_hunt",
    "gashlycrumb",
    "ghost_easy",
]

# Style metadata (artist and book info)
STYLE_METADATA = {
    "genealogy_witch": {
        "artist": "Benjamin Lacombe",
        "books": ["Genealogy of a Witch", "Madame Butterfly"],
    },
    "donothing_day": {
        "artist": "Beatrice Alemagna",
        "books": ["On a Magical Do-Nothing Day"],
    },
    "red_tree": {
        "artist": "Shaun Tan",
        "books": ["The Red Tree"],
    },
    "wolves_walls": {
        "artist": "Dave McKean",
        "books": ["The Wolves in the Walls"],
    },
    "witchlings": {
        "artist": "Júlia Sardà",
        "books": ["The Queen in the Cave", "The Witch in the Tower"],
    },
    "ghost_hunt": {
        "artist": "Cherie Zamazing",
        "books": ["We're Going On A Ghost Hunt"],
    },
    "gashlycrumb": {
        "artist": "Edward Gorey",
        "books": ["The Gashlycrumb Tinies"],
    },
    "ghost_easy": {
        "artist": "Stephanie Laberis",
        "books": ["It's Not Easy Being A Ghost"],
    },
}

STYLES_YAML_PATH = Path("styles.yaml")
STYLES_DIR = Path("ref/styles")


def collect_style_images():
    """Collect all style images grouped by style ID."""
    styles = defaultdict(list)

    if not STYLES_DIR.exists():
        return styles

    for img_path in sorted(STYLES_DIR.glob("*.jpg")):
        # Parse style ID from filename (e.g., "red_tree-01.jpg" -> "red_tree")
        name = img_path.stem
        if "-" in name:
            style_id = name.rsplit("-", 1)[0]
            styles[style_id].append(img_path)

    return styles


def list_styles():
    """List all available styles and their images."""
    styles = collect_style_images()

    print("=" * 60)
    print("AVAILABLE VISUAL STYLES")
    print("=" * 60)
    print()

    for style_id in STYLE_ORDER:
        if style_id in styles:
            images = styles[style_id]
            meta = STYLE_METADATA.get(style_id, {})
            artist = meta.get("artist", "Unknown")
            books = ", ".join(meta.get("books", []))

            print(f"  {style_id}")
            print(f"    Artist: {artist}")
            print(f"    Books: {books}")
            print(f"    Images: {len(images)}")
            for img in images:
                print(f"      - {img.name}")
            print()

    # Check for any styles not in STYLE_ORDER
    extra_styles = set(styles.keys()) - set(STYLE_ORDER)
    if extra_styles:
        print("ADDITIONAL STYLES (not in preference order):")
        for style_id in sorted(extra_styles):
            images = styles[style_id]
            print(f"  {style_id}: {len(images)} images")
        print()


def analyze_style(client, style_id, image_paths):
    """Analyze a style's images and generate description prompts.

    Args:
        client: Gemini client
        style_id: The style identifier
        image_paths: List of paths to style images

    Returns:
        List of style descriptor strings
    """
    print(f"\nAnalyzing style: {style_id}")
    print(f"  Loading {len(image_paths)} images...")

    # Load images
    contents = []
    for img_path in image_paths:
        img = Image.open(img_path)
        contents.append(img)
        print(f"    Loaded: {img_path.name}")

    # Get metadata
    meta = STYLE_METADATA.get(style_id, {})
    artist = meta.get("artist", "Unknown artist")
    books = ", ".join(meta.get("books", ["Unknown book"]))

    # Build the analysis prompt
    prompt = f"""Analyze these illustration images from {artist}'s work (from: {books}).

Generate a list of 8-12 specific, actionable style descriptors that could be used as prompts to recreate this visual style. Each descriptor should be a complete phrase that describes one aspect of the style.

Focus on:
- Color palette and color relationships
- Line quality and stroke characteristics
- Texture and surface treatment
- Composition and framing tendencies
- Character rendering style (if applicable)
- Mood and atmosphere
- Medium/technique appearance (e.g., "watercolor washes", "ink crosshatching")
- Any distinctive or unique visual signatures

Format your response as a simple bulleted list with one descriptor per line, starting each line with "- ".
Do not include any preamble or explanation, just the bulleted list.
Each descriptor should be specific enough to guide an AI image generator.

Example format:
- Muted earth tones with occasional pops of deep crimson
- Delicate crosshatching for shadows and texture
- Slightly elongated figure proportions with oversized eyes
"""

    contents.append(prompt)

    print(f"  Calling Gemini for style analysis...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
    )

    # Parse the response into a list of descriptors
    text = response.text.strip()
    descriptors = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            descriptors.append(line[2:].strip())
        elif line.startswith("* "):
            descriptors.append(line[2:].strip())

    print(f"  Generated {len(descriptors)} style descriptors")
    return descriptors


def analyze_styles(style_filter=None):
    """Analyze all styles (or a specific one) and write to styles.yaml.

    Args:
        style_filter: Optional style ID to analyze only that style
    """
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    # Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    # Collect style images
    styles = collect_style_images()

    if not styles:
        raise ValueError("No style images found in ref/styles/")

    # Load existing styles.yaml if it exists
    if STYLES_YAML_PATH.exists():
        with open(STYLES_YAML_PATH, "r") as f:
            styles_data = yaml.safe_load(f) or {}
    else:
        styles_data = {}

    # Determine which styles to analyze
    if style_filter:
        if style_filter not in styles:
            raise ValueError(f"Style '{style_filter}' not found. Available: {', '.join(styles.keys())}")
        styles_to_analyze = [style_filter]
    else:
        styles_to_analyze = [s for s in STYLE_ORDER if s in styles]

    print("=" * 60)
    print("ANALYZING VISUAL STYLES")
    print("=" * 60)
    print(f"Styles to analyze: {', '.join(styles_to_analyze)}")

    # Analyze each style
    for style_id in styles_to_analyze:
        image_paths = styles[style_id]
        meta = STYLE_METADATA.get(style_id, {})

        descriptors = analyze_style(client, style_id, image_paths)
        styles_data[style_id] = {
            "artist": meta.get("artist", "Unknown"),
            "books": meta.get("books", []),
            "prompts": descriptors,
        }

    # Reorder styles_data according to STYLE_ORDER
    ordered_data = {}
    for style_id in STYLE_ORDER:
        if style_id in styles_data:
            ordered_data[style_id] = styles_data[style_id]
    # Add any extra styles at the end
    for style_id in styles_data:
        if style_id not in ordered_data:
            ordered_data[style_id] = styles_data[style_id]

    # Write to styles.yaml
    with open(STYLES_YAML_PATH, "w") as f:
        yaml.dump(ordered_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print()
    print("=" * 60)
    print(f"Wrote style descriptions to {STYLES_YAML_PATH}")
    print("=" * 60)


def show_styles():
    """Show the current styles.yaml content."""
    if not STYLES_YAML_PATH.exists():
        print(f"No {STYLES_YAML_PATH} file found.")
        print("Run 'uv run scripts/analyze_styles.py analyze' to generate it.")
        return

    with open(STYLES_YAML_PATH, "r") as f:
        content = f.read()

    print("=" * 60)
    print(f"CONTENTS OF {STYLES_YAML_PATH}")
    print("=" * 60)
    print()
    print(content)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]
    style_filter = sys.argv[2] if len(sys.argv) > 2 else None

    if mode == "list":
        list_styles()
    elif mode == "analyze":
        analyze_styles(style_filter)
    elif mode == "show":
        show_styles()
    else:
        print(f"Error: Invalid mode '{mode}'. Must be 'list', 'analyze', or 'show'")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
