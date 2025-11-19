# Katha Multi-Book Project

## Project Overview

A modular storybook system for creating interconnected children's stories across multiple characters. Each character has their own storybook, and characters can share scenes at synchronized points in their stories, creating an interlocking narrative web.

## Important Scripts

**ALWAYS use these scripts** - they are the correct way to interact with the project:

1. **`scripts/show_story.py <character-code>`** - Display a character's complete story
   - Use this EVERY time you need to show a character's story
   - Never manually read and display pages - the script does it correctly
   - Example: `python3 scripts/show_story.py cu`

2. **`scripts/validate_structure.py`** - Validate repository structure and formatting
   - Run after creating/modifying characters or pages
   - Validates formatting, page existence, and constraints
   - Example: `python3 scripts/validate_structure.py`

## Steps

These are the various steps which the user can take to create / manipulate their
world

### Creating a New Character

1. Use `templates/character-example.yaml` as the template
2. Ask the user questions for each field in the template to create their character
3. Fill in all the answers in a new character file in `characters/`
4. **Important**: Set `story: []` (empty list) initially since no pages have been created yet
5. **Important**: Copy the script instructions from the template to the top of the new character file:
   ```yaml
   # To view this character's complete story, run:
   #   python3 scripts/show_story.py <character-code>
   #
   # If you encounter any issues with page formatting or consistency, run:
   #   python3 scripts/validate_structure.py
   ```
   Replace `<character-code>` with the actual two-letter character code.
6. **Do not leak any example data** from the template into the new character

### Creating the World

1. Use `templates/world-example.yaml` as the template
2. Ask the user questions for each field in the template to define their world
3. Fill in all the answers in `world.yaml` at the root level
4. **Do not leak any example data** from the template into the new world

### Binding Two Characters Together

**Important**: This step creates only ONE shared page where the characters meet. Do not create all the remaining pages for either character.

1. Ask the user which two characters should meet/interact
2. Ask about the nature of their interaction (what happens when they meet?)
3. Consult `templates/story-template.yaml` to determine which spread makes sense for them to meet
   - **Constraint**: Two characters CANNOT meet in:
     - Spread 1 - the first spread
     - Spread 11 - second to last spread
     - Spread 12 - final spread
   - Valid meeting spreads are: 2-10 (spreads 02-10 in file naming)
4. Determine the spread number where they'll meet (must be the same for both characters)
5. Check if the shared page already exists (use alphabetically ordered character codes: e.g., `cu-ma-07.yaml`)
6. If the page doesn't exist:
   - Create the shared page in `pages/` with proper naming (character codes alphabetically)
   - Use `templates/page-example.yaml` as the template
   - Write the page content so it makes narrative sense whether reading character A's story or character B's story
   - The text should work from both perspectives
   - **Text constraint**: Keep the `text` field to 2 sentences maximum
   - **Visual**: The `visual` field can be very long and detailed to convey the scene visually
     - **IMPORTANT**: Describe a SINGLE INSTANT IN TIME - not a sequence of actions
     - Describe WHAT is happening at this exact moment (action, poses, expressions)
     - Describe WHERE things are (positions, spatial relationships, background details)
     - Include specific visual details about the world, objects, and environment
     - Do NOT include stylistic suggestions (those come from world.yaml)
     - Do NOT describe multiple moments, sequences, or panels
7. Insert the page reference into both character files' `story:` lists at the correct position (in order)
   - **Format**: Use filename only with `.yaml` extension (e.g., `- cu-ma-07.yaml`)
   - **Do NOT** include the `pages/` folder prefix (e.g., NOT `- pages/cu-ma-07.yaml`)
8. **Important**: Both characters must reference the exact same page file at the same spread number
9. **Stop here**: Do not create any other pages for these characters at this time

### Creating All Pages for a Character

**Note**: This step should be done AFTER binding characters together, so that shared pages already exist and won't be duplicated.

**Important Constraints**:
- Pages are numbered 1-12 only (corresponding to the 12 spreads in the story template)
- Never create pages numbered less than 1 or more than 12
- Skip all joint/shared pages with other characters

1. Ask the user which character they want to create pages for

2. Load the character file from `characters/` to see which pages already exist in their `story:` list

3. **Read all joint pages with other characters**:
   - Identify which pages in the character's `story:` list are shared (filenames with multiple character codes)
   - For each shared page, read the page file from `pages/`
   - Note the spread number, description, visual, and text for each shared page
   - These are fixed anchor points that the story must connect

