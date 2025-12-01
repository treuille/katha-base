#!/usr/bin/env python3
"""
Check for inconsistencies in the Katha Base project.

This script validates:
1. YAML file syntax and structure
2. File inventory (required directories and documentation files)
3. Cross-references between YAML files (characters, locations, attempts)
4. YAML structure consistency (required fields)
5. Naming conventions (YAML and image files)
6. Reference images for all locations and characters
7. Image naming conventions (auto-fixes underscore issues)
"""

import yaml
import sys
import re
from pathlib import Path
from collections import defaultdict


def validate_yaml_files():
    """Validate all YAML files are well-formed."""
    print("=" * 60)
    print("YAML VALIDATION")
    print("=" * 60)

    errors = []
    yaml_files = (
        list(Path('characters').glob('*.yaml')) +
        list(Path('locations').glob('*.yaml')) +
        [Path('story/template.yaml')] +
        list(Path('out/story').glob('*.yaml'))
    )

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
            print(f"✓ {yaml_file}")
        except yaml.YAMLError as e:
            error_msg = f"✗ {yaml_file}: {e}"
            errors.append(error_msg)
            print(error_msg)
        except FileNotFoundError:
            error_msg = f"✗ {yaml_file}: File not found"
            errors.append(error_msg)
            print(error_msg)

    if errors:
        print(f"\n❌ {len(errors)} YAML validation error(s) found")
        return False
    else:
        print(f"\n✅ All {len(yaml_files)} YAML files are well-formed")
        return True


