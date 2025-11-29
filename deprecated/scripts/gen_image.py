#!/usr/bin/env python3
"""
Generate images for storybook pages using various AI models.

Usage:
    uv run scripts/gen_image.py <model-backend> <page-path>

Model Backends:
    openai      - OpenAI gpt-image-1 (generates at 1536x1024, upscales to 3579x2406)
                  Content centered at 3507x2334 with 36px bleed on all sides
                  Photobook format with guide lines for 6x8.5" spread
                  Uses reference images from ref-images/ directory (up to 10 images)
                  Falls back to generation if no reference images found
    prompt      - Display prompt without generating image (testing)

    (Deprecated backends: replicate, ideogram)

Reference Images:
    The script automatically includes reference images based on the page ID:
    - style-*.jpg: Always included for style
    - {char}-*.jpg: Included when character appears in the scene
      (e.g., cu-1.jpg for Cullan, em-1.jpg for Emer, ha-1.jpg for Hansel)

Examples:
    uv run scripts/gen_image.py openai pages/cu-01.yaml
    uv run scripts/gen_image.py prompt pages/cu-ha-02.yaml
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model backend configurations
BACKENDS = {
    "openai": {
        "name": "OpenAI gpt-image-1",
        "env_vars": ["OPENAI_API_KEY"],
        "deprecated": False,
    },
    "replicate": {
        "name": "Replicate IPAdapter Style SDXL (DEPRECATED)",
        "env_vars": ["REPLICATE_API_TOKEN"],
        "deprecated": True,
    },
    "ideogram": {
        "name": "Ideogram v3 (DEPRECATED)",
        "env_vars": ["IDEOGRAM_API_KEY", "IDEOGRAM_API_URL"],
        "deprecated": True,
    },
    "prompt": {
        "name": "Prompt Only (Testing)",
        "env_vars": [],
        "deprecated": False,
    },
}


def print_help():
    """Print help message."""
    print(__doc__)
    print("\nAvailable Model Backends:")
    for backend, config in BACKENDS.items():
        print(f"  {backend:12} - {config['name']}")
    print("\nRequired Environment Variables:")
    for backend, config in BACKENDS.items():
        print(f"  {backend:12} - {', '.join(config['env_vars'])}")
    print("\nNote: Copy .env.example to .env and fill in your API keys")


def validate_args(args):
    """Validate command line arguments."""
    if len(args) != 3:
        print("Error: Invalid number of arguments\n")
        print_help()
        sys.exit(1)

    backend = args[1]
    page_path = args[2]

    if backend not in BACKENDS:
        print(f"Error: Unknown model backend '{backend}'\n")
        print_help()
        sys.exit(1)

    return backend, page_path


def check_api_keys(backend: str):
    """Check if required API keys are present."""
    # Skip check for prompt backend
    if backend == "prompt":
        return

    missing_keys = []
    required_vars = BACKENDS[backend]["env_vars"]

    for var in required_vars:
        if not os.getenv(var):
            missing_keys.append(var)

    if missing_keys:
        print(f"Error: Missing required environment variables for {backend}:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\nPlease set these in your .env file (see .env.example)")
        sys.exit(1)


def get_reference_images(page_id: str) -> list:
    """
    Get reference images for a page based on its ID.
    Returns a list of dicts with 'path' and 'description'.
    """
    ref_dir = Path("ref-images")
    if not ref_dir.exists():
        return []

    # Character ID to name mapping
    char_names = {
        "cu": "Cullan",
        "em": "Emer",
        "ha": "Hansel",
    }

    references = []

    # Always include style reference images
    style_images = sorted(ref_dir.glob("style-*.jpg"))
    for img in style_images:
        references.append(
            {"path": img, "description": "a style reference image"}
        )

    # Parse character IDs from page ID
    # Examples: cu-01 -> [cu], cu-ha-02 -> [cu, ha], em-06 -> [em]
    parts = page_id.split("-")
    char_ids = []
    for part in parts:
        if len(part) == 2 and part.isalpha() and part in char_names:
            char_ids.append(part)

    # Include character reference images
    for char_id in char_ids:
        char_images = sorted(ref_dir.glob(f"{char_id}-*.jpg"))
        char_name = char_names.get(char_id, char_id.upper())
        for img in char_images:
            references.append(
                {"path": img, "description": f"a reference image for {char_name}"}
            )

    return references


def load_visual_style() -> str:
    """Load the visual style from world.yaml."""
    world_path = Path("world.yaml")

    if not world_path.exists():
        print("Warning: world.yaml not found, skipping visual style")
        return ""

    try:
        with open(world_path, "r") as f:
            world_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Failed to load world.yaml: {e}")
        return ""

    visual_style = world_data.get("visual_style", [])
    if visual_style:
        return "\n".join(f"- {item}" for item in visual_style)
    else:
        print("Warning: No 'visual_style' found in world.yaml")
    return ""


def load_character_descriptions(page_id: str) -> dict:
    """
    Load visual descriptions for characters appearing in this page.
    Returns dict mapping character names to their visual descriptions.
    """
    char_dir = Path("characters")
    if not char_dir.exists():
        print("Warning: characters/ directory not found")
        return {}

    # Character ID to filename mapping
    char_files = {
        "cu": "cu-cullan.yaml",
        "em": "em-emer.yaml",
        "ha": "ha-hansel.yaml",
    }

    # Parse character IDs from page ID
    parts = page_id.split("-")
    char_ids = []
    for part in parts:
        if len(part) == 2 and part.isalpha() and part in char_files:
            char_ids.append(part)

    character_descriptions = {}

    for char_id in char_ids:
        char_file = char_dir / char_files[char_id]
        if not char_file.exists():
            print(f"Warning: Character file not found: {char_file}")
            continue

        try:
            with open(char_file, "r") as f:
                char_data = yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Failed to load {char_file}: {e}")
            continue

        char_name = char_data.get("attributes", {}).get("name", char_id.upper())
        visual_desc = char_data.get("attributes", {}).get("visual_description", [])

        if visual_desc:
            character_descriptions[char_name] = visual_desc
        else:
            print(f"Warning: No 'visual_description' found for {char_name} in {char_file}")

    return character_descriptions


def load_page_data(page_path: str) -> dict:
    """Load the page data from a page YAML file."""
    page_path = Path(page_path)

    if not page_path.exists():
        print(f"Error: Page file not found: {page_path}")
        sys.exit(1)

    try:
        with open(page_path, "r") as f:
            page_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Failed to load page file: {e}")
        sys.exit(1)

    visual_prompt = page_data.get("visual", "")
    if not visual_prompt:
        print(f"Error: No 'visual' field found in {page_path}")
        sys.exit(1)

    return page_data


def build_full_prompt(
    page_data: dict, visual_style: str, references: list, character_descriptions: dict
) -> str:
    """Build the complete prompt with visual style and visual content."""
    visual = page_data.get("visual", "")
    text = page_data.get("text", "")

    prompt_parts = [
        "Create a beautiful illustration for a children's storybook page.",
        "Output a single wide image for a two-page spread.",
        "Do not multiple images or panels, just one cohesive scene.",
    ]

    # Add text instructions at the top if text is present
    if text:
        prompt_parts.append("")
        prompt_parts.append("IMPORTANT: You MUST include story text as readable typography in the image.")
        prompt_parts.append("The text should be clearly legible, using 16pt font size.")
        prompt_parts.append("CRITICAL: Do NOT place any text across the 50% vertical centerline of the image.")
        prompt_parts.append("The center is where the two-page spread folds together - keep text away from this area.")
        prompt_parts.append("Place text either on the left side or right side, but never spanning across the middle.")
        prompt_parts.append("Integrate the text into the illustration using a font style that matches the storybook aesthetic.")
        prompt_parts.append("The exact text to include will be provided at the end of this prompt.")

    # Add reference images section
    if references:
        prompt_parts.append("\n--- REFERENCE IMAGES ---")
        for i, ref in enumerate(references, start=1):
            prompt_parts.append(f"Image {i} is {ref['description']}.")

    # Add visual style
    if visual_style:
        prompt_parts.append("\n--- VISUAL STYLE ---")
        prompt_parts.append(visual_style)

    # Add character visual descriptions
    if character_descriptions:
        prompt_parts.append("\n--- CHARACTER VISUAL DESCRIPTIONS ---")
        for char_name, desc_list in character_descriptions.items():
            prompt_parts.append(f"\n{char_name}:")
            for item in desc_list:
                prompt_parts.append(f"- {item}")

    # Add image content
    prompt_parts.append("\n--- SCENE TO ILLUSTRATE ---")
    prompt_parts.append(visual)

    # Add actual text content at the bottom
    if text:
        prompt_parts.append("\n--- TEXT TO INCLUDE IN IMAGE ---")
        prompt_parts.append(text.strip())

    return "\n".join(prompt_parts)


def generate_with_openai(prompt: str, page_id: str, references: list) -> str:
    """Generate image using OpenAI gpt-image-1 with reference images."""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed. Run: uv pip install openai")
        sys.exit(1)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print(f"Generating image with OpenAI gpt-image-1...")
    print(f"Prompt length: {len(prompt)} characters")
    if references:
        print(f"Using {len(references)} reference image(s)")

    # Truncate prompt if too long
    if len(prompt) > 10000:
        print(f"Warning: Prompt truncated from {len(prompt)} to 10000 characters")
        prompt = prompt[:10000]

    try:
        # If we have reference images, use images.edit()
        # Otherwise fall back to images.generate()
        if references:
            # Open reference image files (max 10)
            image_files = []
            try:
                for ref in references[:10]:  # Limit to 10 images
                    image_files.append(open(ref['path'], 'rb'))

                response = client.images.edit(
                    model="gpt-image-1",
                    image=image_files,
                    prompt=prompt,
                    size="1536x1024",  # Landscape 3:2 (closest to 2:1 available)
                    quality="high",
                    n=1,
                )
            finally:
                # Close all opened files
                for f in image_files:
                    f.close()
        else:
            # No reference images, use regular generation
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1536x1024",  # Landscape 3:2 (closest to 2:1 available)
                quality="high",
                n=1,
            )

        # Handle both URL and base64 responses
        import base64
        import io
        from PIL import Image, ImageDraw

        # Check if response has URL or base64 data
        if hasattr(response.data[0], 'url') and response.data[0].url:
            # Download from URL
            import requests
            image_data = requests.get(response.data[0].url).content
        elif hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
            # Decode base64 data
            image_data = base64.b64decode(response.data[0].b64_json)
        else:
            print(f"Error: Unexpected response format from OpenAI API")
            print(f"Response: {response}")
            sys.exit(1)

        # Load image from bytes
        print("Processing image for photobook format...")
        img = Image.open(io.BytesIO(image_data))

        # Inner content dimensions (the actual generated image area)
        CONTENT_WIDTH = 3507
        CONTENT_HEIGHT = 2334

        # Full output dimensions with bleed area
        FULL_WIDTH = 3579
        FULL_HEIGHT = 2406

        # Upscale to content size using Lanczos resampling for quality
        print(f"Upscaling from {img.size[0]}x{img.size[1]} to {CONTENT_WIDTH}x{CONTENT_HEIGHT}...")
        img = img.resize((CONTENT_WIDTH, CONTENT_HEIGHT), Image.Resampling.LANCZOS)

        # Convert to RGB if needed (for JPG format)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Create larger canvas with white background
        print(f"Creating full canvas {FULL_WIDTH}x{FULL_HEIGHT}...")
        canvas = Image.new('RGB', (FULL_WIDTH, FULL_HEIGHT), (255, 255, 255))

        # Calculate centering offset (should be 36, 36)
        offset_x = (FULL_WIDTH - CONTENT_WIDTH) // 2
        offset_y = (FULL_HEIGHT - CONTENT_HEIGHT) // 2

        # Paste the upscaled image centered on the canvas
        canvas.paste(img, (offset_x, offset_y))

        # Add guide lines on the full canvas
        print("Adding photobook guide lines...")
        draw = ImageDraw.Draw(canvas)

        # Horizontal guide lines (spanning full width)
        draw.line([(0, 36), (FULL_WIDTH, 36)], fill=(0, 0, 0), width=1)  # Top margin
        draw.line([(0, 2370), (FULL_WIDTH, 2370)], fill=(0, 0, 0), width=1)  # Bottom margin

        # Vertical guide lines (spanning full height)
        draw.line([(36, 0), (36, FULL_HEIGHT)], fill=(0, 0, 0), width=1)  # Left margin
        draw.line([(3543, 0), (3543, FULL_HEIGHT)], fill=(0, 0, 0), width=1)  # Right margin
        draw.line([(1789, 0), (1789, FULL_HEIGHT)], fill=(0, 0, 0), width=1)  # Center gutter/spine

        # Use canvas instead of img for saving
        img = canvas

        # Save to output directory
        output_dir = Path("out-images")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{page_id}-openai.jpg"

        print(f"Saving photobook-ready image ({FULL_WIDTH}x{FULL_HEIGHT})...")
        img.save(output_path, "JPEG", quality=95)

        return str(output_path)

    except Exception as e:
        print(f"Error generating image with OpenAI: {e}")
        sys.exit(1)


# DEPRECATED: Replicate backend - commented out for now
# def generate_with_replicate(prompt: str, page_id: str) -> str:
#     """Generate image using Replicate IPAdapter Style SDXL."""
#     try:
#         import replicate
#     except ImportError:
#         print("Error: replicate package not installed. Run: uv pip install replicate")
#         sys.exit(1)
#
#     print(f"Generating image with Replicate IPAdapter Style SDXL...")
#     print(f"Prompt length: {len(prompt)} characters")
#
#     try:
#         # Use hardcoded style reference image
#         style_image_path = Path("out-images/cu-01-openai.jpg")
#         print(f"Using style reference: {style_image_path}")
#
#         # Open and use the style image (will fail if doesn't exist)
#         with open(style_image_path, "rb") as f:
#             output = replicate.run(
#                 "lucataco/ipadapter-style-sdxl:9a89134b4c84c264c817645f1703db1e73f66a43c3f0bf2697ec2edce95f7d39",
#                 input={
#                     "prompt": prompt,
#                     "style_image": f,
#                     "width": 1536,
#                     "height": 768,
#                     "num_outputs": 1,
#                     "guidance_scale": 7.5,
#                     "num_inference_steps": 50,
#                     "style_strength": 0.5,  # How much to apply the style (0-1)
#                 },
#             )
#
#         # Download the image
#         import requests
#
#         image_url = output[0]
#         image_data = requests.get(image_url).content
#
#         # Save to out-images directory
#         output_dir = Path("out-images")
#         output_dir.mkdir(parents=True, exist_ok=True)
#
#         output_path = output_dir / f"{page_id}-replicate.jpg"
#
#         with open(output_path, "wb") as f:
#             f.write(image_data)
#
#         return str(output_path)
#
#     except Exception as e:
#         print(f"Error generating image with Replicate: {e}")
#         sys.exit(1)


# DEPRECATED: Ideogram backend - commented out for now
# def generate_with_ideogram(prompt: str, page_id: str) -> str:
#     """Generate image using Ideogram v3."""
#     import requests
#
#     api_key = os.getenv("IDEOGRAM_API_KEY")
#     api_url = os.getenv(
#         "IDEOGRAM_API_URL", "https://api.ideogram.ai/v1/ideogram-v3/generate"
#     )
#
#     print(f"Generating image with Ideogram v3...")
#     print(f"Prompt length: {len(prompt)} characters")
#
#     headers = {
#         "Api-Key": api_key,
#         "Content-Type": "application/json",
#     }
#
#     # Use flat JSON structure (not nested under image_request)
#     payload = {
#         "prompt": prompt,
#         "aspect_ratio": "3x1",  # Wide aspect ratio
#         "magic_prompt": "OFF",
#     }
#
#     try:
#         response = requests.post(api_url, headers=headers, json=payload)
#         response.raise_for_status()
#
#         result = response.json()
#
#         # Extract image URL from response
#         if "data" in result and len(result["data"]) > 0:
#             image_url = result["data"][0].get("url")
#         else:
#             print(f"Error: Unexpected API response structure: {result}")
#             sys.exit(1)
#
#         # Download the image
#         image_data = requests.get(image_url).content
#
#         # Save to out-images directory
#         output_dir = Path("out-images")
#         output_dir.mkdir(parents=True, exist_ok=True)
#
#         output_path = output_dir / f"{page_id}-ideogram.jpg"
#
#         with open(output_path, "wb") as f:
#             f.write(image_data)
#
#         return str(output_path)
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error generating image with Ideogram: {e}")
#         if hasattr(e, "response") and e.response is not None:
#             print(f"Response: {e.response.text}")
#         sys.exit(1)


def generate_prompt(prompt: str, page_id: str) -> str:
    """Display the prompt without generating an image."""
    print(f"\n{'='*80}")
    print("GENERATED PROMPT")
    print(f"{'='*80}\n")
    print(prompt)
    print(f"\n{'='*80}")
    print(f"Prompt length: {len(prompt)} characters")
    print(f"Page ID: {page_id}")
    print(f"{'='*80}\n")
    return "N/A (prompt mode)"


def main():
    """Main entry point."""
    # Validate arguments
    if len(sys.argv) == 1 or sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
        sys.exit(0)

    backend, page_path = validate_args(sys.argv)

    # Extract page ID from path for output filename (e.g., "pages/cu-ha-02.yaml" -> "cu-ha-02")
    page_id = Path(page_path).stem

    # Check API keys before doing anything
    print(f"Checking API keys for {backend}...")
    check_api_keys(backend)

    # Get reference images for this page
    print(f"Loading reference images for {page_id}...")
    references = get_reference_images(page_id)
    if references:
        print(f"  Found {len(references)} reference image(s)")
        for ref in references:
            print(f"    - {ref['path'].name}: {ref['description']}")
    else:
        print(f"  No reference images found")

    # Load visual style and page data
    print(f"Loading visual style...")
    visual_style = load_visual_style()

    # Load character descriptions
    print(f"Loading character descriptions for {page_id}...")
    character_descriptions = load_character_descriptions(page_id)
    if character_descriptions:
        print(f"  Found descriptions for {len(character_descriptions)} character(s)")
        for char_name in character_descriptions:
            print(f"    - {char_name}")
    else:
        print(f"  No character descriptions found")

    print(f"Loading page: {page_path}")
    page_data = load_page_data(page_path)

    # Build complete prompt
    prompt = build_full_prompt(page_data, visual_style, references, character_descriptions)

    # Generate image with selected backend
    if backend == "openai":
        output_path = generate_with_openai(prompt, page_id, references)
    elif backend == "replicate":
        print("Error: Replicate backend is currently deprecated")
        print("Use 'openai' or 'prompt' backend instead")
        sys.exit(1)
    elif backend == "ideogram":
        print("Error: Ideogram backend is currently deprecated")
        print("Use 'openai' or 'prompt' backend instead")
        sys.exit(1)
    elif backend == "prompt":
        output_path = generate_prompt(prompt, page_id)

    if backend != "prompt":
        print(f"\n✓ Image generated successfully!")
        print(f"  Saved to: {output_path}")


if __name__ == "__main__":
    main()
