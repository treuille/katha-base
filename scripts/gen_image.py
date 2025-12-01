#!/usr/bin/env python3
"""
Generate an image for a story page using AI image generation.

Usage:
    uv run scripts/gen_image.py [mode] <page_file>

Modes:
    prompt - Show the image gen prompt and list all referenced images
    gemini - Generate the image using gemini-3-pro-image-preview model

Example:
    uv run scripts/gen_image.py prompt out/story/p09-arthur-cullan.yaml
    uv run scripts/gen_image.py gemini out/story/p09-arthur-cullan.yaml

Requirements:
    - GEMINI_API_KEY must be set in .env file
    - Reference images must exist in ref/characters/, ref/locations/, ref/objects/
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


# Target dimensions for final output
# The actual generation uses 3:2 aspect ratio which closely matches this ~1.5 ratio
CONTENT_WIDTH = 3507
CONTENT_HEIGHT = 2334


def load_yaml_file(file_path):
    """Load and parse a YAML file."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def load_template_visual_style():
    """Load the overall visual style from story/template.yaml."""
    template = load_yaml_file('story/template.yaml')
    return template.get('visual', [])


def load_character_visual(character_id):
    """Load visual description for a character."""
    char_file = Path('characters') / f'{character_id}.yaml'
    if not char_file.exists():
        return []

    char_data = load_yaml_file(char_file)
    return char_data.get('visual', [])


def load_location_visual(location_id):
    """Load visual description for a location."""
    loc_file = Path('locations') / f'{location_id}.yaml'
    if not loc_file.exists():
        return []

    loc_data = load_yaml_file(loc_file)
    return loc_data.get('visual', [])


def collect_reference_images(page_data):
    """Collect all reference images for style, characters, locations, and objects."""
    images = []
    image_labels = []

    # Collect style reference images first
    style_dir = Path('ref/style')
    if style_dir.exists():
        style_images = sorted(style_dir.glob('style-*.jpg'))
        for img_path in style_images:
            images.append(str(img_path))
            image_labels.append(f"A style reference image showing the illustration style")

    # Collect character images
    characters = page_data.get('characters', [])
    for char_id in characters:
        # Find all images for this character (e.g., arthur-01.jpg, arthur-02.jpg)
        char_images = sorted(Path('ref/characters').glob(f'{char_id.replace("_", "-")}-*.jpg'))
        for img_path in char_images:
            images.append(str(img_path))
            # Extract the display name from the character YAML
            char_file = Path('characters') / f'{char_id}.yaml'
            if char_file.exists():
                char_data = load_yaml_file(char_file)
                char_name = char_data.get('name', char_id.title())
            else:
                char_name = char_id.title()
            image_labels.append(f"A reference picture of {char_name}")

    # Collect location images
    location = page_data.get('location')
    if location:
        loc_images = sorted(Path('ref/locations').glob(f'{location.replace("_", "-")}-*.jpg'))
        for img_path in loc_images:
            images.append(str(img_path))
            # Extract the display name from the location YAML
            loc_file = Path('locations') / f'{location}.yaml'
            if loc_file.exists():
                loc_data = load_yaml_file(loc_file)
                loc_name = loc_data.get('display_name', location.replace('_', ' ').title())
            else:
                loc_name = location.replace('_', ' ').title()
            image_labels.append(f"A reference picture of the {loc_name}")

    # Collect object images
    objects = page_data.get('objects', [])
    for obj_id in objects:
        obj_images = sorted(Path('ref/objects').glob(f'{obj_id.replace("_", "-")}-*.jpg'))
        for img_path in obj_images:
            images.append(str(img_path))
            image_labels.append(f"A reference picture of {obj_id.replace('_', ' ')}")

    return images, image_labels


def build_prompt(page_data):
    """Build the complete image generation prompt."""
    # Load visual style from template
    visual_style = load_template_visual_style()

    # Collect reference images
    ref_images, ref_labels = collect_reference_images(page_data)

    # Build the image reference section
    image_ref_text = f"\n\nI have provided {len(ref_images)} reference images:\n\n"
    for i, label in enumerate(ref_labels, 1):
        image_ref_text += f"Image {i}: {label}\n"

    # Build character visual descriptions
    characters = page_data.get('characters', [])
    char_descriptions = []
    for char_id in characters:
        char_visual = load_character_visual(char_id)
        if char_visual:
            # Get character name
            char_file = Path('characters') / f'{char_id}.yaml'
            if char_file.exists():
                char_data = load_yaml_file(char_file)
                char_name = char_data.get('name', char_id.title())
            else:
                char_name = char_id.title()

            char_desc = f"\n{char_name}:\n"
            for item in char_visual:
                char_desc += f"  - {item}\n"
            char_descriptions.append(char_desc)

    # Build location visual description
    location = page_data.get('location')
    location_description = ""
    if location:
        loc_visual = load_location_visual(location)
        if loc_visual:
            loc_file = Path('locations') / f'{location}.yaml'
            if loc_file.exists():
                loc_data = load_yaml_file(loc_file)
                loc_name = loc_data.get('display_name', location.replace('_', ' ').title())
            else:
                loc_name = location.replace('_', ' ').title()

            location_description = f"\nLocation ({loc_name}):\n"
            for item in loc_visual:
                location_description += f"  - {item}\n"

    # Get page-specific visual description
    page_visual = page_data.get('visual', '')
    if isinstance(page_visual, list):
        page_visual = '\n'.join(f"  - {item}" for item in page_visual)

    # Get page text that should be displayed in the image
    page_text = page_data.get('text', '')
    if isinstance(page_text, str):
        page_text = page_text.strip()

    # Build the complete prompt
    prompt = f"""Create an illustration for a children's storybook page.

OVERALL VISUAL STYLE:
"""
    for style_item in visual_style:
        prompt += f"  - {style_item}\n"

    prompt += image_ref_text

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

