---
description: Check all documentation and templates for inconsistencies and errors
---

Run the automated inconsistency checker, then perform manual checks for remaining issues.

## Automated Checks

First, run the automated inconsistency checking script:

```bash
uv run python scripts/check_inconsistencies.py
```

This script automatically validates:
- YAML file syntax and structure
- Reference images for all locations and characters
- Image naming conventions (fixes underscore issues)

## Manual Checks

After running the automated script, systematically check for the following:

**IMPORTANT**: Skip and ignore all deprecated folders and any files within them. Do not check or report on deprecated content.

Please perform the following manual checks:

## 1. File Inventory
List all files in these directories (excluding any deprecated folders):
- `characters/` - Character YAML files
- `locations/` - Location YAML files
- `story/` - Story template and overview
- `README.md` - Main documentation
- `.claude/` - Project documentation

## 2. Cross-Document Consistency Checks

### File Naming Conventions
- Verify all documented naming patterns match actual examples
- Check file naming format: `id.yaml` or `id-xx.jpg` where:
  - `id` is a multiple letter code, potentially with underscores (e.g., `arthur`, `dining_room`, `sun_room`)
  - `xx` is a digit number with leading 0 (e.g., `01`, `02`, not `1`, `2`)
- Verify consistency across character, location, and image files

### Terminology Consistency
- Check that terms are used consistently across all files (e.g., "spread" vs "page", "storybook" vs "book")
- Verify technical terms like "YAML", "markdown" are spelled consistently
- Check that character names in examples match across files

### Structural References
- Verify that all referenced template files exist
- Check that file paths mentioned in README are accurate
- Confirm directory structure in README matches actual structure
- Verify all example file references are correct

## 3. Content Accuracy Checks

### README.md
- Spelling and grammar
- Accurate file path references
- Correct command examples
- Up-to-date directory structure
- Accurate description of workflows

### YAML Data Files
- Consistent YAML structure across similar files (characters, locations, story template)
- Accurate comments and documentation
- Example data makes sense and is consistent
- No contradictory instructions or examples

### .claude/ Documentation
- Consistent with README
- No contradictory instructions
- Accurate references to project structure

## 4. YAML Validation
- Verify all YAML files are well-formed and parseable
- Check for syntax errors (indentation, colons, quotes, etc.)
- Validate YAML structure consistency across similar file types
- Ensure no duplicate keys or invalid values

## 5. Reference Image Verification
- Verify every location has at least one reference image in `ref/locations/`
- Verify every character has at least one reference image in `ref/characters/`
- Check that image filenames follow naming conventions (e.g., `location_name-01.jpg`)
- Report any locations or characters missing reference images

## 6. Quality Checks
- Spelling mistakes throughout all files
- Grammatical errors
- Inconsistent formatting (spacing, capitalization)
- Unclear or ambiguous instructions
- Outdated information

## 7. Report Format

For each issue found, report:
1. **File**: Which file contains the issue
2. **Line** (if applicable): Specific line number
3. **Type**: Inconsistency/Spelling/Grammar/Formatting/Other
4. **Issue**: What's wrong
5. **Suggestion**: How to fix it

Organize findings by severity:
- **Critical**: Things that would cause confusion or errors
- **Important**: Inconsistencies that reduce clarity
- **Minor**: Spelling, formatting, small improvements

If no issues are found, confirm that everything is consistent and correct.
