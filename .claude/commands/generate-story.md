# Generate Story for a Character

You are generating story pages for a character's picture book. This is a **three-phase process**: gather requirements, reason deeply about the story, then generate pages.

---

## Phase 1: Gather Requirements

**Ask the user these questions before proceeding:**

1. **Which character?** (arthur, cullan, emer, hansel, henry, or james)

2. **Overwrite existing pages?** (default: no, skip existing files)

**Wait for user responses before continuing to Phase 2.**

---

## Phase 2: Research & Story Reasoning

### 2.1 Read All Context Files

Read these files to understand the world and structure:
- @README.md - Project structure
- @story/overview.md - Story world, narrative architecture, themes
- @story/template.yaml - The shared page-by-page narrative template
- @story/page-template.yaml - Output format for individual pages

### 2.2 Read Character-Specific Files

Read the character file from @characters/{character_id}.yaml to understand:
- Their **pair partner** (who they swap rooms with)
- Their **first and second attempt rooms**
- Their **core strength** (what makes them the hero of their room)
- Their **personality traits**, dressing style, favorite genres, favorite objects

### 2.3 Read All Existing Pages for This Character

Check `out/story/` for any existing page files that include this character. Read them all to understand:
- What has already been established (continuity constraints)
- The voice and tone already set
- Any specific details or callbacks to preserve

### 2.4 Deep Story Reasoning

Now **reason extensively** about what will make this character's story compelling. Consider:

**Narrative Flow:**
- What makes each page want to lead to the next page?
- Where are the moments of tension, mystery, and release?
- How does the pacing build from "something feels off" to "full confrontation"?

**Character Arc:**
- How does this child's **core strength** emerge gradually?
- What's their moment of doubt? Their breakthrough moment?
- How do they change from page 1 to the epilogue?

**Character Authenticity:**
- How can their **favorite objects** appear naturally in scenes?
- How does their **dressing style** inform what we see?
- What **genre references** (from their favorite genres) could enrich their scenes?
- What small behavioral details reveal their **personality**?

**The Two-Attempts Pattern:**
- First attempt: They try a simple fix in the "wrong" room. It partially works but reveals their limitation.
- Second attempt: In "their" room, they see the deeper pattern and use their true strength.
- How do we make the difference between these two feel meaningful and earned?

**Pair Dynamic:**
- What makes the crossover scene between this child and their pair partner feel like a genuine exchange?
- How do their different strengths create complementary conversation?

**Visual Storytelling:**
- What's the single most dramatic image for each page?
- How do we show rather than tell the emotional beats?

**Generate specific creative ideas** for key moments:
- 2-3 specific visual ideas that showcase character personality
- A memorable line or moment for the pair crossover
- How their strength manifests in the second-attempt room

---

## Phase 3: Review & Generate

### 3.1 Present Story Summary

Before generating any files, present to the user:

**Story Arc Summary** (2-3 sentences describing the emotional journey)

**Key Creative Choices:**
- List 3-5 specific creative ideas you're excited about
- Note any particularly interesting visual moments planned
- Highlight how character details will be woven in

**Continuity Notes** (if existing pages were found):
- What constraints from existing pages must be preserved
- Any potential conflicts to resolve

### 3.2 Get User Approval

Ask the user:
> "Does this direction feel right? Any ideas you'd like me to incorporate or change?"

**Wait for user confirmation before generating pages.**

### 3.3 Generate Pages

For each page in @story/template.yaml where this character appears:

**Determine page type:**
- **Joint pages**: All 6 children appear
- **Pair pages**: Only this character and their designated pair partner
- **Individual pages**: Only this character

**File naming convention:**
- Format: `p{number}-{char1}-{char2}-{...}.yaml`
- List characters appearing on the page in **alphabetical order**, dash-separated
- Only include the 6 main children in filenames (not regan or dorje_legpa)
- Examples: `p01-arthur-cullan-emer-hansel-henry-james.yaml`, `p09-arthur-cullan.yaml`, `p07-cullan.yaml`

**For each page file:**
- If it exists and overwrite=no: Print "⏭️ Skipping p{number} (already exists)"
- If it exists and overwrite=yes: Print "♻️ Regenerating p{number}"
- If new: Print "✨ Creating p{number}"

**Page content (from @story/page-template.yaml structure):**
- Fill metadata from @story/template.yaml (id, section, page_type, characters, location, story_beat)
- Use symbolic room references from character file

**Visual field** (3-5 bullet points):
- Describe the single dramatic image for this page
- Focus on composition, character actions, key visual elements
- DO NOT duplicate info from template/character/location files (added automatically by image generator)
- Frame a specific moment in time matching the story_beat

**Text field** (aim for no more than 70 words):
- Third person for individual pages
- Include dialogue where appropriate (use quotes)
- Match tone to story_beat and character personality

**NEVER use TODO placeholders** - always write complete content.

### 3.4 Validate Generated Pages

Run the consistency checker to validate all generated pages:

```bash
uv run python scripts/check_inconsistencies.py
```

If any YAML validation errors are found, fix them before proceeding. Common issues:
- Colons in story_beat text need `|` block syntax (e.g., `story_beat: |`)
- Unquoted special characters

### 3.5 Summary

After completing, provide:
- Total pages for this character
- Pages created vs. skipped
- List of all page files
- Any notes on creative choices made
- Confirmation that consistency check passed
