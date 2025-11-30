# Katha Base

A picture book generation system for creating illustrated story pages.

**For the complete story world, characters, and narrative details, see [story/overview.md](story/overview.md).**

## Project Structure

```
katha-base/
├── characters/      # Character definitions
├── locations/       # Location and room definitions
├── story/           # Story structure and narrative design
│   ├── template.yaml    # Shared narrative template
│   └── overview.md      # Story world and narrative overview
├── ref-images/      # Reference images for visual style
├── out-images/      # Generated illustrations (git-ignored)
├── deprecated/      # Archived old structure
└── .streamlit/      # Streamlit configuration and secrets
```

## Directory Overview

- **characters/** - Character definitions in YAML format
- **locations/** - Location and room definitions in YAML format
- **story/template.yaml** - Shared page-by-page narrative template structure
- **story/overview.md** - Complete story world description, narrative architecture, and character details
- **ref-images/** - Visual reference images for style and character appearances
- **out-images/** - Generated illustrations (not committed to repository)

## Setup

1. Copy `.env.example` to `.env` and add your API keys
2. Add reference images to `ref-images/`
3. Configure Google API key in `.streamlit/secrets.toml`