def fix_image_naming():
    """Fix image naming conventions (replace underscore with hyphen ONLY before the number)."""
    print("\n" + "=" * 60)
    print("FIXING IMAGE NAMING CONVENTIONS")
    print("=" * 60)

    renamed_count = 0

    # Fix locations - keep underscores in names, only replace before number
    if Path('ref/locations').exists():
        for img in Path('ref/locations').glob('*.jpg'):
            # Check if the pattern is name_NN.jpg (underscore before number)
            if '_' in img.stem:
                parts = img.stem.rsplit('_', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    # Replace only the last underscore with hyphen
                    new_name = f"{parts[0]}-{parts[1]}.jpg"
                    new_path = img.parent / new_name
                    img.rename(new_path)
                    print(f"  Renamed: {img.name} → {new_name}")
                    renamed_count += 1

    # Fix characters - replace ALL underscores with hyphens
    if Path('ref/characters').exists():
        for img in Path('ref/characters').glob('*_*.jpg'):
            new_name = img.name.replace('_', '-')
            new_path = img.parent / new_name
            img.rename(new_path)
            print(f"  Renamed: {img.name} → {new_name}")
            renamed_count += 1

    if renamed_count > 0:
        print(f"\n✓ Renamed {renamed_count} image(s) to use correct naming")
    else:
        print("\n✓ All images already use correct naming convention")

    return True


def check_reference_images():
    """Check that all locations and characters have reference images."""
    print("\n" + "=" * 60)
    print("REFERENCE IMAGE VERIFICATION")
    print("=" * 60)

    issues = []

    # Check locations
    print("\nLocations:")
    location_files = list(Path('locations').glob('*.yaml'))
    location_images = defaultdict(list)

    if Path('ref/locations').exists():
        for img in Path('ref/locations').glob('*.jpg'):
            # Extract location name from image filename (e.g., "dining_room-01.jpg" -> "dining_room")
            location_name = img.stem.rsplit('-', 1)[0]
            location_images[location_name].append(img.name)

    for location_file in location_files:
        location_id = location_file.stem
        with open(location_file, 'r') as f:
            data = yaml.safe_load(f)
            display_name = data.get('display_name', location_id)

        if location_id in location_images:
            print(f"  ✓ {location_id}: {len(location_images[location_id])} image(s) - {', '.join(location_images[location_id])}")
        else:
            issue = f"  ✗ {location_id} ({display_name}): No reference images found"
            print(issue)
            issues.append(issue)

    # Check characters
    print("\nCharacters:")
    character_files = list(Path('characters').glob('*.yaml'))
    character_images = defaultdict(list)

    if Path('ref/characters').exists():
        for img in Path('ref/characters').glob('*.jpg'):
            # Extract character name from image filename (e.g., "arthur-01.jpg" -> "arthur")
            # Convert hyphens to underscores to match character ID format
            character_name = img.stem.rsplit('-', 1)[0].replace('-', '_')
            character_images[character_name].append(img.name)

    for character_file in character_files:
        character_id = character_file.stem
        with open(character_file, 'r') as f:
            data = yaml.safe_load(f)
            display_name = data.get('name', character_id)

        if character_id in character_images:
            print(f"  ✓ {character_id}: {len(character_images[character_id])} image(s) - {', '.join(character_images[character_id])}")
        else:
            issue = f"  ✗ {character_id} ({display_name}): No reference images found"
            print(issue)
            issues.append(issue)

    if issues:
        print(f"\n❌ {len(issues)} missing reference image(s)")
        return False
    else:
        print(f"\n✅ All locations and characters have reference images")
        return True


def check_file_inventory():
    """Check that expected directories and key files exist."""
    print("\n" + "=" * 60)
    print("FILE INVENTORY")
    print("=" * 60)

    issues = []

    # Check required directories
    required_dirs = {
        'characters': 'Character YAML files',
        'locations': 'Location YAML files',
        'story': 'Story template and overview',
        'ref': 'Reference images',
        'ref/characters': 'Character reference images',
        'ref/locations': 'Location reference images',
        'ref/objects': 'Object reference images',
        'out': 'Generated outputs',
        'out/images': 'Generated illustrations',
        'out/story': 'Generated story files',
    }

    print("\nChecking directories:")
    for dir_path, description in required_dirs.items():
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}/ ({description})")
        else:
            issue = f"  ✗ Missing directory: {dir_path}/ ({description})"
            print(issue)
            issues.append(issue)

    # Check key documentation files
    required_files = {
        'README.md': 'Main project documentation',
        'story/overview.md': 'Story world overview',
        'story/template.yaml': 'Story template',
        '.claude/claude.md': 'Claude context documentation',
    }

    print("\nChecking key files:")
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"  ✓ {file_path} ({description})")
        else:
            issue = f"  ✗ Missing file: {file_path} ({description})"
            print(issue)
            issues.append(issue)

    # Report file counts
    print("\nFile counts:")
    print(f"  Characters: {len(list(Path('characters').glob('*.yaml')))} YAML files")
    print(f"  Locations: {len(list(Path('locations').glob('*.yaml')))} YAML files")
    if Path('ref/characters').exists():
        print(f"  Character images: {len(list(Path('ref/characters').glob('*.jpg')))} files")
    if Path('ref/locations').exists():
        print(f"  Location images: {len(list(Path('ref/locations').glob('*.jpg')))} files")
    if Path('ref/objects').exists():
        print(f"  Object images: {len(list(Path('ref/objects').glob('*.jpg')))} files")

    if issues:
        print(f"\n❌ {len(issues)} file inventory issue(s) found")
        return False
    else:
        print("\n✅ All expected directories and files present")
        return True


def check_cross_references():
    """Validate cross-references between YAML files and images."""
    print("\n" + "=" * 60)
    print("CROSS-REFERENCE VALIDATION")
    print("=" * 60)

    issues = []

    # Load all character and location IDs
    character_ids = set()
    location_ids = set()

    for yaml_file in Path('characters').glob('*.yaml'):
        character_ids.add(yaml_file.stem)

    for yaml_file in Path('locations').glob('*.yaml'):
        location_ids.add(yaml_file.stem)

    print("\nValidating character attempt_locations:")
    for char_file in Path('characters').glob('*.yaml'):
        with open(char_file, 'r') as f:
            data = yaml.safe_load(f)

        if 'attempt_locations' in data:
            for loc in data['attempt_locations']:
                if loc not in location_ids:
                    issue = f"  ✗ {char_file.stem}: references non-existent location '{loc}'"
                    print(issue)
                    issues.append(issue)
                else:
                    print(f"  ✓ {char_file.stem}: attempt_location '{loc}' exists")

    print("\nValidating location character references:")
    for loc_file in Path('locations').glob('*.yaml'):
        with open(loc_file, 'r') as f:
            data = yaml.safe_load(f)

        # Check attempts array
        if 'attempts' in data:
            for attempt in data['attempts']:
                if 'character' in attempt:
                    char_id = attempt['character']
                    if char_id not in character_ids:
                        issue = f"  ✗ {loc_file.stem}: references non-existent character '{char_id}'"
                        print(issue)
                        issues.append(issue)
                    else:
                        print(f"  ✓ {loc_file.stem}: character '{char_id}' exists")

        # Check special character fields
        for field in ['release_lead_character', 'climax_focus_character']:
            if field in data:
                char_id = data[field]
                if char_id not in character_ids:
                    issue = f"  ✗ {loc_file.stem}: {field} '{char_id}' does not exist"
                    print(issue)
                    issues.append(issue)
                else:
                    print(f"  ✓ {loc_file.stem}: {field} '{char_id}' exists")

    if issues:
        print(f"\n❌ {len(issues)} cross-reference issue(s) found")
        return False
    else:
        print("\n✅ All cross-references are valid")
        return True


