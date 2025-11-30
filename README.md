# Katha Base

A picture book generation system for creating illustrated story pages.

**For the complete story world, characters, and narrative details, see [story/overview.md](story/overview.md).**

## Project Structure

```
katha-base/
├── characters/          # Character definitions
├── locations/           # Location and room definitions
├── story/               # Story structure and narrative design
│   ├── template.yaml    # Shared narrative template
│   └── overview.md      # Story world and narrative overview
├── ref/                 # Reference images for visual style
│   ├── characters/      # Character reference images
│   ├── locations/       # Location reference images
│   └── objects/         # Object reference images
├── out/                 # Generated outputs (git-ignored)
│   ├── images/          # Generated illustrations
│   └── story/           # Generated story files
├── deprecated/          # Archived old structure
└── .streamlit/          # Streamlit configuration and secrets
```

## Directory Overview

- **characters/** - Character definitions in YAML format
- **locations/** - Location and room definitions in YAML format
- **story/template.yaml** - Shared page-by-page narrative template structure
- **story/overview.md** - Complete story world description, narrative architecture, and character details
- **ref/** - Visual reference images for style and character appearances (JPG format, named as `name-##.jpg`)
  - **ref/characters/** - Character reference images
  - **ref/locations/** - Location reference images
  - **ref/objects/** - Object reference images
- **out/** - Generated outputs (not committed to repository)
  - **out/images/** - Generated illustrations
  - **out/story/** - Generated story files

## Setup

1. Copy `.env.example` to `.env` and add your API keys
2. Add reference images to `ref/` subdirectories (`characters/`, `locations/`, `objects/`)
3. Configure Google API key in `.streamlit/secrets.toml`

## Image Generation

The `scripts/gen_image.py` script generates illustrations for story pages using AI image generation.

### Usage

```bash
uv run scripts/gen_image.py [mode] <page_file>
```

**Modes:**
- `prompt` - Display the image generation prompt and list all referenced images
- `gemini` - Generate the image using gemini-3-pro-image-preview model

**Examples:**

```bash
# Show the prompt for a page
uv run scripts/gen_image.py prompt out/story/p09-arthur-cullan.yaml

# Generate an image using Gemini
uv run scripts/gen_image.py gemini out/story/p09-arthur-cullan.yaml
```

### How it works

The script assembles a comprehensive image generation prompt by combining:

1. **Overall visual style** from `story/template.yaml`
2. **Character visual descriptions** from each character's YAML file (e.g., `characters/arthur.yaml`)
3. **Location visual descriptions** from the location YAML file (e.g., `locations/hallway.yaml`)
4. **Page-specific scene description** from the page YAML file
5. **Reference images** from `ref/style/`, `ref/characters/`, `ref/locations/`, and `ref/objects/`

The script automatically finds all reference images matching the characters, locations, and objects in the page, and includes them in the prompt with proper labeling. Style reference images are always included first to establish the overall illustration style.

### Output

- Generated images are saved to `out/images/{page_id}.jpg`
- Aspect ratio: 3:2 (closest to target ratio of 3507x2334 which is ~1.5)

### Requirements

- Copy `.env.example` to `.env` and set your `GEMINI_API_KEY` for image generation
- Reference images must follow naming convention: `{id}-{number}.jpg` (e.g., `arthur-01.jpg`, `hallway-02.jpg`)
