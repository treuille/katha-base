#!/usr/bin/env python3
"""
Generate an image for a story page using AI image generation.

Usage:
    uv run scripts/gen_image.py <mode> <file> [--style STYLE]

Modes:
    prompt <page_file> [--style STYLE] - Show the image gen prompt and list all referenced images
    gemini <page_file> [--style STYLE] - Generate the image using Gemini
    frame  <image_file>                - Frame an existing image for print with bleed and guide lines

Examples:
    uv run scripts/gen_image.py prompt out/story/p09-arthur-cullan.yaml
    uv run scripts/gen_image.py gemini out/story/p09-arthur-cullan.yaml --style red_tree
    uv run scripts/gen_image.py frame out/images/genealogy_witch/p09-arthur-cullan.jpg

The default style is defined in story/template.yaml (currently 'genealogy_witch').
Available styles (see story/styles.yaml):
    genealogy_witch, red_tree, gashlycrumb, donothing_day, ghost_hunt, ghost_easy

Requirements:
    - GEMINI_API_KEY must be set in .env file (for gemini mode)
    - Reference images must exist in ref/styles/, ref/characters/, ref/locations/, ref/objects/
"""

import sys
import argparse
import yaml
from pathlib import Path
from collections import defaultdict
from google import genai
from google.genai import types
from PIL import Image

# Public API
__all__ = ["build_prompt", "generate_image", "show_prompt", "frame_image", "get_default_style"]

# Target dimensions for final output
# The actual generation uses 3:2 aspect ratio which closely matches this ~1.5 ratio
CONTENT_WIDTH = 3507
CONTENT_HEIGHT = 2334

# Print-ready dimensions (with bleed area)
FULL_WIDTH = 3579      # CONTENT_WIDTH + 2 * BLEED
FULL_HEIGHT = 2406     # CONTENT_HEIGHT + 2 * BLEED
BLEED = 36             # Bleed area on all sides

# Model for image generation (via Vertex AI)
# GEMINI_MODEL = "gemini-2.5-flash-image"
# GEMINI_MODEL = "gemini-3-pro-image"
GEMINI_MODEL = "gemini-3-pro-image-preview"
# GEMINI_MODEL = "imagen-3.0-generate-001"

# Vertex AI configuration
VERTEX_PROJECT = "gen-lang-client-0783348437"
VERTEX_LOCATION = "global"  # Preview models require global endpoint

# Gemini 3 Pro supports max 14 reference images
MAX_TOTAL_IMAGES = 14
MAX_STYLE_IMAGES = 1
MAX_LOCATION_IMAGES = 1
MAX_CHARACTER_IMAGES = 1
CENTER_GUTTER = 1789   # Center line for two-page spread fold


def _load_yaml_file(file_path):
    """Load and parse a YAML file."""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def get_default_style():
    """Get the default style from story/template.yaml.

    Returns:
        str: The default style ID (e.g., 'genealogy_witch')

    Raises:
        ValueError: If no default_style is defined in template.yaml
    """
    template = _load_yaml_file("story/template.yaml")
    default_style = template.get("default_style")
    if not default_style:
        raise ValueError("No default_style defined in story/template.yaml")
    return default_style


def _load_style(style_id):
    """Load style configuration from story/styles.yaml.

    Args:
        style_id: The style identifier (e.g., 'genealogy_witch', 'red_tree')

    Returns:
        dict with 'artist', 'books', and 'prompts' keys

    Raises:
        ValueError: If style_id is not found in styles.yaml
    """
    styles = _load_yaml_file("story/styles.yaml")
    if style_id not in styles:
        available = list(styles.keys())
        raise ValueError(f"Unknown style '{style_id}'. Available: {available}")
    return styles[style_id]


def _load_template_setting():
    """Load the setting description from story/template.yaml.

    This provides story-specific setting info (house, atmosphere, etc.)
    that is combined with the style-specific visual prompts.
    """
    template = _load_yaml_file("story/template.yaml")
    return template.get("visual", [])