4. **Plan the story arc**:
   - Think about how to weave a coherent story that connects all the joint pages together
   - Consider the narrative flow: how does the character get from one joint page to the next?
   - The solo pages you create must bridge these joint pages into a single flowing narrative

5. **Create spreads 1-12**:
   - Go through spreads 1-12 sequentially
   - **Skip any spreads that are joint pages** (already created during binding)
   - For each page that needs to be created:
     - Use `templates/page-example.yaml` as the template
     - Determine which spread (1-12) the page belongs to based on `templates/story-template.yaml`
     - Copy the `beat`, `hook`, and `payoff` from the corresponding spread in the story template
     - Create a simple, bland `description` (1-2 sentences) for what happens on this page
     - Create a `visual` description based on the world defined in `world.yaml`
       - **Visual can be very long and detailed** to convey the scene richly
       - **IMPORTANT**: Describe a SINGLE INSTANT IN TIME - not a sequence of actions
       - Describe WHAT is happening at this exact moment (action, poses, expressions)
       - Describe WHERE things are (positions, spatial relationships, background details)
       - Include specific visual details about the world, objects, and environment
       - Do NOT include stylistic suggestions (those come from world.yaml)
       - Do NOT describe multiple moments, sequences, or panels
     - Create a `text` field with the actual page text
       - **Text must be 2 sentences maximum** - keep it super short and concise
     - Make sure the page flows naturally with the joint pages and overall story arc
     - Keep descriptions generic enough to be customized later
     - Save the page file in `pages/` with the naming convention `cc-pp.yaml` (e.g., `ma-01.yaml`, `cu-07.yaml`)

6. Update the character's `story:` list to include all newly created pages in sequential order (1-12), with joint pages in their correct positions
   - **Format**: Use filename only with `.yaml` extension (e.g., `- cu-01.yaml`, `- cu-ma-07.yaml`)
   - **Do NOT** include the `pages/` folder prefix (e.g., NOT `- pages/cu-01.yaml`)

### Validating Repository Structure

Before showing stories or making significant changes, you can run the structure validation script to validate that all pages are properly formatted:

```bash
python3 scripts/validate_structure.py
```

This script validates:
- At least one character exists
- Page references are properly formatted (filename.yaml without path prefix)
- All referenced pages exist
- Spreads 1, 11, and 12 are character-specific (no overlaps)
- No stray pages in the pages directory
- All page YAML files are valid
- Characters have 12 pages

The script provides color-coded output and exits with code 0 on success, 1 on failure.

**When to run this script:**
- After binding characters together
- After creating all pages for a character
- If you suspect formatting inconsistencies
- Before committing changes

### Showing and Critiquing a Character's Story

**IMPORTANT**: Always use the `show_story.py` script to display a character's story. This is the primary way to view and analyze stories. Never manually read and display all pages - the script handles this correctly.

This operation displays the complete story for a character, followed by a critique with improvement suggestions.

**Part 1: Display the Story**

1. Ask the user which character's story they want to see (or they may directly request "Show me [character]'s story")
2. **Always use the `show_story.py` script** to display the full story:
   ```bash
   python3 scripts/show_story.py <character-code>
   ```
   Examples:
   - `python3 scripts/show_story.py cu` for Cullan
   - `python3 scripts/show_story.py em` for Emer
   - `python3 scripts/show_story.py ha` for Hansel
