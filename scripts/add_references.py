#!/usr/bin/env python3
"""Add symlinks to katha-base reference files."""

import os
import sys
from pathlib import Path

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def success(msg):
    print(f"{GREEN}✓{RESET} {msg}")


def error(msg):
    print(f"{RED}✗{RESET} {msg}")


SYMLINKS = [
    # (link_path, target_relative_to_link_parent)
    ("ref/characters", "../../katha-base/ref/characters"),
    ("ref/locations", "../../katha-base/ref/locations"),
    ("ref/objects", "../../katha-base/ref/objects"),
    ("ref/styles", "../../katha-base/ref/styles"),
    ("out/versions", "../../katha-base/out/versions"),
    ("out/images", "../../katha-base/out/images"),
    ("bak", "../katha-base/bak"),
]


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)

    # Check katha-base exists
    if not Path("../katha-base").is_dir():
        error("../katha-base directory not found")
        sys.exit(1)
    success("Found ../katha-base")

    # Check for existing symlinks/files
    errors = []
    for link_path, _ in SYMLINKS:
        if Path(link_path).exists() or Path(link_path).is_symlink():
            errors.append(f"{link_path} already exists")

    if errors:
        for e in errors:
            error(e)
        error("Remove existing paths before running this script")
        sys.exit(1)

    # Create symlinks
    for link_path, target in SYMLINKS:
        Path(link_path).symlink_to(target)
        success(f"Created {link_path} → {target}")

    success("All symlinks created!")


if __name__ == "__main__":
    main()
