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

     ## Pages

     ### p01-arthur-cullan-emer-hansel-henry-james
     ### p02-arthur-cullan-emer-hansel-henry-james
     ### p03-arthur
     ### p03-cullan
     ... (all pages in page number order)
     ### p30-arthur-cullan-emer-hansel-henry-james
     ```

5. **Key rules:**
   - List all pages in page number order
   - Include all page types (joint, pair, individual) together in sequence

6. **Confirm creation** by showing the file path and number of pages included
