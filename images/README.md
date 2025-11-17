# Generated Images

This directory contains AI-generated illustrations for storybook pages.

## How Images Are Generated

Images are created using the `gen_image.py` script:

```bash
uv run scripts/gen_image.py <model-backend> <page-path>
```

## Naming Convention

Generated images follow the format: `{page-id}-{backend}.jpg`

Examples:
- `cu-01-openai.jpg` - Cullan's first page generated with OpenAI DALL-E 3
- `em-05-replicate.jpg` - Emer's fifth page generated with Replicate SDXL
- `ha-12-ideogram.jpg` - Hansel's twelfth page generated with Ideogram v3

## Image Specifications

- **Aspect Ratio**: Wide format (2:1 or 3:1 depending on backend)
- **Format**: JPEG (.jpg)
- **Resolution**: Varies by backend
  - OpenAI: 1792x1024 (2:1 ratio)
  - Replicate: 1536x768 (2:1 ratio)
  - Ideogram: 3:1 ratio (backend-dependent resolution)

## Available Backends

- **openai** - OpenAI DALL-E 3
- **replicate** - Replicate IPAdapter Style SDXL
  - **Requires** `images/cu-01-openai.jpg` as a style reference
  - Applies the visual style from that reference image to all generations
  - Generate the reference image with OpenAI first before using Replicate
- **ideogram** - Ideogram v3
- **prompt** - Test mode (displays prompt without generating)

## What Gets Generated

Each image includes:
1. **World Visual Style** - Consistent aesthetic from `world.yaml`
2. **Scene Illustration** - Visual description from the page YAML file

## Notes

- This directory is git-ignored (except this README)
- Images are generated on-demand and not committed to the repository
- Each user generates their own images using their API keys
