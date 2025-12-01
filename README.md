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
│   ├── styles.yaml      # Visual style definitions
│   ├── styles-skip.yaml # Skipped/experimental styles
│   └── overview.md      # Story world and narrative overview
├── ref/                 # Reference images for visual style
│   ├── styles/          # Visual style reference images
│   ├── characters/      # Character reference images
│   ├── locations/       # Location reference images
│   └── objects/         # Object reference images
├── out/                 # Generated outputs (git-ignored)
│   ├── images/{style}/  # Generated illustrations by style
│   ├── books/{style}/   # Generated PDF books by style
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
  - **ref/styles/** - Visual style reference images (see Visual Styles section below)
  - **ref/characters/** - Character reference images
  - **ref/locations/** - Location reference images
  - **ref/objects/** - Object reference images
- **out/** - Generated outputs (not committed to repository)
  - **out/images/{style_id}/** - Generated illustrations organized by style
  - **out/books/{style_id}/** - Generated PDF books organized by style
  - **out/story/** - Generated story files

## Visual Styles

Style configuration is defined in `story/styles.yaml`, with reference images in `ref/styles/` using the naming convention `{style_id}-{##}.jpg`.

**Active styles** (in priority order):
1. `genealogy_witch` — **Benjamin Lacombe** — Genealogy of a Witch, Madame Butterfly
2. `red_tree` — **Shaun Tan** — The Red Tree
3. `gashlycrumb` — **Edward Gorey** — The Gashlycrumb Tinies
4. `donothing_day` — **Beatrice Alemagna** — On a Magical Do-Nothing Day
5. `ghost_hunt` — **Cherie Zamazing** — We're Going On A Ghost Hunt
6. `ghost_easy` — **Stephanie Laberis** — It's Not Easy Being A Ghost

Skipped/experimental styles are in `story/styles-skip.yaml`.

## Setup

1. Copy `.env.example` to `.env` and add your API keys
2. Add reference images to `ref/` subdirectories (`characters/`, `locations/`, `objects/`)
3. Configure Google API key in `.streamlit/secrets.toml`

## Image Generation

The `scripts/gen_image.py` script generates illustrations for story pages using AI image generation.

### Usage

```bash
uv run scripts/gen_image.py <mode> <file> [style_id]
```

**Modes:**
- `prompt <page_file> <style_id>` - Display the image generation prompt and list all referenced images
- `gemini <page_file> <style_id>` - Generate the image using gemini-3-pro-image-preview model
- `frame <image_file>` - Frame an existing image for print with bleed and guide lines

**Examples:**

```bash
# Show the prompt for a page in genealogy_witch style
uv run scripts/gen_image.py prompt out/story/p09-arthur-cullan.yaml genealogy_witch

# Generate an image in red_tree style
uv run scripts/gen_image.py gemini out/story/p09-arthur-cullan.yaml red_tree

# Frame a generated image for printing
uv run scripts/gen_image.py frame out/images/genealogy_witch/p09-arthur-cullan.jpg
```

### How it works

The script assembles a comprehensive image generation prompt by combining:

1. **Style prompts** from `story/styles.yaml` (artist-specific visual characteristics)
2. **Story setting** from `story/template.yaml` (house, Christmas atmosphere, etc.)
3. **Character visual descriptions** from each character's YAML file
4. **Location visual descriptions** from the location YAML file
5. **Page-specific scene description** from the page YAML file (`visual` field)
6. **Page text to display** from the page YAML file (`text` field)
7. **Reference images** from `ref/styles/`, `ref/characters/`, `ref/locations/`, and `ref/objects/`

### Output

- Generated images are saved to `out/images/{style_id}/{page_id}.jpg`
- Aspect ratio: 3:2 (closest to target ratio of 3507x2334 which is ~1.5)

### Requirements

- Copy `.env.example` to `.env` and set your `GEMINI_API_KEY` for image generation
- Reference images must follow naming convention: `{id}-{number}.jpg` (e.g., `arthur-01.jpg`, `genealogy_witch-02.jpg`)

## Book Generation

The `scripts/gen_book.py` script generates complete picture book PDFs for a character in a specific style.

### Usage

```bash
uv run scripts/gen_book.py <character_id> <style_id>
```

**Examples:**

```bash
# Generate Cullan's book in genealogy_witch style
uv run scripts/gen_book.py cullan genealogy_witch

# Generate books in parallel for multiple styles
uv run scripts/gen_book.py cullan genealogy_witch &
uv run scripts/gen_book.py cullan red_tree &
uv run scripts/gen_book.py cullan gashlycrumb &
```

### Output

- PDFs saved to: `out/books/{style_id}/{character}-{version}.pdf`
- Images saved to: `out/images/{style_id}/{page_id}.jpg`
