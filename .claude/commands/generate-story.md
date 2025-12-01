# Generate Story for a Character

You are generating story pages for a character's picture book.

## Context Files to Read First

**ALWAYS read these files first for context:**
1. @README.md - Project structure and organization
2. @story/overview.md - Story world, narrative architecture, and character details
3. @story/template.yaml - The shared page-by-page narrative template
4. @story/page-template.yaml - The structure/format for individual page files

## Task

1. **Ask the user which character** to generate pages for (arthur, cullan, emer, hansel, henry, or james)

2. **Ask if they want to overwrite existing pages** (default: no, skip existing)

3. **Read the character file** from @characters/{character_id}.yaml to understand:
   - Their pair partner
   - Their first and second attempt rooms
   - Their core strengths and traits
   - Their personality, dressing style, favorite genres, and favorite objects

4. **For each page in @story/template.yaml**, determine if this character appears:
   - **Joint pages**: All 6 children appear
   - **Pair pages**: Only the character and their designated pair partner appear
   - **Individual pages**: Only this character appears

5. **Generate page files** in `out/story/` with the naming convention:
   - **Always** use `p{number}-{char1}-{char2}-{...}.yaml` format
   - List ALL characters appearing on the page in **alphabetical order**, dash-separated
   - Examples: `p01-arthur-cullan-emer-hansel-henry-james.yaml`, `p09-arthur-cullan.yaml`, `p07-arthur.yaml`
   - **Note**: Only include the 6 main child characters in filenames (arthur, cullan, emer, hansel, henry, james), even if other characters like regan or dorje_legpa appear on the page

6. **For each page file**:
   - **Check if it already exists**
   - If it exists and overwrite=no: Print "⏭️ Skipping p{number} (already exists)" and continue
   - If it exists and overwrite=yes: Print "♻️ Regenerating p{number}" and proceed
   - If it doesn't exist: Print "✨ Creating p{number}" and proceed

7. **Copy the template structure** from @story/page-template.yaml to create each page, filling in:
   - Page metadata (id, section, page_type, characters, location, story_beat) from @story/template.yaml
   - **Write complete visual and text content** for each page based on the story_beat and character
   - Use symbolic room references from the character file (first_attempt_location, second_attempt_location)

8. **Writing Visual and Text Content**:
   - **Visual field**: Write 3-5 bullet points describing the single dramatic image for this page
     - Focus on composition, character actions, and key visual elements
     - DO NOT duplicate information from @story/template.yaml, @characters/, or @locations/ (that's added automatically by the image generator)
     - Frame a specific moment in time that matches the story_beat
   - **Text field**: Write the picture book text (maximum 50 words)
     - Write in third person for individual pages, focusing on the main character's experience
     - Include dialogue where appropriate (use quotes)
     - Match the tone and content to the story_beat and character's personality
   - **NEVER use TODO placeholders** - always write complete content

## Character Consistency

When filling in page content (especially visual descriptions), **hew as closely as possible** to each character's:
- **Personality traits** and core strengths
- **Dressing style** and typical clothing
- **Favorite genres** (books, games, activities)
- **Favorite objects** and possessions

**Pepper the story throughout** (especially visually) with hints and references to these character-specific details. Each page should feel authentic to who these children are.

## Summary

After completing, provide:
- Total pages that should exist for this character
- Number of pages created
- Number of pages skipped (already existed)
- List of all page files for this character
