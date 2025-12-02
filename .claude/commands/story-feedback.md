---
description: Create a feedback markdown file for a character's story
---

# Create Story Feedback File

Create a feedback markdown file for collecting notes on a character's story pages.

## Instructions

1. **Ask the user which character(s)** they want to create a feedback file for (e.g., cullan, arthur, emer, hansel, henry, james)

2. **Find the latest version** by listing `out/versions/` and taking the highest number

3. **Find all story pages** by listing `out/story/p*.yaml`

4. **Create the feedback file** at the project root with this format:
   - Filename: `v{version}_feedback.md` (e.g., `v07_feedback.md`)
   - Structure:
     ```markdown
     # Story Feedback

     ## Metadata

     - version: `{version}`

     ## High level feedback

     ## Joint pages feedback

     ### p01-arthur-cullan-emer-hansel-henry-james
     ### p02-arthur-cullan-emer-hansel-henry-james
     ### p18-arthur-cullan-emer-hansel-henry-james
     ... (all joint pages with all 6 kids)

     ---

     ## Arthur

     ### p03-arthur
     ### p04-arthur
     ... (arthur's individual pages in order)
     ### p08-arthur-cullan
     ... (pair pages shown ONLY under first character alphabetically)
     ### p28-arthur

     ---

     ## Cullan

     ### p03-cullan
     ... (cullan's individual pages only - NO pair pages since arthur-cullan already shown above)
     ### p28-cullan

     ---

     ## Emer
     ... (emer's individual pages)
     ### p08-emer-henry
     ... (emer-henry pair pages shown here since emer comes first)

     ---

     ## Hansel
     ... (hansel's individual pages)
     ### p08-hansel-james
     ... (hansel-james pair pages shown here since hansel comes first)

     ---

     ## Henry
     ... (henry's individual pages only - NO pair pages)

     ---

     ## James
     ... (james's individual pages only - NO pair pages)
     ```

5. **Key rules:**
   - Joint pages (all 6 kids) go in their own section at the top
   - Individual pages go under each character
   - **Pair pages appear ONLY ONCE** under the first character alphabetically (e.g., arthur-cullan under Arthur, emer-henry under Emer, hansel-james under Hansel)
   - Pages within each section are sorted by page number

6. **Confirm creation** by showing the file path and number of pages included
