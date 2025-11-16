# Katha Multi-Book Project

## Project Overview

A modular storybook system for creating interconnected children's stories across multiple characters. Each character has their own storybook, and characters can share scenes at the same page numbers, creating an interlocking narrative web.

## Architecture

```
world.yaml (master document)
    ↓ links to
characters/cc-name.yaml (character attributes + page list)
    ↓ references
pages/cc-pp.yaml (individual story pages)
```

### Core Concept

- **World Document** (`world.yaml`): Master YAML file defining world lore, settings, challenges, and character interactions
- **Character Files** (`characters/`): Each character is their own storybook with attributes and an ordered page list
- **Page Files** (`pages/`): Individual scenes that can belong to one or multiple characters
- **Shared Pages**: When characters interact, they share a page at the same page number in both books

### File Naming

All filenames use lowercase with dashes:

- **World**: `world.yaml`
- **Characters**: `characters/cc-name.yaml` (e.g., `ma-maya.yaml`, `le-leo.yaml`, `cu-cullan.yaml`)
  - `cc` = two-letter character code (unique identifier)
  - `name` = character name in lowercase
- **Pages**: `pages/cc-pp.yaml` (e.g., `ma-01.yaml`, `le-05.yaml`, `cu-01.yaml`)
  - `cc` = two-letter character code
  - `pp` = two-digit page number
- **Shared Pages**: `pages/cc-cc-pp.yaml` (e.g., `cu-ma-07.yaml`, `le-ma-07.yaml`)
  - Character codes in alphabetical order
  - Same page number across all involved characters

## How It Works

### world.yaml - The Master Document

`world.yaml` is the central hub:
- Defines world lore, settings, rules, themes
- Links to all character files
- Maps character interactions (who appears together, at which page numbers)
- Does NOT contain detailed character attributes (those live in character files)

### Character Files - The Storybooks

Each character file in `characters/` is a complete storybook:
- Character attributes (name, age, appearance, personality, goals, etc.)
- Ordered list of pages for this character's narrative
- References to pages they appear in (both solo and shared)

Example: `characters/ma-maya.yaml` contains:
- Maya's profile
- Her page sequence: `ma-01`, `ma-02`, ..., `le-ma-07` (shared with Leo), `ma-08`, ...

### Page Files - The Scenes

Each page in `pages/` contains:
- Story content (markdown)
- Metadata (characters, setting, mood, plot points)
- Image prompt for illustrations
- Can be referenced by one or multiple character files

### The Shared Page Constraint

**Critical Rule**: When characters share a scene, they must be at the SAME page number.

Example:
- Maya's book page 7 → `le-ma-07.yaml`
- Leo's book page 7 → `le-ma-07.yaml` (same file!)

Both `characters/ma-maya.yaml` and `characters/le-leo.yaml` list this page at position 7.

## File Structure

```
katha-base/
├── world.yaml                 # Your world (copy from templates/world-example.yaml)
├── characters/
│   ├── ma-maya.yaml           # Maya's storybook
│   ├── le-leo.yaml            # Leo's storybook
│   ├── sa-sara.yaml           # Sara's storybook
│   └── cu-cullan.yaml         # Cullan's storybook
├── pages/
│   ├── ma-01.yaml             # Maya solo page 1
│   ├── le-01.yaml             # Leo solo page 1
│   ├── cu-01.yaml             # Cullan solo page 1
│   ├── le-ma-07.yaml          # Shared page (both at page 7)
│   └── ...
├── templates/
│   ├── world-example.yaml
│   ├── character-example.yaml
│   ├── story-template.yaml
│   └── page-template.yaml
└── .claude/
    └── claude.md              # This file
```

## Working with the Graph Structure

### How Claude Reads the Structure

When Claude needs to understand the narrative:

1. **Start at world.yaml**: See the big picture, character index, and interaction map
2. **Load character files**: Understand each character's arc and page sequence
3. **Read pages in order**: Follow the narrative by reading pages in sequence for each character
4. **Understand relationships**: See how shared pages connect different character narratives

### Example: Reading Maya's Story

```
1. Read world.yaml → see Maya's file is ma-maya.yaml, code "ma"
2. Read characters/ma-maya.yaml → get her attributes and page list
3. Read pages in order:
   - pages/ma-01.yaml (page 1, solo)
   - pages/ma-02.yaml (page 2, solo)
   - pages/le-ma-07.yaml (page 7, shared with Leo)
   - pages/ma-08.yaml (page 8, solo)
   - etc.
```

### Cross-Referencing

- Pages know which characters appear via `character_codes` field
- Character files list their full page sequence
- world.yaml maps all interactions
- No circular dependencies: world → characters → pages (one direction)

## Key Features

- **Modular and Reusable**: Same page can appear in multiple character books
- **Synchronized Interactions**: Characters share scenes at same page numbers
- **Character-Driven**: Each character is their own storybook
- **Graph Structure**: World links to characters, characters link to pages
- **Easy to Navigate**: Claude can traverse the graph to understand relationships
- **Flexible Narrative**: Mix solo and shared scenes for each character

## Templates

Templates serve as both examples and schemas, showing the structure with real example data:

- **World Template**: `templates/world-example.yaml` - Copy to `world.yaml` to create your world
- **Character Template**: `templates/character-example.yaml` - Complete example showing all fields with Cullan's data
- **Story Arc Template**: `templates/story-template.yaml` - **SOURCE OF TRUTH** for story structure: 12 spreads with beats, hooks, and payoffs
- **Page Template**: `templates/page-template.yaml` - Template for creating individual story pages
- Copy and fill in to create new content

### Story Structure

All stories follow the structure defined in `templates/story-template.yaml`:
- 12 spreads (24 pages) covering the complete story arc
- Each spread has: story beat, description, hook (anticipation), and payoff (next spread)
- Pages should match the beats, hooks, and payoffs described in the template
- This ensures consistent story structure across all character books

## Quick Reference

- **Master document**: `world.yaml` (at root level, copy from `templates/world-example.yaml`)
- **Story structure**: `templates/story-template.yaml` (SOURCE OF TRUTH - 12 spreads with beats, hooks, payoffs)
- **Character files**: `characters/cc-name.yaml` (see `templates/character-example.yaml` for structure)
- **Page files**: `pages/cc-pp.yaml` or `pages/cc-cc-pp.yaml` (see `templates/page-template.yaml` for structure)
- **Templates**: `templates/*.yaml` (example files that also serve as schemas)