def _load_character_visual(character_id):
    """Load visual description for a character."""
    char_file = Path("characters") / f"{character_id}.yaml"
    if not char_file.exists():
        return []

    char_data = _load_yaml_file(char_file)
    return char_data.get("visual", [])


def _load_location_visual(location_id):
    """Load visual description for a location."""
    loc_file = Path("locations") / f"{location_id}.yaml"
    if not loc_file.exists():
        return []

    loc_data = _load_yaml_file(loc_file)
    return loc_data.get("visual", [])


def _collect_reference_images(page_data, style_id):
    """Collect all reference images for style, characters, locations, and objects.

    Args:
        page_data: The page YAML data
        style_id: The style identifier for loading style reference images
    """
    images = []
    image_labels = []

    # Load style info for labeling
    style = _load_style(style_id)
    artist = style.get("artist", style_id)

    # Collect style reference images first (ref/styles/{style_id}-*.jpg)
    style_images = sorted(Path("ref/styles").glob(f"{style_id}-*.jpg"))[:MAX_STYLE_IMAGES]
    for img_path in style_images:
        images.append(str(img_path))
        image_labels.append(
            f"A style reference image showing {artist}'s illustration style"
        )

    # Collect character images
    characters = page_data.get("characters", [])
    for char_id in characters:
        # Find all images for this character (e.g., arthur-01.jpg, arthur-02.jpg)
        char_images = sorted(Path("ref/characters").glob(f"{char_id}-*.jpg"))[:MAX_CHARACTER_IMAGES]
        for img_path in char_images:
            images.append(str(img_path))
            # Extract the display name from the character YAML
            char_file = Path("characters") / f"{char_id}.yaml"
            if char_file.exists():
                char_data = _load_yaml_file(char_file)
                char_name = char_data.get("name", char_id.title())
            else:
                char_name = char_id.title()
            image_labels.append(f"A reference picture of {char_name}")

    # Collect location images
    location = page_data.get("location")
    if location:
        loc_images = sorted(Path("ref/locations").glob(f"{location}-*.jpg"))[:MAX_LOCATION_IMAGES]
        for img_path in loc_images:
            images.append(str(img_path))
            # Extract the display name from the location YAML
            loc_file = Path("locations") / f"{location}.yaml"
            if loc_file.exists():
                loc_data = _load_yaml_file(loc_file)
                loc_name = loc_data.get(
                    "display_name", location.replace("_", " ").title()
                )
            else:
                loc_name = location.replace("_", " ").title()
            image_labels.append(f"A reference picture of the {loc_name}")

    # Collect object images
    objects = page_data.get("objects", [])
    for obj_id in objects:
        obj_images = sorted(Path("ref/objects").glob(f"{obj_id}-*.jpg"))
        for img_path in obj_images:
            images.append(str(img_path))
            image_labels.append(f"A reference picture of {obj_id.replace('_', ' ')}")

    # Validate total image count
    if len(images) > MAX_TOTAL_IMAGES:
        raise ValueError(
            f"Too many reference images ({len(images)}). "
            f"Gemini 3 Pro supports max {MAX_TOTAL_IMAGES} reference images."
        )

    return images, image_labels