def check_visual_field_structure():
    """Check that visual fields contain only plain strings, no nested elements."""
    print("\n" + "=" * 60)
    print("VISUAL FIELD STRUCTURE VALIDATION")
    print("=" * 60)

    issues = []

    print("\nValidating character visual fields:")
    for char_file in Path('characters').glob('*.yaml'):
        with open(char_file, 'r') as f:
            data = yaml.safe_load(f)

        if 'visual' not in data:
            print(f"  - {char_file.stem}: no visual field (skipped)")
            continue

        visual = data['visual']
        if not isinstance(visual, list):
            issue = f"  ✗ {char_file.stem}: visual field is not a list"
            print(issue)
            issues.append(issue)
            continue

        has_nested = False
        for i, item in enumerate(visual):
            if not isinstance(item, str):
                issue = f"  ✗ {char_file.stem}: visual[{i}] is {type(item).__name__}, expected str"
                print(issue)
                issues.append(issue)
                has_nested = True

        if not has_nested:
            print(f"  ✓ {char_file.stem}: all visual items are plain strings")

    print("\nValidating location visual fields:")
    for loc_file in Path('locations').glob('*.yaml'):
        with open(loc_file, 'r') as f:
            data = yaml.safe_load(f)

        if 'visual' not in data:
            print(f"  - {loc_file.stem}: no visual field (skipped)")
            continue

        visual = data['visual']
        if not isinstance(visual, list):
            issue = f"  ✗ {loc_file.stem}: visual field is not a list"
            print(issue)
            issues.append(issue)
            continue

        has_nested = False
        for i, item in enumerate(visual):
            if not isinstance(item, str):
                issue = f"  ✗ {loc_file.stem}: visual[{i}] is {type(item).__name__}, expected str"
                print(issue)
                issues.append(issue)
                has_nested = True

        if not has_nested:
            print(f"  ✓ {loc_file.stem}: all visual items are plain strings")

    if issues:
        print(f"\n❌ {len(issues)} visual field structure issue(s) found")
        return False
    else:
        print("\n✅ All visual fields contain plain strings only")
        return True


def check_yaml_structure():
    """Check YAML structure consistency across files."""
    print("\n" + "=" * 60)
    print("YAML STRUCTURE CONSISTENCY")
    print("=" * 60)

    issues = []

    # Required fields for characters (description is optional)
    required_character_fields = ['name', 'age']

    print("\nValidating character file structure:")
    for char_file in Path('characters').glob('*.yaml'):
        with open(char_file, 'r') as f:
            data = yaml.safe_load(f)

        missing_fields = [field for field in required_character_fields if field not in data]
        if missing_fields:
            issue = f"  ✗ {char_file.stem}: missing fields {missing_fields}"
            print(issue)
            issues.append(issue)
        else:
            print(f"  ✓ {char_file.stem}: has all required fields")

    # Required fields for locations (type is optional, but display_name is required)
    required_location_fields = ['display_name']

    print("\nValidating location file structure:")
    for loc_file in Path('locations').glob('*.yaml'):
        with open(loc_file, 'r') as f:
            data = yaml.safe_load(f)

        missing_fields = [field for field in required_location_fields if field not in data]
        if missing_fields:
            issue = f"  ✗ {loc_file.stem}: missing fields {missing_fields}"
            print(issue)
            issues.append(issue)
        else:
            print(f"  ✓ {loc_file.stem}: has all required fields")

    if issues:
        print(f"\n❌ {len(issues)} structure issue(s) found")
        return False
    else:
        print("\n✅ All YAML files have consistent structure")
        return True