3. The script will automatically display:
   - All pages in the character's story in order
   - Each page's description, visual, and text
   - Analysis of overlaps with other characters (showing before/after context from the other character's story)

**Part 2: Critique the Story**

After the script displays the story, automatically provide a critique:

1. **Check world consistency**:
   - Load `world.yaml`
   - Verify the story aligns with the world's settings, visual style, rules, and themes
   - Note any inconsistencies or missed opportunities to use world elements

2. **Check story structure alignment**:
   - Load `templates/story-template.yaml`
   - For each page, verify it matches the corresponding spread's `beat`, `hook`, and `payoff`
   - Identify any pages where the story structure isn't being followed properly

3. **For shared pages with other characters**:
   - The script output will show overlap analysis including before/after pages from other characters' stories
   - Use this information to understand cross-character constraints
   - Any suggested changes to shared pages must make sense in both characters' narrative arcs

4. **Generate three improvement suggestions**:
   - Each suggestion should specify:
     - Which page(s) to modify
     - What to change (description, visual, text, or beat alignment)
     - Why this improves the story
     - If it's a shared page, confirm the change works with the other character's before/after pages
   - Prioritize suggestions that:
     - Strengthen world consistency
     - Better align with story structure beats
     - Improve narrative flow and character development

5. **Present the critique** at the bottom of the output in this format:
   ```
   ---

   ## Story Critique for [Character Name]

   ### World Consistency
   [Analysis of how well the story aligns with world.yaml]

   ### Story Structure
   [Analysis of how well pages match story template beats]

   ### Shared Page Constraints
   [List any shared pages and note the before/after context from other characters]

   ### Three Suggestions for Improvement

   1. **[Page X]: [Brief title]**
      - What to change: [specific change]
      - Why: [rationale]
      - Constraints: [any shared page considerations]

   2. **[Page Y]: [Brief title]**
      ...

   3. **[Page Z]: [Brief title]**
      ...
   ```

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
- **Shared Pages**: When characters interact, they share a page at the same spread number in both books

### File Naming

All filenames use lowercase with dashes:

- **World**: `world.yaml`
- **Characters**: `characters/cc-name.yaml` (e.g., `ma-maya.yaml`, `le-leo.yaml`, `cu-cullan.yaml`)
  - `cc` = two-letter character code (unique identifier)
  - `name` = character name in lowercase
- **Pages**: `pages/cc-pp.yaml` (e.g., `ma-01.yaml`, `le-05.yaml`, `cu-01.yaml`)
  - `cc` = two-letter character code
  - `pp` = two-digit spread number (always two digits: 01, 02, ..., 12)
  - Note: Spread numbers are used for file naming, not actual book page numbers
- **Shared Pages**: `pages/cc-cc-pp.yaml` (e.g., `cu-ma-07.yaml`, `le-ma-07.yaml`)
  - Character codes in alphabetical order
  - Same spread number across all involved characters

**Important**: When referencing pages in character files' `story:` lists, use only the filename with `.yaml` extension (e.g., `- cu-01.yaml`), NOT the full path (NOT `- pages/cu-01.yaml`).

## How It Works

### world.yaml - The Master Document

`world.yaml` is the central hub:
- Defines world lore, settings, rules, themes
- Links to all character files
- Maps character interactions (who appears together, at which spread numbers)
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

**Critical Rule**: When characters share a scene, they must be at the SAME spread number.

Example:
- Maya's book spread 7 → `le-ma-07.yaml`
- Leo's book spread 7 → `le-ma-07.yaml` (same file!)

Both `characters/ma-maya.yaml` and `characters/le-leo.yaml` list this page at position 7 in their story lists.

## Image Generation

For generating AI illustrations for story pages, see the complete documentation in `docs/image-generation.md`. The script `scripts/gen_image.py` can generate images using various backends (OpenAI, Replicate, Ideogram).

Generated images are stored in the `out-images/` directory and are not committed to the repository.

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
│   └── page-example.yaml
├── docs/
│   └── image-generation.md    # Image generation documentation
├── scripts/
│   ├── gen_image.py           # Generate AI illustrations
│   ├── show_story.py          # Display character stories
│   ├── validate_structure.py  # Validate repository structure
│   └── pull-from-base.sh      # Pull updates from base repo
├── ref-images/                # Reference images for style (git-ignored except README)
├── out-images/                # Generated images (git-ignored)
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
- **Synchronized Interactions**: Characters share scenes at same spread numbers
- **Character-Driven**: Each character is their own storybook
- **Graph Structure**: World links to characters, characters link to pages
- **Easy to Navigate**: Claude can traverse the graph to understand relationships
- **Flexible Narrative**: Mix solo and shared scenes for each character

## Templates

Templates serve as both examples and schemas, showing the structure with real example data:

- **World Template**: `templates/world-example.yaml` - Copy to `world.yaml` to create your world
- **Character Template**: `templates/character-example.yaml` - Complete example showing all fields with Cullan's data
- **Story Arc Template**: `templates/story-template.yaml` - **SOURCE OF TRUTH** for story structure: 12 spreads with beats, hooks, and payoffs
- **Page Template**: `templates/page-example.yaml` - Template for creating individual story pages
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
- **Page files**: `pages/cc-pp.yaml` or `pages/cc-cc-pp.yaml` (see `templates/page-example.yaml` for structure)
- **Templates**: `templates/*.yaml` (example files that also serve as schemas)