Please display this text exactly as written in a clear, readable storybook font that fits the Marin Hanford illustration style.
"""

    prompt += """
Please create a single illustration that captures this moment in the Marin Hanford illustration style, using the reference images provided to ensure character and location consistency. Include lots of fun little details as shown in the reference images.
"""

    return prompt, ref_images


def show_prompt_mode(page_file):
    """Show the prompt and list referenced images."""
    page_data = load_yaml_file(page_file)
    prompt, ref_images = build_prompt(page_data)

    print("=" * 80)
    print("IMAGE GENERATION PROMPT")
    print("=" * 80)
    print()
    print(prompt)
    print()
    print("=" * 80)
    print(f"REFERENCED IMAGES ({len(ref_images)} total)")
    print("=" * 80)
    for i, img_path in enumerate(ref_images, 1):
        print(f"{i}. {img_path}")
    print()


def generate_with_gemini(page_file):
    """Generate image using Gemini."""
    # Get API key
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("Please copy .env.example to .env and set your GEMINI_API_KEY")
        sys.exit(1)

    # Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    # Load page data and build prompt
    page_data = load_yaml_file(page_file)
    prompt, ref_images = build_prompt(page_data)

    print(f"Generating image for {page_file}...")
    print(f"Using {len(ref_images)} reference images")
    print(f"Prompt: {len(prompt)} characters")

    # Load reference images as PIL Images
    loaded_images = []
    for img_path in ref_images:
        try:
            img = Image.open(img_path)
            loaded_images.append(img)
            print(f"  Loaded: {img_path}")
        except Exception as e:
            print(f"  Warning: Could not load {img_path}: {e}")

    print(f"Successfully loaded {len(loaded_images)} reference images")

    # Determine aspect ratio based on our target dimensions
    # CONTENT_WIDTH = 3507, CONTENT_HEIGHT = 2334, ratio ~= 1.5 (3:2)
    aspect_ratio = "3:2"

    # Build multimodal contents: reference images + text prompt
    # The images come first, then the text prompt
    contents = loaded_images + [prompt]

    # Use Gemini to generate the image
    try:
        print(f"Calling gemini-3-pro-image-preview with aspect ratio {aspect_ratio}...")
        print(f"Sending {len(loaded_images)} reference images + text prompt")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                )
            )
        )

        print(f"Response received with {len(response.parts)} part(s)")

        # Extract images from response parts
        generated_images = []
        for part in response.parts:
            if part.inline_data:
                generated_images.append(part)

        if not generated_images:
            print("Error: No images were generated in the response")
            sys.exit(1)

        print(f"Successfully generated {len(generated_images)} image(s)")

        # Save the generated image(s)
        page_id = page_data.get('id', 'unknown')
        output_dir = Path('out/images')
        output_dir.mkdir(parents=True, exist_ok=True)

        for idx, image_part in enumerate(generated_images):
            # Get the PIL image
            img_obj = image_part.as_image()
            pil_image = img_obj._pil_image

            # Determine output filename
            if len(generated_images) == 1:
                output_file = output_dir / f'{page_id}.jpg'
            else:
                output_file = output_dir / f'{page_id}_{idx + 1}.jpg'

            # Save the image
            pil_image.save(output_file, format='JPEG', quality=95)
            print(f"✅ Saved image to: {output_file}")

        print(f"\n🎉 Image generation complete!")

    except Exception as e:
        print(f"Error generating image: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Parse arguments
    if len(sys.argv) == 2:
        # Assume prompt mode if only page file is given
        mode = 'prompt'
        page_file = sys.argv[1]
    else:
        mode = sys.argv[1]
        page_file = sys.argv[2]

    # Validate mode
    if mode not in ['prompt', 'gemini']:
        print(f"Error: Invalid mode '{mode}'. Must be 'prompt' or 'gemini'")
        print(__doc__)
        sys.exit(1)

    # Validate page file exists
    if not Path(page_file).exists():
        print(f"Error: Page file '{page_file}' not found")
        sys.exit(1)

    # Execute the appropriate mode
    if mode == 'prompt':
        show_prompt_mode(page_file)
    elif mode == 'gemini':
        generate_with_gemini(page_file)


if __name__ == '__main__':
    main()