def check_naming_conventions():
    """Validate file naming conventions."""
    print("\n" + "=" * 60)
    print("NAMING CONVENTION VALIDATION")
    print("=" * 60)

    issues = []

    # Check YAML file naming (should be lowercase with underscores)
    yaml_pattern = re.compile(r'^[a-z][a-z0-9_]*\.yaml$')

    print("\nValidating YAML file names:")
    for yaml_file in list(Path('characters').glob('*.yaml')) + list(Path('locations').glob('*.yaml')):
        if not yaml_pattern.match(yaml_file.name):
            issue = f"  ✗ {yaml_file}: does not match naming pattern (lowercase, underscores only)"
            print(issue)
            issues.append(issue)
        else:
            print(f"  ✓ {yaml_file.name}")

    # Check image file naming (should be id-XX.jpg, where id can contain hyphens for multi-word names)
    image_pattern = re.compile(r'^[a-z][a-z0-9_-]*-\d{2}\.jpg$')

    print("\nValidating image file names:")
    if Path('ref/characters').exists():
        for img_file in Path('ref/characters').glob('*.jpg'):
            if not image_pattern.match(img_file.name):
                issue = f"  ✗ ref/characters/{img_file.name}: does not match pattern (id-XX.jpg)"
                print(issue)
                issues.append(issue)
            else:
                print(f"  ✓ ref/characters/{img_file.name}")

    if Path('ref/locations').exists():
        for img_file in Path('ref/locations').glob('*.jpg'):
            if not image_pattern.match(img_file.name):
                issue = f"  ✗ ref/locations/{img_file.name}: does not match pattern (id-XX.jpg)"
                print(issue)
                issues.append(issue)
            else:
                print(f"  ✓ ref/locations/{img_file.name}")

    # Check ID consistency between YAML and images
    print("\nValidating ID consistency between YAML files and images:")

    # Characters
    for char_file in Path('characters').glob('*.yaml'):
        char_id = char_file.stem
        has_image = False
        if Path('ref/characters').exists():
            for img in Path('ref/characters').glob('*.jpg'):
                img_id = img.stem.rsplit('-', 1)[0].replace('-', '_')
                if img_id == char_id:
                    has_image = True
                    break

        if has_image:
            print(f"  ✓ {char_id}: YAML and image ID match")
        else:
            issue = f"  ✗ {char_id}: YAML exists but no matching image ID found"
            print(issue)
            issues.append(issue)

    # Locations
    for loc_file in Path('locations').glob('*.yaml'):
        loc_id = loc_file.stem
        has_image = False
        if Path('ref/locations').exists():
            for img in Path('ref/locations').glob('*.jpg'):
                img_id = img.stem.rsplit('-', 1)[0]
                if img_id == loc_id:
                    has_image = True
                    break

        if has_image:
            print(f"  ✓ {loc_id}: YAML and image ID match")
        else:
            issue = f"  ✗ {loc_id}: YAML exists but no matching image ID found"
            print(issue)
            issues.append(issue)

    if issues:
        print(f"\n❌ {len(issues)} naming convention issue(s) found")
        return False
    else:
        print("\n✅ All files follow naming conventions")
        return True


def main():
    """Run all consistency checks."""
    print("KATHA BASE - INCONSISTENCY CHECKER")
    print()

    all_passed = True

    # Run YAML validation
    if not validate_yaml_files():
        all_passed = False

    # Fix image naming conventions
    fix_image_naming()

    # Run file inventory check
    if not check_file_inventory():
        all_passed = False

    # Run cross-reference validation
    if not check_cross_references():
        all_passed = False

    # Run YAML structure consistency check
    if not check_yaml_structure():
        all_passed = False

    # Run visual field structure check
    if not check_visual_field_structure():
        all_passed = False

    # Run naming convention validation
    if not check_naming_conventions():
        all_passed = False

    # Run reference image check
    if not check_reference_images():
        all_passed = False

    # Final summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