def build_prompt(page_data, style_id):
    """Build the complete image generation prompt.

    Args:
        page_data: The page YAML data
        style_id: The style identifier (e.g., 'genealogy_witch')

    Returns:
        tuple: (prompt_text, ref_image_paths, ref_labels) where:
            - prompt_text: The text prompt (without image references, those are interleaved separately)
            - ref_image_paths: List of paths to reference images
            - ref_labels: List of labels describing each reference image
    """
    # Load style prompts and template setting
    style = _load_style(style_id)
    style_prompts = style.get("prompts", [])
    artist = style.get("artist", style_id)
    setting_description = _load_template_setting()

    # Collect reference images
    ref_images, ref_labels = _collect_reference_images(page_data, style_id)

    # Build character visual descriptions
    characters = page_data.get("characters", [])
    char_descriptions = []
    for char_id in characters:
        char_visual = _load_character_visual(char_id)
        if char_visual:
            # Get character name
            char_file = Path("characters") / f"{char_id}.yaml"
            if char_file.exists():
                char_data = _load_yaml_file(char_file)
                char_name = char_data.get("name", char_id.title())
            else:
                char_name = char_id.title()

            char_desc = f"\n{char_name}:\n"
            for item in char_visual:
                char_desc += f"  - {item}\n"
            char_descriptions.append(char_desc)

    # Build location visual description
    location = page_data.get("location")
    location_description = ""
    if location:
        loc_visual = _load_location_visual(location)
        if loc_visual:
            loc_file = Path("locations") / f"{location}.yaml"
            if loc_file.exists():
                loc_data = _load_yaml_file(loc_file)
                loc_name = loc_data.get(
                    "display_name", location.replace("_", " ").title()
                )
            else:
                loc_name = location.replace("_", " ").title()

            location_description = f"\nLocation ({loc_name}):\n"
            for item in loc_visual:
                location_description += f"  - {item}\n"

    # Get page-specific visual description
    page_visual = page_data.get("visual", "")
    if isinstance(page_visual, list):
        page_visual = "\n".join(f"  - {item}" for item in page_visual)

    # Get page text that should be displayed in the image
    page_text = page_data.get("text", "")
    if isinstance(page_text, str):
        page_text = page_text.strip()

    # Build the complete prompt (without image references - those are interleaved separately)
    prompt = f"""Create an illustration for a children's storybook page in {artist}'s illustration style.

VISUAL STYLE ({artist}):
"""
    for style_item in style_prompts:
        prompt += f"  - {style_item}\n"

    if setting_description:
        prompt += "\nSTORY SETTING:\n"
        for setting_item in setting_description:
            prompt += f"  - {setting_item}\n"

    if char_descriptions:
        prompt += "\nCHARACTER VISUAL DETAILS:\n"
        prompt += "".join(char_descriptions)

    if location_description:
        prompt += location_description

    prompt += f"""
PAGE-SPECIFIC SCENE:
{page_visual}
"""

    if page_text:
        prompt += f"""
TEXT TO DISPLAY IN THE IMAGE:
The following text must be included in the illustration with appropriate storybook typography and placement:

"{page_text}"

Please display this text exactly as written in a clear, readable storybook font that fits {artist}'s illustration style.
"""

    prompt += f"""
Please create a single illustration that captures this moment in {artist}'s illustration style, using the reference images provided to ensure character and location consistency. Include lots of fun little details as shown in the reference images.
"""

    return prompt, ref_images, ref_labels


def show_prompt(page_file, style_id):
    """Show the prompt and list referenced images.

    Args:
        page_file: Path to the page YAML file
        style_id: The style identifier (e.g., 'genealogy_witch')
    """
    page_data = _load_yaml_file(page_file)
    prompt, ref_images, ref_labels = build_prompt(page_data, style_id)

    style = _load_style(style_id)
    artist = style.get("artist", style_id)

    print("=" * 80)
    print(f"IMAGE GENERATION PROMPT (Style: {style_id} / {artist})")
    print("=" * 80)
    print()
    print(prompt)
    print()
    print("=" * 80)
    print(f"REFERENCED IMAGES ({len(ref_images)} total)")
    print("=" * 80)
    for i, (img_path, label) in enumerate(zip(ref_images, ref_labels), 1):
        print(f"{i}. {img_path}")
        print(f"   Label: {label}")
    print()


