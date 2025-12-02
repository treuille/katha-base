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
│   ├── page-template.yaml # Template for individual page files
│   ├── styles.yaml      # Visual style definitions
│   ├── styles-skip.yaml # Skipped/experimental styles
│   └── overview.md      # Story world and narrative overview
├── ref/                 # Reference images for visual style
│   ├── styles/          # Visual style reference images
│   ├── characters/      # Character reference images
│   ├── locations/       # Location reference images
│   └── objects/         # Object reference images
├── out/                 # Generated outputs (git-ignored)
│   ├── images/          # Shared image storage (reused across versions)
│   │   ├── *.txt        # Prompt text files ({page_stem}-{hash}.txt)
│   │   └── *.jpg        # Generated images ({page_stem}-{hash}.jpg)
│   ├── versions/        # Versioned output folders
│   │   └── {xx}/        # Version folders (01/, 02/, etc.)
│   │       ├── *-book.pdf
│   │       └── manifest.yaml
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
  - **out/images/** - Shared storage for prompts and images (reused across versions)
    - Prompts: `{page_stem}-{prompt_hash}.txt`
    - Images: `{page_stem}-{prompt_hash}.jpg` (raw, unframed)
  - **out/versions/{xx}/** - Versioned output folders (e.g., `out/versions/01/`)
    - Books: `{character}-book.pdf`
    - `manifest.yaml` with version metadata (references images in `out/images/`)
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

1. Install Google Cloud SDK: `curl https://sdk.cloud.google.com | bash`
2. Authenticate: `gcloud auth application-default login`
3. Set quota project: `gcloud auth application-default set-quota-project <PROJECT_ID>`
4. Add reference images to `ref/` subdirectories (`characters/`, `locations/`, `objects/`)

## Image Generation

The `scripts/gen_image.py` script generates illustrations for story pages using AI image generation.

### Usage

```bash
uv run scripts/gen_image.py <mode> <file> [style_id]
```

**Modes:**
- `prompt <page_file> <style_id>` - Display the image generation prompt and list all referenced images
- `gemini <page_file> <style_id>` - Generate the image using Gemini
- `frame <image_file>` - Frame an existing image for print with bleed and guide lines

**Examples:**

```bash
# Show the prompt for a page in genealogy_witch style
uv run scripts/gen_image.py prompt out/story/p09-arthur-cullan.yaml genealogy_witch

# Generate an image in red_tree style
uv run scripts/gen_image.py gemini out/story/p09-arthur-cullan.yaml red_tree

# Frame a generated image for printing (legacy - framing now happens during PDF creation)
uv run scripts/gen_image.py frame out/images/p09-arthur-cullan-a1b2c.jpg
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

- Generated images are saved to `out/images/{page_stem}-{prompt_hash}.jpg`
- Prompt text saved to `out/images/{page_stem}-{prompt_hash}.txt`
- Aspect ratio: 3:2 (closest to target ratio of 3507x2334 which is ~1.5)
- Images are stored raw (unframed); framing happens during PDF creation
- Images are shared across versions (same prompt hash = same image)

### Requirements

- Authenticate with Google Cloud: `gcloud auth application-default login`
- Set quota project: `gcloud auth application-default set-quota-project <PROJECT_ID>`
- Reference images must follow naming convention: `{id}-{number}.jpg` (e.g., `arthur-01.jpg`, `genealogy_witch-02.jpg`)

## Book Generation

The `scripts/gen_book.py` script generates complete picture book PDFs for a character.

### Usage

```bash
uv run scripts/gen_book.py <character_id> [--style STYLE] [--message MESSAGE]
```

**Options:**
- `--style STYLE` - Visual style to use (default: from `story/template.yaml`)
- `--message MESSAGE` - Required when creating a new version (prompts changed)

**Examples:**

```bash
# Generate Cullan's book (uses existing version if prompts unchanged)
uv run scripts/gen_book.py cullan

# Create a new version with a message
uv run scripts/gen_book.py cullan --message "Updated story text"

# Generate Arthur's book in a specific style
uv run scripts/gen_book.py arthur --style red_tree
```

### Versioning

The script automatically detects when prompts have changed:
- **Prompts unchanged**: Uses existing version, skips already-generated images
- **Prompts changed**: Requires `--message` flag to create a new version

This enables:
- **Crash recovery**: Re-run to resume interrupted generations
- **Idempotent runs**: Same prompt = same image (skipped if exists)
- **Joint page efficiency**: Generating one character's book also generates shared pages

### Output

- PDFs saved to: `out/versions/{xx}/{character}-book.pdf`
- Images saved to: `out/images/{page_stem}-{prompt_hash}.jpg` (shared across versions)
- Prompts saved to: `out/images/{page_stem}-{prompt_hash}.txt`
- Manifest: `out/versions/{xx}/manifest.yaml` (tracks metadata, git commit, style, references to shared images)
