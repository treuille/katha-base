# Migration Guide: Node Types & Layout Refactor

This guide explains how to migrate existing stories to the new structure with narrative node types and the updated layout system.

## What Changed

### Layout Structure

**Old Structure:**
- 12 spreads per character
- 1 page per spread = 12 pages total
- 1 image per page = 12 images total
- 2 sentences per page
- File naming: `{char}-{spread}.yaml` (e.g., `cu-03.yaml`)

**New Structure:**
- 12 spreads per character (same)
- **2 pages per spread = 24 pages total**
- **2 images per page = 48 images total**
- **2-3 sentences per image**
- File naming: `{char}-{spread}-{page}.yaml` (e.g., `cu-03-1.yaml`, `cu-03-2.yaml`)

### Narrative Node Types

**Old System:**
- No formal node types
- Shared pages were just regular pages with multiple character codes

**New System:**
Four node types with specific metadata requirements:

1. **Solo (👤):** Single character moment
2. **Meeting (🤝):** Characters physically meet
   - Required metadata: location, shared_action, dialogue_packets, cross_book_alignment
3. **Mirrored (🪞):** Parallel challenges, thematic rhyming
   - Required metadata: shared_theme, scenario_variants, symbolic_motif, spread_alignment
4. **Resonant (✨):** Emotional ripple across distance
   - Required metadata: emotional_state_packets, ripple_effect, symbolic_resonance, placement_rule

## Migration Steps

### 1. Update Character Files

**Action:** Update story lists to include 24 pages instead of 12.

**Before:**
```yaml
story:
  - cu-01.yaml
  - cu-02.yaml
  # ... through cu-12.yaml
```

**After:**
```yaml
story:
  # Spread 1 (character-specific)
  - cu-01-1.yaml
  - cu-01-2.yaml

  # Spread 2
  - cu-02-1.yaml
  - cu-02-2.yaml

  # ... continue for all 12 spreads

  # Spread 12 (character-specific)
  - cu-12-1.yaml
  - cu-12-2.yaml
```

### 2. Split Existing Pages

For each existing page (e.g., `cu-03.yaml`), create 2 new pages:

**Original Page Structure:**
```yaml
id: cu-03
spread: 3
beat: "Attempt #1"
description: Cullan tries climbing the ladder
visual: |
  [One long visual description]
text: |
  Cullan tried to climb but the ladder was slippery.
```

**Split into 2 Pages:**

**`cu-03-1.yaml`:**
```yaml
id: cu-03-1
spread: 3
page: 1
node_type: solo
beat: "Attempt #1"
description: Cullan approaches the ladder
images:
  - image_number: 1
    visual: |
      Cullan stands at base of oak tree, examining ladder
    text: |
      Cullan had a plan: climb the tree. He tested the ladder carefully.

  - image_number: 2
    visual: |
      Cullan places foot on first rung, confident expression
    text: |
      The first rung looked sturdy. He was ready to start his ascent.
```

**`cu-03-2.yaml`:**
```yaml
id: cu-03-2
spread: 3
page: 2
node_type: solo
beat: "Attempt #1"
description: Cullan's ladder attempt fails
images:
  - image_number: 1
    visual: |
      Cullan mid-slip, ladder tilting, surprised expression
    text: |
      His foot slipped on the wet rung. Everything happened so fast!

  - image_number: 2
    visual: |
      Cullan on ground, looking up at ladder, tools scattered
    text: |
      He sat on the ground, mud on his pants. Time for a new plan.
```

### 3. Add Node Type Metadata

For each page, add the appropriate `node_type` field and metadata:

**Solo Nodes:**
```yaml
node_type: solo
# No additional metadata required
```

**Meeting Nodes:**
```yaml
node_type: meeting
meeting_data:
  location: "The Ancient Library's reading room"
  time_context: "Morning of day 3, spread 7"
  shared_action: "Characters decode an ancient map together"
  dialogue_packets:
    - character: cu
      line: "Look at these symbols!"
    - character: ma
      line: "They match my grandmother's pendant."
  cross_book_alignment:
    scene_id: "library_map_discovery"
    pov_variants:
      - character: cu
        focus: "Map details and architecture"
      - character: ma
        focus: "Emotional connection to pendant"
```

**Mirrored Nodes:**
```yaml
node_type: mirrored
mirrored_data:
  shared_theme: "Facing fear of heights"
  scenario_variants:
    - character: cu
      scenario: "Climbing oak to rescue bird"
      location: "Forest clearing"
    - character: no
      scenario: "Ascending library ladder for ancient book"
      location: "Town library"
  symbolic_motif: "Golden feather catching light"
  spread_alignment: spread_5
  visual_rhyming:
    - element: "Upward perspective"
    - element: "Sweat on brow, tight grip"
```

**Resonant Nodes:**
```yaml
node_type: resonant
resonant_data:
  emotional_state_packets:
    - character: cu
      state: "Breakthrough clarity after struggle"
      trigger: "Realizes pattern in forest paths"
    - character: ma
      state: "Sudden hope despite setback"
      trigger: "Feels warmth and certainty"
  ripple_effect: |
    As Cullan discovers the pattern, Maya feels sudden warmth
    miles away. Connection unexplained but visual.
  symbolic_resonance:
    phenomenon: "Sky shimmer with golden light"
    description: "Both look up, see same golden light"
  placement_rule: "Follows Cullan's growth in spread 6"
  temporal_sync: "Same afternoon, different locations"
```