def generate_image(page_file, style_id):
    """Generate image using Gemini.

    Args:
        page_file: Path to the page YAML file
        style_id: The style identifier (e.g., 'genealogy_witch')

    Returns:
        Path to the generated image file
    """
    # Initialize the Gemini client via Vertex AI (higher quota than AI Studio)
    # Uses gcloud application-default credentials (run: gcloud auth application-default login)
    client = genai.Client(
        vertexai=True,
        project=VERTEX_PROJECT,
        location=VERTEX_LOCATION,
    )

    # Load style info
    style = _load_style(style_id)
    artist = style.get("artist", style_id)

    # Load page data and build prompt
    page_data = _load_yaml_file(page_file)
    prompt, ref_images, ref_labels = build_prompt(page_data, style_id)

    print(f"Generating image for {page_file}...")
    print(f"Style: {style_id} ({artist})")
    print(f"Using {len(ref_images)} reference images")
    print(f"Prompt: {len(prompt)} characters")

    # Build multimodal contents by interleaving images with their labels
    # This helps the model associate each image with its description
    contents = []

    for img_path, label in zip(ref_images, ref_labels):
        img = Image.open(img_path)
        contents.append(img)
        contents.append(label)
        print(f"  Loaded: {img_path} ({label})")

    # Add the main prompt at the end
    contents.append(prompt)

    num_images = len([c for c in contents if isinstance(c, Image.Image)])
    print(f"Successfully loaded {num_images} reference images")

    # Determine aspect ratio based on our target dimensions
    # CONTENT_WIDTH = 3507, CONTENT_HEIGHT = 2334, ratio ~= 1.5 (3:2)
    aspect_ratio = "3:2"

    print(f"Calling {GEMINI_MODEL} with aspect ratio {aspect_ratio}...")
    print(f"Sending {num_images} reference images (interleaved with labels) + main prompt")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
            ),
        ),
    )

    # Debug: print full response if parts is None
    if response.parts is None:
        print(f"WARNING: response.parts is None")
        print(f"Full response: {response}")
        if hasattr(response, 'prompt_feedback'):
            print(f"Prompt feedback: {response.prompt_feedback}")
        if hasattr(response, 'candidates') and response.candidates:
            for i, candidate in enumerate(response.candidates):
                print(f"Candidate {i}: {candidate}")
                if hasattr(candidate, 'finish_reason'):
                    print(f"  Finish reason: {candidate.finish_reason}")
                if hasattr(candidate, 'safety_ratings'):
                    print(f"  Safety ratings: {candidate.safety_ratings}")
        raise RuntimeError("API returned no parts - likely content filtering or rate limiting")

    print(f"Response received with {len(response.parts)} part(s)")

    # Extract images from response parts
    generated_images = []
    for part in response.parts:
        if part.inline_data:
            generated_images.append(part)

    if not generated_images:
        raise RuntimeError("No images were generated in the response")

    print(f"Successfully generated {len(generated_images)} image(s)")

    # Save the generated image(s)
    # Use the input filename stem (without .yaml extension) for output
    # Output to style-specific subdirectory
    input_filename = Path(page_file).stem  # e.g., "p09-arthur-cullan"
    output_dir = Path("out/images") / style_id
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = None
    for idx, image_part in enumerate(generated_images):
        # Get the PIL image
        img_obj = image_part.as_image()
        pil_image = img_obj._pil_image

        # Determine output filename - matches input filename with .jpg extension
        if len(generated_images) == 1:
            output_file = output_dir / f"{input_filename}.jpg"
        else:
            output_file = output_dir / f"{input_filename}_{idx + 1}.jpg"

        # Save the image
        pil_image.save(output_file, format="JPEG", quality=95)
        print(f"Saved image to: {output_file}")

    print(f"\nImage generation complete!")

    return output_file


