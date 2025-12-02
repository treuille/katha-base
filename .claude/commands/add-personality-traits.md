---
description: Add visual easter eggs based on character personality traits to story pages
---

# Add Personality Traits Easter Eggs

Add subtle visual easter eggs to a character's story pages that reflect their personality, interests, and traits.

## Instructions

1. **Ask the user which character** they want to add personality easter eggs for:
   - arthur, cullan, emer, hansel, henry, or james

2. **Read the character file** from `characters/{character}.yaml` to understand:
   - Their `summary` (personality traits, interests, hobbies)
   - Their `favorite_toys`
   - Their `favorite_genres`
   - Their `superpower`
   - Any other defining characteristics

3. **Find all story pages** for that character by listing `out/story/p*.yaml` and filtering for files that include the character name. This includes:
   - **Individual pages** (only this character, e.g., `p03-cullan.yaml`)
   - **Pair pages** (this character + partner, e.g., `p08-arthur-cullan.yaml`)
   - **Joint pages** (all 6 kids, e.g., `p01-arthur-cullan-emer-hansel-henry-james.yaml`)

4. **For each page in page number order:**

   a. Read the current page content (story_beat, visual, text)

   b. Analyze what subtle visual easter eggs could be added that:
      - Reflect the character's personality traits or interests
      - Are subtle background details, not main focus
      - Fit naturally into the scene without forcing
      - Add depth for observant readers who know the character
      - Could be items, decorations, poses, expressions, background objects, etc.

   c. **Present ONE suggestion at a time** to the user with:
      - The page ID (e.g., p03-cullan)
      - The current visual field content
      - Your proposed easter egg addition
      - Brief explanation of why it relates to the character's personality

   d. **Wait for explicit user approval** before making any change:
      - If approved: Edit the page's visual field to add the easter egg
      - If rejected: Move on to the next page without changes
      - User can also provide modifications to the suggestion

   e. **Only proceed to the next page after current page is resolved**

5. **Easter egg ideas to consider** (based on character traits):
   - Favorite toys/items visible in background
   - Books or media related to their interests
   - Subtle poses or expressions that reflect personality
   - Background decorations matching their hobbies
   - Items from their attempt_locations appearing
   - Visual callbacks to their superpower theme
   - Objects related to their favorite_genres

6. **Important rules:**
   - NEVER add an easter egg without explicit approval
   - Present suggestions ONE AT A TIME
   - Wait for user response before moving to next page
   - Keep easter eggs subtle - they're background details, not the focus
   - Don't suggest easter eggs that would contradict the existing visual
   - Skip pages that already have good personality-related easter eggs

7. **When finished**, summarize:
   - Total pages reviewed
   - Number of easter eggs added
   - Brief list of what was added where
