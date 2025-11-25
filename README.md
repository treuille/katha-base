# Katha Base

A storybook generation system for creating illustrated story pages.

## Project Structure

```
katha-base/
├── lib/              # Reusable system components
│   ├── scripts/      # Image generation and processing scripts
│   └── templates/    # YAML templates and prompt templates
│
└── content/          # Story-specific content
    ├── characters/   # Character definitions (6 YAML files)
    ├── story/        # Story structure
    │   └── template.yaml  # 23-page narrative template
    ├── ref-images/   # Reference images for visual style
    └── out-images/   # Generated illustrations (git-ignored)
```

### lib/

Contains the abstract framework - scripts, templates, and tools that define how the storybook generation system works. These components are reusable across different stories.

### content/

Contains the particular content for your specific story:

- **characters/** - Definitions for all six main characters (Arthur, James, Cullan, Hansel, Emer, Henry), each with their unique traits, favorite toys, room assignments, and superpowers
- **story/template.yaml** - The shared 23-page narrative template that all six character books follow. Each character experiences the same story beats but with personalized content based on their unique characteristics
- **ref-images/** - Visual reference images for style and character appearances
- **out-images/** - Generated illustrations (not committed to repository)

## Story Template

The `content/story/template.yaml` file defines a 23-page narrative structure shared across all six character books. Each character's book follows the same template with:

- **Page types**: `individual` (solo character focus), `pair` (two characters), or `joint` (all characters together)
- **Story sections**: Ordinary World → First Whack → Crossover/Pair → Second Whack → Realizing the Bigger Problem → Climax → Carrying It Out → Resolution
- **Location modes**: Fixed locations or role-based (e.g., `first_whack_room` varies per character)

While the template is the same, each character's book personalizes the content based on their traits, rooms, and superpowers from their character definition.

## Setup

1. Copy `.env.example` to `.env` and add your API keys
2. Add reference images to `content/ref-images/`
3. Run generation scripts from `lib/scripts/`