### 4. Rename and Update Shared Pages

**Old naming:**
- `cu-ma-07.yaml` (both characters at spread 7)

**New naming:**
- `cu-ma-07-1.yaml` (both characters, spread 7, page 1)
- `cu-ma-07-2.yaml` (both characters, spread 7, page 2)

Remember: Character codes must be alphabetically ordered!

### 5. Run Validation

After migration, run the validation script:

```bash
python3 scripts/validate_structure.py
```

Expected warnings during migration:
- "Page missing 'node_type' field" - Add node types
- "Page missing 'images' array" - Convert to new structure
- "Has X pages, expected 24" - Complete the page split

### 6. Update Image Generation

The `gen_image.py` script supports both old and new formats:

**For new-structure pages:**
```bash
# Generate both images (default)
uv run scripts/gen_image.py openai pages/cu-03-1.yaml

# Generate specific image
uv run scripts/gen_image.py openai pages/cu-03-1.yaml --image-num 1
```

**Output naming:**
- Old: `cu-03-openai.jpg`
- New: `cu-03-1-img1-openai.jpg`, `cu-03-1-img2-openai.jpg`

## Migration Strategy Recommendations

### Incremental Migration (Recommended)

1. **Start with one character** (e.g., Noah)
2. **Update character file** (24 pages instead of 12)
3. **Create new page files** with new structure
4. **Add node types** as you create pages
5. **Test with validation script**
6. **Generate images** for completed pages
7. **Repeat for next character**

### Advantages:
- Test the new system gradually
- Learn node type patterns
- Catch issues early
- Validate frequently

### Bulk Migration (Advanced)

Create a script to batch-convert pages, but manually review:
- Text splitting (ensure logical breaks)
- Visual description splitting (2 coherent moments)
- Node type assignment (requires understanding story flow)

## Common Migration Patterns

### Pattern 1: Action Sequence

**Old (1 image):**
> "Cullan climbed the ladder but it was slippery and he fell."

**New (2 images):**
> Image 1: "Cullan gripped the ladder, ready to climb. Today would be different."
> Image 2: "His foot slipped! He tumbled backwards toward the ground."

### Pattern 2: Discovery and Reaction

**Old (1 image):**
> "Cullan found the hidden key and realized what it meant."

**New (2 images):**
> Image 1: "Behind the loose stone, Cullan spotted something golden. A key!"
> Image 2: "He held the ancient key up to the light. This changed everything."

### Pattern 3: Dialogue Exchange

**Old (1 image):**
> "Maya told Cullan about the map and he agreed to help."

**New (2 images):**
> Image 1: "Maya unrolled the old map. 'I need your help,' she said quietly."
> Image 2: "Cullan studied the strange symbols. 'I'm in,' he replied with a nod."

## Backward Compatibility

The updated scripts maintain backward compatibility:

- **`validate_structure.py`:** Works with both formats (warns about missing fields)
- **`gen_image.py`:** Detects structure automatically
- **`show_story.py`:** Displays both formats correctly

This allows gradual migration without breaking existing workflows.

## Node Type Selection Guide

### When to use Solo
- Character alone
- Internal monologue moments
- Individual challenges
- Personal discoveries

### When to use Meeting
- Characters physically in same place
- Direct interaction required
- Shared dialogue
- Collaborative action
- Same scene from different POVs

### When to use Mirrored
- Characters face similar challenges separately
- Thematic parallels
- Symbolic connections
- Different locations, same emotional beat
- "What if" comparisons

### When to use Resonant
- Emotional connection across distance
- One character's growth affects another
- Unexplained sympathetic moments
- Symbolic environmental phenomena
- MUST follow character growth moment

## Validation Checklist

Before considering migration complete:

- [ ] Character file has 24 pages
- [ ] All page files follow new naming: `{char}-{spread}-{page}.yaml`
- [ ] Each page has `node_type` field
- [ ] Each page has `page` field (1 or 2)
- [ ] Each page has `images` array with 2 images
- [ ] Each image has `visual` and `text` fields
- [ ] Text is 2-3 sentences per image
- [ ] Node-specific metadata present (meeting, mirrored, resonant)
- [ ] Spreads 1, 11, 12 are character-specific (no shared pages)
- [ ] Shared pages use alphabetical character codes
- [ ] `python3 scripts/validate_structure.py` passes

## Getting Help

If you encounter issues during migration:

1. Check `templates/page-example.yaml` for current structure
2. Review `templates/story-template.yaml` for node type specifications
3. Run validation frequently: `python3 scripts/validate_structure.py`
4. Use show_story to preview: `python3 scripts/show_story.py <char-code>`
5. Test image generation on one page first

## Timeline

Estimated migration time per character:
- Simple story (12 → 24 pages): 2-4 hours
- Complex story with multiple node types: 4-8 hours
- Full project (3-4 characters): 1-2 weeks

Budget more time for:
- First character (learning curve)
- Adding rich node metadata
- Image regeneration
- Story refinement