def frame_image(image_path):
    """Frame an image for printing with bleed area and guide lines.

    Takes a generated image and prepares it for print by:
    - Resizing to exact content dimensions (CONTENT_WIDTH x CONTENT_HEIGHT)
    - Adding bleed area (BLEED pixels on all sides)
    - Drawing guide lines for margins and center gutter

    Args:
        image_path: Path to the source image

    Returns:
        Path to the framed image (saved as {original_stem}-framed.jpg)
    """
    from PIL import ImageDraw

    image_path = Path(image_path)

    # Load and resize to content dimensions
    img = Image.open(image_path)
    img_resized = img.resize((CONTENT_WIDTH, CONTENT_HEIGHT), Image.Resampling.LANCZOS)

    # Create white canvas at full dimensions (with bleed)
    canvas = Image.new("RGB", (FULL_WIDTH, FULL_HEIGHT), "white")

    # Paste content centered on canvas (offset by bleed)
    canvas.paste(img_resized, (BLEED, BLEED))

    # Draw guide lines
    draw = ImageDraw.Draw(canvas)
    guide_color = (200, 200, 200)  # Light gray

    # Horizontal lines (top and bottom margins)
    draw.line([(0, BLEED), (FULL_WIDTH, BLEED)], fill=guide_color, width=1)
    draw.line([(0, FULL_HEIGHT - BLEED), (FULL_WIDTH, FULL_HEIGHT - BLEED)], fill=guide_color, width=1)

    # Vertical lines (left and right margins)
    draw.line([(BLEED, 0), (BLEED, FULL_HEIGHT)], fill=guide_color, width=1)
    draw.line([(FULL_WIDTH - BLEED, 0), (FULL_WIDTH - BLEED, FULL_HEIGHT)], fill=guide_color, width=1)

    # Center gutter line (for two-page spread fold)
    draw.line([(CENTER_GUTTER, 0), (CENTER_GUTTER, FULL_HEIGHT)], fill=guide_color, width=1)

    # Save output
    output_dir = Path("out/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{image_path.stem}-framed.jpg"

    canvas.save(output_file, format="JPEG", quality=95)
    print(f"Framed image saved to: {output_file}")
    print(f"  Content: {CONTENT_WIDTH}x{CONTENT_HEIGHT}")
    print(f"  Full (with bleed): {FULL_WIDTH}x{FULL_HEIGHT}")

    return output_file


def _get_available_styles():
    """Get list of available style IDs from styles.yaml."""
    styles_file = Path("story/styles.yaml")
    if styles_file.exists():
        styles = _load_yaml_file(styles_file)
        return list(styles.keys())
    return []


def main():
    """Main entry point."""
    available_styles = _get_available_styles()
    default_style = get_default_style()

    parser = argparse.ArgumentParser(
        description="Generate images for story pages using AI image generation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available styles: {', '.join(available_styles)}\nDefault style: {default_style}"
    )

    subparsers = parser.add_subparsers(dest="mode", required=True, help="Operation mode")

    # prompt subcommand
    prompt_parser = subparsers.add_parser("prompt", help="Show the image gen prompt and list all referenced images")
    prompt_parser.add_argument("page_file", help="Path to the page YAML file")
    prompt_parser.add_argument("--style", default=default_style, help=f"Style ID (default: {default_style})")

    # gemini subcommand
    gemini_parser = subparsers.add_parser("gemini", help="Generate the image using Gemini")
    gemini_parser.add_argument("page_file", help="Path to the page YAML file")
    gemini_parser.add_argument("--style", default=default_style, help=f"Style ID (default: {default_style})")

    # frame subcommand
    frame_parser = subparsers.add_parser("frame", help="Frame an existing image for print with bleed and guide lines")
    frame_parser.add_argument("image_file", help="Path to the image file to frame")

    args = parser.parse_args()

    # Frame mode
    if args.mode == "frame":
        if not Path(args.image_file).exists():
            parser.error(f"Image file '{args.image_file}' not found")
        frame_image(args.image_file)
        return

    # prompt and gemini modes
    page_file = args.page_file
    style_id = args.style

    # Validate input file exists
    if not Path(page_file).exists():
        parser.error(f"Page file '{page_file}' not found")

    # Validate style exists
    if available_styles and style_id not in available_styles:
        parser.error(f"Unknown style '{style_id}'. Must be one of: {', '.join(available_styles)}")

    # Execute the appropriate mode
    if args.mode == "prompt":
        show_prompt(page_file, style_id)
    elif args.mode == "gemini":
        generate_image(page_file, style_id)


if __name__ == "__main__":
    main()
