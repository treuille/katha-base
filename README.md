# katha-base

Modular storybook system for creating a set of interlocking storybooks for multiple children.

## Overview

Create interconnected children's stories where each character has their own book, and characters can meet at synchronized points in their stories.

### Key Concepts

- Each character is defined in a YAML file with attributes and storylines
- Characters can share pages at the same spread number across their books
- **Story structure:**
  - 12 spreads (a spread is both pages when you open a book)
  - 2 pages per spread (24 pages total per character)
  - 2 images per page (48 images total per character)
  - 2-3 sentences of text per image
- **Narrative node types:** Solo, Meeting, Mirrored, Resonant (see below)
- See `templates/story-template.yaml` for the complete story structure
- All content is stored as YAML files with markdown text and image prompts

### Narrative Node Types

The system supports four types of narrative nodes that define how story moments connect:

- **Solo (👤):** Single character's individual journey moment
- **Meeting (🤝):** Characters physically converge at the same place and time
  - Requires: location, shared action, dialogue, cross-book alignment metadata
- **Mirrored (🪞):** Characters face parallel challenges in different places; themes rhyme
  - Requires: shared theme, scenario variants, symbolic motif, spread alignment
- **Resonant (✨):** Emotional/energetic ripple connecting characters across distance
  - Requires: emotional state packets, ripple effect, symbolic resonance
  - Must follow a moment of character growth

## Architecture

```
world.yaml (master: world lore + character links)
    ↓
characters/cc-name.yaml (each character = one storybook)
    ↓
pages/cc-pp.yaml (individual scenes, can be shared)
```

### Key Concept: Shared Pages

When characters meet or have parallel moments, they share pages at the same spread:
- Maya's book spread 7, page 1 → `le-ma-07-1.yaml`
- Leo's book spread 7, page 1 → `le-ma-07-1.yaml` (same file!)

Each spread can contain different node types depending on the story beat (see `templates/story-template.yaml` for which node types are allowed per spread).

## Getting Started

For each of these steps, just ask claude to do it for you, and it will prompt you to get all of the relevant information. (See `.claude/claude.md` to see the instructions which Claude will follow.)

1. Create all your characters (suggested to do this one at a time).
2. Create the world.
3. Bind characters together by creating shared interaction pages.
4. Create all pages for each character (one character at a time).
5. Show and critique each character's story to refine and improve it. You can say, for example, "Show me Cullan's story."

## Viewing Stories and Testing Consistency

### View a Character's Complete Story

To view a character's complete story with overlap analysis:

```bash
python3 scripts/show_story.py <character-code>
```

Examples:
- `python3 scripts/show_story.py cu` - Shows Cullan's story
- `python3 scripts/show_story.py em` - Shows Emer's story
- `python3 scripts/show_story.py ha` - Shows Hansel's story

The script displays all pages in order, including description, visual, and text fields, plus an analysis of overlaps with other characters showing before/after context.

### Validate Repository Structure

To verify repository structure and that all pages are properly formatted:

```bash
python3 scripts/validate_structure.py
```

This validates:
- Page formatting (correct extensions, no path prefixes)
- All referenced pages exist
- Spreads 1, 11, and 12 are character-specific (no overlaps)
- No stray pages in the pages directory
- YAML validity
- Page structure (node types, images array, required fields)
- Node-specific metadata validation

The script exits with code 0 on success, 1 on failure, with color-coded error messages.

## Image Generation

Generate AI illustrations for story pages using the `gen_image.py` script. See [`docs/image-generation.md`](docs/image-generation.md) for complete documentation on setup, usage, and available backends.

## Structure

- `world.yaml` - Master document: world lore, settings, character index, interaction map (copy from `templates/world-example.yaml`)
- `characters/` - Character files (each is a storybook with attributes + page list)
- `pages/` - Individual story pages (YAML with markdown content + image prompts)
- `templates/` - Example files that serve as both templates and schemas
- `scripts/` - Utility scripts for repository management
  - `gen_image.py` - Generate illustrations for pages using AI models (generates 2 images per page; usage: `uv run scripts/gen_image.py <backend> <page-path> [--image-num 1|2]`)
  - `gen_all_images.py` - Generate illustrations for all pages in parallel (usage: `uv run scripts/gen_all_images.py [--workers N] [--backend MODEL]`)
  - `pull-from-base.sh` - Safely pulls latest changes from katha-base to forked repositories
  - `show_story.py` - Display a character's complete story with node types and images (usage: `python3 scripts/show_story.py <character-code>`)
  - `validate_structure.py` - Validate repository structure, node types, and image arrays (usage: `python3 scripts/validate_structure.py`)
- `docs/` - Additional documentation
  - `image-generation.md` - Complete guide to generating AI illustrations for storybook pages
- `ref-images/` - Reference images for style consistency (git-ignored except README)
- `.claude/` - Project documentation

## File Naming

All lowercase with dashes:

- Characters: `ma-maya.yaml`, `le-leo.yaml`, `cu-cullan.yaml` (two-letter code + name)
- Solo pages: `ma-01-1.yaml`, `le-05-2.yaml`, `cu-01-1.yaml` (character code + spread number 01-12 + page number 1-2)
- Shared pages: `cu-ma-07-1.yaml`, `le-ma-07-2.yaml` (character codes alphabetically + spread number + page number)
- Image output: `cu-01-1-img1-openai.jpg`, `cu-01-1-img2-openai.jpg` (page ID + image number + backend)

Templates serve as both examples and schemas:
- **World**: `templates/world-example.yaml` - World structure
- **Story Arc**: `templates/story-template.yaml` - **SOURCE OF TRUTH** for story structure (12 spreads with beats, hooks, payoffs)
- **Character**: `templates/character-example.yaml` - Character structure
- **Page**: `templates/page-example.yaml` - Individual page structure
