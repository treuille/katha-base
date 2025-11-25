# Katha Base - Claude Context

This is a storybook generation system that creates AI-illustrated story pages.

## Project Architecture

The project follows a two-directory structure:

### lib/
The **library** contains reusable, abstract components that define how the system works:
- `scripts/` - Python scripts for generating images from story definitions
- `templates/` - YAML and prompt templates for structuring content

Think of this as the "engine" - it's story-agnostic and reusable.

### content/
The **content** directory contains story-specific material:
- `characters/` - Character definitions (one YAML file per character)
- `locations/` - Location and room definitions with haunting themes and whack assignments
- `story/template.yaml` - The 23-page story template shared across all 6 character books
- `ref-images/` - Reference images that define the visual style and character appearances
- `out-images/` - Generated illustrations (git-ignored, user-generated)

This is where the particular story lives - the actual content being illustrated.

**Story Structure**: All six main characters (Arthur, James, Cullan, Hansel, Emer, Henry) share the same 23-page narrative template. Each character experiences the same story beats but with personalized content based on their unique traits, rooms, and superpowers. The template defines page types (individual, pair, or joint), locations, and story beats for the hero's journey.

## Key Concepts

- **Reference Images**: Style guides (`style-*.jpg`) and character references (`cu-*.jpg`, etc.) that inform image generation
- **Generated Images**: AI-created illustrations based on story pages, saved to `content/out-images/`
- **Separation of Concerns**: `lib/` defines the system, `content/` defines the story

## Working with this Project

When making changes:
- System improvements (scripts, templates) go in `lib/`
- Story content (images, definitions) goes in `content/`
- Keep the separation clean to enable reuse across different stories
