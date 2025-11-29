# Katha Base

A picture book generation system for creating illustrated story pages.

## Project Structure

```
katha-base/
├── characters/      # Character definitions (6 YAML files)
├── locations/       # Location and room definitions (8 YAML files)
├── story/           # Story structure
│   ├── template.yaml    # 23-page narrative template
│   └── overview.md      # Story overview and details
├── ref-images/      # Reference images for visual style
├── out-images/      # Generated illustrations (git-ignored)
├── deprecated/      # Old lib/ structure (archived)
└── .streamlit/      # Streamlit configuration and secrets
```

## Story Content

- **characters/** - Definitions for all six main characters, each with their unique traits, favorite toys, room assignments, and superpowers
- **locations/** - Definitions for all locations and rooms, each with haunting themes, descriptions, and first/second whack assignments
- **story/template.yaml** - The shared 23-page narrative template that all six character books follow. Each character experiences the same story beats but with personalized content based on their unique characteristics
- **ref-images/** - Visual reference images for style and character appearances
- **out-images/** - Generated illustrations (not committed to repository)

## Story Template

The `story/template.yaml` file defines a 23-page narrative structure shared across all six character books. Each character's book follows the same template with:

- **Page types**: `individual` (solo character focus), `pair` (two characters), or `joint` (all characters together)
- **Story sections**: Ordinary World → First Whack → Crossover/Pair → Second Whack → Realizing the Bigger Problem → Climax → Carrying It Out → Resolution
- **Location modes**: Fixed locations or role-based (e.g., `first_whack_room` varies per character)

While the template is the same, each character's book personalizes the content based on their traits, rooms, and superpowers from their character definition.

## Setup

1. Copy `.env.example` to `.env` and add your API keys
2. Add reference images to `ref-images/`
3. Configure Google API key in `.streamlit/secrets.toml`
