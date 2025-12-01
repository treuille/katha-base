# Katha Base - Claude Context

**For project structure:** See [README.md](../README.md)
**For story world and narrative details:** See [story/overview.md](../story/overview.md)

## Coding Conventions

### Python Execution

- **Always use `uv run`**: All Python commands must be executed with `uv run python` or `uv run python3`
- **Package management**: Use `uv add` to add new dependencies to the project

### File Organization

- **YAML files**: Character and location definitions use YAML format
- **Flat structure**: All story content lives at root level (characters/, locations/, story/)
- **Generated content**: AI-created content goes in `out/` (git-ignored) - images in `out/images/`, stories in `out/story/`
- **Reference images**: Visual references in `ref/` organized by type (characters/, locations/, objects/)
- **Deprecated code**: Old system components in `deprecated/` - don't modify unless migrating back
- **Empty directories**: Use `.gitkeep` files to preserve empty directories in git (e.g., `ref/.gitkeep`, `out/images/.gitkeep`)

### File Naming Conventions

- **YAML files**: Use format `id.yaml` where `id` is a multiple letter code, potentially with underscores
  - Examples: `arthur.yaml`, `dining_room.yaml`, `sun_room.yaml`
- **Page files** (`out/story/*.yaml`): Use format `p{number}-{char1}-{char2}-{...}.yaml` where:
  - `{number}` is a two-digit page number (e.g., `01`, `02`, `24`)
  - Characters are listed in **alphabetical order**, dash-separated
  - **Only include the 6 main child characters** (arthur, cullan, emer, hansel, henry, james) in filenames, even if other characters like regan or dorje_legpa appear on the page
  - Examples: `p01-arthur-cullan-emer-hansel-henry-james.yaml`, `p09-arthur-cullan.yaml`, `p07-arthur.yaml`
- **Image files**: Must be JPG format, use naming format `{id}-{xx}.jpg` where:
  - `{id}` matches the YAML filename exactly (e.g., `arthur`, `dorje_legpa`, `dining_room`)
  - `{xx}` is a two-digit number with leading zero (e.g., `01`, `02`, not `1`, `2`)
  - The dash (`-`) is ONLY used as the separator before the number
  - Underscores in IDs are preserved (this allows unambiguous parsing: everything before the last `-` is the ID)
  - Examples: `arthur-01.jpg`, `dorje_legpa-01.jpg`, `dining_room-02.jpg`

### Working with Data Files

- **Character files** (`characters/*.yaml`): Define character attributes, attempt locations, pair partners
- **Location files** (`locations/*.yaml`): Define room behaviors and attempt sequences
- **Story template** (`story/template.yaml`): Defines page sequence, types, and story beats
- **Page files** (`out/story/*.yaml`): Individual page definitions with visual and text content
  - **Visual field**: 3-5 bullet points describing the scene composition (DO NOT duplicate info from template/characters/locations)
  - **Text field**: Picture book text, maximum 50 words, matches story_beat
  - **NEVER use TODO placeholders** - always write complete content

### Key Patterns

- **Attempt locations**: Characters have `attempt_locations` array (first and second room assignments)
- **Location attempts**: Haunted rooms have `attempts` array with `character` and `summary` fields
- **Special locations**: `exterior.yaml` uses `release_lead_character`; `living_room.yaml` uses `climax_focus_character` (climax/finale scenes)

### Terminology

- Use "attempt" not "whack"
- Use "character" not "kid" in data structures (field names like `climax_focus_character`)
- Use "location" for rooms/places
- In narrative text (descriptions, summaries), informal terms like "kids" are acceptable and refer to the child characters

### Documentation Practices

- **Avoid explicit counts**: Don't write "Eight characters" or "Six rooms" - these numbers become stale when content changes. Use general terms like "Characters inhabiting this world:" instead.
- **Deduplicate information**: Don't repeat the same information across multiple files. Reference authoritative sources (e.g., "see `characters/*.yaml`") rather than duplicating lists.
- **Single source of truth**: Character details live in `characters/*.yaml`, location details in `locations/*.yaml`, story structure in `story/template.yaml`.

### Error Handling

- **Let exceptions propagate**: Do not use try/catch blocks unless the catch is part of the logical flow of the program. Let exceptions flow out naturally so they can be handled usefully by agentic callers or surface clearly in logs.
- **Raise, don't print-and-exit**: Use `raise RuntimeError(...)` or `raise ValueError(...)` instead of `print("Error: ..."); sys.exit(1)`. This makes functions composable and testable.
- **Return values, don't assume paths**: Functions that create files should return the path to the created file, not just print it. Callers should use the returned path rather than reconstructing it.

## Scripts

### Image Generation (`scripts/gen_image.py`)

Generates illustrations for story pages using AI image generation with reference images.

**Basic Usage:**
```bash
uv run scripts/gen_image.py [mode] <page_file>
```

**Modes:**
- `prompt` - Display the complete image generation prompt and list all referenced images (useful for debugging/review)
- `gemini` - Generate the actual image using gemini-3-pro-image-preview model
- `frame` - Frame an existing image for print with bleed area and guide lines

**Examples:**
```bash
# Preview the prompt for page 09
uv run scripts/gen_image.py prompt out/story/p09-arthur-cullan.yaml

# Generate the image for page 09
uv run scripts/gen_image.py gemini out/story/p09-arthur-cullan.yaml

# Frame a generated image for printing
uv run scripts/gen_image.py frame out/images/p09-arthur-cullan.jpg
```

**How the Prompt is Assembled:**

The script automatically builds a comprehensive prompt by combining:

1. **Visual style** from `story/template.yaml` (`visual` field)
2. **Character visual descriptions** from `characters/{character_id}.yaml` (`visual` field)
3. **Location visual descriptions** from `locations/{location_id}.yaml` (`visual` field)
4. **Page-specific scene** from the page YAML file (`visual` field)
5. **Page text to display** from the page YAML file (`text` field) - with explicit instructions to render in image
6. **Reference images** - automatically discovers and includes all matching images:
   - Style images: `ref/styles/{style_id}-*.jpg` (always included first)
   - Character images: `ref/characters/{character_id}-*.jpg`
   - Location images: `ref/locations/{location_id}-*.jpg`
   - Object images: `ref/objects/{object_id}-*.jpg`

**Reference Image Labeling:**

Images are labeled in the prompt using a common prompt engineering pattern:
```
I have provided 11 reference images:

Image 1: A style reference image showing the illustration style
Image 2: A style reference image showing the illustration style
Image 3: A reference picture of Arthur
Image 4: A reference picture of Arthur
Image 5: A reference picture of Cullan
Image 6: A reference picture of the Hallway
...
```

**Output:**
- Generated images saved to: `out/images/{page_id}.jpg`
- Aspect ratio: 3:2 (maintains ~1.5 ratio, close to target 3507x2334)
- Framed images saved to: `out/images/{page_id}-framed.jpg`

**Print Dimensions (frame mode):**
- Content area: 3507×2334 pixels
- Full size (with bleed): 3579×2406 pixels
- Bleed: 36 pixels on all sides
- Center gutter: 1789 pixels (for two-page spread fold)
- Guide lines drawn in light gray for margins and center gutter

**Requirements:**
- Copy `.env.example` to `.env` and set your `GEMINI_API_KEY` (for gemini mode)
- Reference images must exist in `ref/` subdirectories
- Image naming: `{id}-{number}.jpg` (e.g., `arthur-01.jpg`, `dorje_legpa-01.jpg`, `hallway-02.jpg`)

