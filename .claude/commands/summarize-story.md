---
description: Summarize a character's story as a narrative to a markdown file
---

# Summarize Story for a Character

Create a natural language narrative summary of a character's story journey.

## Instructions

1. **Ask the user which character** they want to summarize:
   - arthur, cullan, emer, hansel, henry, or james

2. **Find all story pages** for that character by listing `out/story/p*.yaml` and filtering for files that include the character name

3. **Read each page file** in page number order, categorizing them as:
   - **Individual pages** (only this character) - PRIMARY FOCUS
   - **Pair pages** (this character + their partner) - PRIMARY FOCUS
   - **Joint pages** (all 6 kids) - minimal focus, just for context

4. **Write a narrative summary** that:
   - Tells the character's story in natural, flowing prose (3-5 paragraphs)
   - Focuses heavily on their individual journey and pair interactions
   - Only briefly mentions joint scenes for context where needed
   - Captures the emotional arc and key moments
   - Highlights their unique personality, strengths, and growth

5. **Create the summary file** at the project root:
   - Filename: `{character_name}_summary.md` (e.g., `cullan_summary.md`)
   - Structure:
     ```markdown
     # {Character Name}'s Story

     {3-5 paragraphs of narrative summary telling their story naturally}
     ```

6. **Confirm creation** by showing:
   - The file path created
   - A brief note that the summary is ready for review
