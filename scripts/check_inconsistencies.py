#!/usr/bin/env python3
"""
Check for inconsistencies in the Katha Base project.

This script validates:
1. YAML file syntax and structure
2. Reference images for all locations and characters
3. Location and character ID consistency
"""

import yaml
import sys
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
        [Path('story/template.yaml')]
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
    if Path('ref-images/locations').exists():
        for img in Path('ref-images/locations').glob('*.jpg'):
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
    if Path('ref-images/ref-characters').exists():
        for img in Path('ref-images/ref-characters').glob('*_*.jpg'):
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

    if Path('ref-images/locations').exists():
        for img in Path('ref-images/locations').glob('*.jpg'):
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

    if Path('ref-images/ref-characters').exists():
        for img in Path('ref-images/ref-characters').glob('*.jpg'):
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
