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
- **Image files**: Must be JPG format, use naming format `id-xx.jpg` where:
  - `id` is a multiple letter code, potentially with underscores (e.g., `play_room`, `dining_room`)
  - `xx` is a two-digit number with leading zero (e.g., `01`, `02`, not `1`, `2`)
  - Always use underscores for multi-word names, dash to separate the number
  - Examples: `arthur-01.jpg`, `dining_room-01.jpg`, `play_room-02.jpg`

### Working with Data Files

- **Character files** (`characters/*.yaml`): Define character attributes, attempt locations, pair partners
- **Location files** (`locations/*.yaml`): Define room behaviors and attempt sequences
- **Story template** (`story/template.yaml`): Defines page sequence, types, and story beats

### Key Patterns

- **Attempt locations**: Characters have `attempt_locations` array (first and second room assignments)
- **Location attempts**: Haunted rooms have `attempts` array with `character` and `summary` fields
- **Special locations**: `exterior.yaml` uses `release_lead_character`; `living_room.yaml` uses `climax_focus_character` (climax/finale scenes)

### Terminology

- Use "attempt" not "whack"
- Use "character" not "kid" in data structures (field names like `climax_focus_character`)
- Use "location" for rooms/places
- In narrative text (descriptions, summaries), informal terms like "kids" are acceptable and refer to the child characters
