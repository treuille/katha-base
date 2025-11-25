---
description: Check all documentation and templates for inconsistencies and errors
---

Systematically check all template files, example files, README, and scripts for inconsistencies, spelling mistakes, and other errors.

**IMPORTANT**: Skip and ignore all deprecated folders and any files within them. Do not check or report on deprecated content.

Please perform the following checks:

## 1. File Inventory
List all files in these directories (excluding any deprecated folders):
- `templates/` - All template and example YAML files
- `README.md` - Main documentation
- `scripts/` - Utility scripts
- `.claude/` - Project documentation

## 2. Cross-Document Consistency Checks

### File Naming Conventions
- Verify all documented naming patterns match actual examples
- Check character code format (two-letter + name)
- Check page numbering format (01, 02, not 1, 2)
- Verify shared page naming (alphabetical character codes)

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

### Template Files
- Consistent YAML structure across similar files
- Accurate comments and documentation
- Example data makes sense and is consistent
- No contradictory instructions or examples

### Scripts
- Accurate script descriptions in README
- Consistent error messages
- Clear and helpful comments
- No hardcoded values that should be variables

### .claude/ Documentation
- Consistent with README
- No contradictory instructions
- Accurate references to project structure

## 4. Quality Checks
- Spelling mistakes throughout all files
- Grammatical errors
- Inconsistent formatting (spacing, capitalization)
- Unclear or ambiguous instructions
- Outdated information

## 5. Report Format

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
