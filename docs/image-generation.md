# Image Generation

Generate AI illustrations for storybook pages using the `gen_image.py` script.

## Usage

### Generate a Single Page

```bash
uv run scripts/gen_image.py <model-backend> <page-path>
```

### Generate All Pages in Parallel

```bash
uv run scripts/gen_all_images.py [--workers N] [--backend MODEL]
```

## Naming Convention

Generated images follow the format: `{page-id}-openai.jpg`

Examples:
- `cu-01-openai.jpg` - Cullan's first page
- `em-05-openai.jpg` - Emer's fifth page
- `cu-ha-07-openai.jpg` - Shared page with Cullan and Hansel

## Image Specifications

- **Model**: OpenAI gpt-image-1
- **Aspect Ratio**: 3:2 (landscape)
- **Resolution**: 1536x1024 pixels
- **Format**: JPEG (.jpg)

## Available Backends

- **openai** - OpenAI gpt-image-1 (recommended)
  - Uses reference images from `ref-images/` directory (up to 10 images)
  - Automatically includes character visual descriptions
  - Embeds story text as typography in the image
  - Falls back to standard generation if no reference images found
- **prompt** - Test mode (displays prompt without generating)

**Note**: The `replicate` and `ideogram` backends are deprecated and no longer functional.

## What Gets Generated

Each image includes:
1. **Reference Images** - Visual style from `ref-images/` directory
   - World reference images (world-*.jpg) for overall aesthetic
   - Character reference images (cu-*.jpg, em-*.jpg, etc.) for character appearance
2. **World Visual Style** - Style description from `world.yaml`
3. **Character Visual Descriptions** - Physical descriptions from character YAML files
4. **Scene Illustration** - Visual description from the page YAML file
5. **Story Text** - Embedded as readable typography (avoiding the center fold line)

**Important**: Each generated image should be a single frame showing one moment in time. The visual descriptions should NOT include panels, subframes, or multiple scenes. Create one cohesive illustration per page.

## Reference Images

The script automatically includes reference images based on the page being generated:

- **World images**: All files matching `ref-images/world-*.jpg` are always included
- **Character images**: Files matching `ref-images/{character-code}-*.jpg` are included when that character appears
  - Example: For page `cu-ha-07.yaml`, includes `cu-*.jpg` and `ha-*.jpg`

Place your reference images in the `ref-images/` directory following this naming convention.

## Setup

1. Copy `.env.example` to `.env`
2. Add your API key:
   - `OPENAI_API_KEY` - For OpenAI backend
3. Add reference images to `ref-images/` directory (optional but recommended)

## Examples

```bash
# Generate a single page
uv run scripts/gen_image.py openai pages/cu-01.yaml

# Generate all pages with default settings (5 workers)
uv run scripts/gen_all_images.py

# Generate all pages with 10 concurrent workers
uv run scripts/gen_all_images.py --workers 10

# Test mode - show prompt without generating
uv run scripts/gen_image.py prompt pages/cu-ha-02.yaml
```

## Output Location

All generated images are saved to the `out-images/` directory and are git-ignored (not committed to the repository). Each user generates their own images using their API keys.
