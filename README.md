# katha-base

Modular storybook system for creating a set of interlocking storybooks for multiple children.

## Overview

Create interconnected children's stories where each character has their own book, and characters can meet at synchronized page numbers.

### Key Concepts

- Each character is defined in a YAML file with attributes and storylines
- Characters can share pages at the same page number across their books
- Story structure follows a 12-spread arc (see `templates/story-template.yaml`)
- All content is stored as YAML files with markdown text and image prompts

## Architecture

```
world.yaml (master: world lore + character links)
    ↓
characters/cc-name.yaml (each character = one storybook)
    ↓
pages/cc-pp.yaml (individual scenes, can be shared)
```

### Key Concept: Shared Pages

When characters meet, they share the SAME page at the SAME page number:
- Maya's book page 7 → `le-ma-07.yaml`
- Leo's book page 7 → `le-ma-07.yaml` (same file!)

## Getting Started

For each of these steps, just ask claude to do it for you, and it will prompt you to get all of the relevant information. (See `.claude/claude.md` to see the instructions which Claude will follow.)

1. Create all your characters (suggested to do this one at a time).
2. Create the world.
3. Bind characters together by creating shared interaction pages.
4. Create all pages for each character (one character at a time).
5. Show and critique each character's story to refine and improve it. You can say, for example, "Show me Cullan's story."

## Structure

- `world.yaml` - Master document: world lore, settings, character index, interaction map (copy from `templates/world-example.yaml`)
- `characters/` - Character files (each is a storybook with attributes + page list)
- `pages/` - Individual story pages (YAML with markdown content + image prompts)
- `templates/` - Example files that serve as both templates and schemas
- `scripts/` - Utility scripts for repository management
  - `pull-from-base.sh` - Safely pulls latest changes from katha-base to forked repositories
- `.claude/` - Project documentation

## File Naming

All lowercase with dashes:

- Characters: `ma-maya.yaml`, `le-leo.yaml`, `cu-cullan.yaml` (two-letter code + name)
- Solo pages: `ma-01.yaml`, `le-05.yaml`, `cu-01.yaml` (character code + page number)
- Shared pages: `cu-ma-07.yaml`, `le-ma-07.yaml` (character codes alphabetically + shared page number)

Templates serve as both examples and schemas:
- **World**: `templates/world-example.yaml` - World structure
- **Story Arc**: `templates/story-template.yaml` - **SOURCE OF TRUTH** for story structure (12 spreads with beats, hooks, payoffs)
- **Character**: `templates/character-example.yaml` - Character structure
- **Page**: `templates/page-example.yaml` - Individual page structure
