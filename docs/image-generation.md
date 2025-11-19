# Image Generation

Generate AI illustrations for storybook pages using the `gen_image.py` script.

## NEW STRUCTURE (Post-Refactor)

- Each page contains **2 images**
- Each image has its own visual description and text (2-3 sentences)
- By default, the script generates both images per page
- You can optionally generate a single image using `--image-num`

## Usage

### Generate All Images for a Page (2 images)

```bash
uv run scripts/gen_image.py <model-backend> <page-path>
```

### Generate a Specific Image (1 or 2)

```bash
uv run scripts/gen_image.py <model-backend> <page-path> --image-num <1|2>
```

### Generate All Pages in Parallel

```bash
uv run scripts/gen_all_images.py [--workers N] [--backend MODEL]
```

## Naming Convention

Generated images follow the format: `{page-id}-img{N}-{backend}.jpg`

Examples:
- `cu-01-1-img1-openai.jpg` - Cullan's spread 1, page 1, image 1
- `cu-01-1-img2-openai.jpg` - Cullan's spread 1, page 1, image 2
- `em-05-2-img1-openai.jpg` - Emer's spread 5, page 2, image 1
- `cu-ha-07-1-img1-openai.jpg` - Shared page with Cullan and Hansel

## Image Specifications

- **Model**: OpenAI gpt-image-1
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
   - Style reference images (style-*.jpg) for overall aesthetic
   - Character reference images (cu-*.jpg, em-*.jpg, etc.) for character appearance
2. **Visual Style** - Style description from `world.yaml`
3. **Character Visual Descriptions** - Physical descriptions from character YAML files
4. **Scene Illustration** - Visual description from the specific image's `visual` field
5. **Story Text** - 2-3 sentences embedded as readable typography

**Important**: Each generated image shows one moment in time (not panels or multiple scenes). Each page contains 2 sequential images that together tell a mini-story within that page.

## Reference Images

The script automatically includes reference images based on the page being generated:

- **Style images**: All files matching `ref-images/style-*.jpg` are always included
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
# Generate both images for a page (default behavior)
uv run scripts/gen_image.py openai pages/cu-01-1.yaml

# Generate only image 1 for a page
uv run scripts/gen_image.py openai pages/cu-01-1.yaml --image-num 1

# Generate only image 2 for a page
uv run scripts/gen_image.py openai pages/cu-01-1.yaml --image-num 2

# Generate all pages with default settings (5 workers)
uv run scripts/gen_all_images.py

# Generate all pages with 10 concurrent workers
uv run scripts/gen_all_images.py --workers 10

# Test mode - show prompt without generating
uv run scripts/gen_image.py prompt pages/cu-ha-02-1.yaml
```

## Output Location

All generated images are saved to the `out-images/` directory and are git-ignored (not committed to the repository). Each user generates their own images using their API keys.
