# Katha Base - Claude Context

This is a picture book generation system that creates AI-illustrated story pages.

## Project Architecture

The project uses a flat, content-focused structure where all story elements live at the root level:

### Root Directory Structure
```
katha-base/
├── characters/      # Character definitions (one YAML per character)
├── locations/       # Location and room definitions
├── story/           # Story template and overview
├── ref-images/      # Visual style and character reference images
├── out-images/      # Generated illustrations (git-ignored)
├── deprecated/      # Archived lib/ structure (old system components)
└── .streamlit/      # Streamlit configuration and secrets
```

### Key Directories

- **characters/** - Definitions for all six main characters (Arthur, James, Cullan, Hansel, Emer, Henry), each with unique traits, favorite toys, room assignments, and superpowers
- **locations/** - Location and room definitions with haunting themes and attempt assignments
- **story/** - Contains `template.yaml` (the 23-page story template shared across all 6 character books) and `overview.md`
- **ref-images/** - Style guides (`style-*.jpg`) and character references (`cu-*.jpg`, etc.) that inform image generation
- **out-images/** - AI-created illustrations based on story pages (not committed to git)
- **deprecated/** - Old lib/ structure with previous scripts and templates (archived, not actively used)

**Story Structure**: All six main characters share the same 23-page narrative template. Each character experiences the same story beats but with personalized content based on their unique traits, rooms, and superpowers. The template defines page types (individual, pair, or joint), locations, and story beats for the hero's journey.

## Key Concepts

- **Reference Images**: Style guides and character references in `ref-images/` that inform AI image generation
- **Generated Images**: AI-created illustrations saved to `out-images/` (using Google Gemini Nano Banana Pro)
- **Flat Structure**: All story content is at the root level for easy access
- **Deprecated Code**: Old system components are preserved in `deprecated/` but not actively used

## Working with this Project

When making changes:
- Story content (characters, locations, templates) lives at root level
- Generated images go in `out-images/` (git-ignored)
- Old code is in `deprecated/` - don't modify unless migrating something back
