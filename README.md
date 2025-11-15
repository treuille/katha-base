# katha-base

Modular storybook system for creating a set of interlocking storybooks for multiple children.

## Overview

Create interconnected children's stories where each character has their own book, and characters can meet at synchronized page numbers. The system allows for:

1. Defining characters with attributes and storylines
2. Mapping character interactions (who meets whom, at which page numbers)
3. Generating pages automatically using AI (with story text and image prompts)
4. Iterating on the complete narrative web all at once

## Architecture

```
world.md (master: world lore + character links)
    ↓
characters/cc-name.yaml (each character = one storybook)
    ↓
pages/cc-pp.yaml (individual scenes, can be shared)
```

### Key Concept: Shared Pages

When characters meet, they share the SAME page at the SAME page number:
- Maya's book page 7 → `le-ma-07.yaml`
- Leo's book page 7 → `le-ma-07.yaml` (same file!)

## Structure

- `world.md` - Master document: world lore, settings, character index, interaction map
- `characters/` - Character files (each is a storybook with attributes + page list)
- `pages/` - Individual story pages (YAML with markdown content + image prompts)
- `docs/*-schema.md` - Structure documentation and validation rules
- `templates/` - Templates for characters and pages
- `.claude/` - Project instructions and slash commands

## File Naming

All lowercase with dashes:

- Characters: `ma-maya.yaml`, `le-leo.yaml`, `cu-cullan.yaml` (two-letter code + name)
- Solo pages: `ma-01.yaml`, `le-05.yaml`, `cu-01.yaml` (character code + page number)
- Shared pages: `cu-ma-07.yaml`, `le-ma-07.yaml` (character codes alphabetically + shared page number)

## Workflow

1. **Define the world** - Edit `world.md` with settings, themes, and lore
2. **Create characters** - Use `/new-character` to add characters to `characters/`
3. **Map interactions** - In `world.md`, plan which characters meet at which pages
4. **Generate pages** - Use `/create-all-pages` to create all story pages at once
5. **Iterate** - Edit pages and characters, regenerate as needed

## Getting Started

1. Fill out `world.md` with your world details
2. Create character files using `/new-character`
3. Add character interaction mapping to `world.md`
4. Run `/create-all-pages` to generate all page files
5. Review and refine the generated content

## Documentation

See `.claude/claude.md` for detailed architecture and workflow instructions.

- Character schema: `docs/character-schema.md`
- Page schema: `docs/page-schema.md`
- Templates: `templates/`

## Commands

- `/new-character` - Create a new character file
- `/new-page` - Create a single page manually
- `/create-all-pages` - Generate all pages from character interaction map
