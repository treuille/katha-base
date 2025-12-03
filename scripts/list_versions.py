#!/usr/bin/env python3
"""List all versions with nice formatting."""

import sys
from pathlib import Path

# Add parent directory to path so we can import from scripts package
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.versioning import VERSIONS_DIR, read_manifest

# ANSI colors
CYAN = '\033[36m'
YELLOW = '\033[33m'
DIM = '\033[2m'
RESET = '\033[0m'

TOTAL_WIDTH = 50


def main():
    if not VERSIONS_DIR.exists():
        print("No versions found.")
        return

    versions = sorted(
        [p for p in VERSIONS_DIR.iterdir() if p.is_dir() and p.name.isdigit()],
        key=lambda p: int(p.name)
    )

    if not versions:
        print("No versions found.")
        return

    for version_path in versions:
        version_num = int(version_path.name)
        manifest = read_manifest(version_num)

        if manifest is None:
            continue

        version_str = f"{CYAN}{version_num:02d}{RESET}"

        num_images = len(manifest.get('images', {}))
        num_books = len(manifest.get('books', []))
        message = manifest.get('message') or ''

        # Calculate available space for message
        # Format: "NN  message...  counts"
        # We want counts right-aligned, so calculate message space
        max_counts_len = 12  # e.g. "99 img 9 PDF"
        fixed_chars = 2 + 2 + 2 + max_counts_len  # version + gaps + counts
        max_msg_len = TOTAL_WIDTH - fixed_chars

        # Truncate message if needed
        if len(message) > max_msg_len:
            message = message[:max_msg_len - 2] + '..'

        # Pad message to fixed width
        message_padded = message.ljust(max_msg_len)

        # Build counts display (left-aligned, with dim labels)
        # Use consistent spacing: "NN img N pdf" format
        if num_images == 0 and num_books == 0:
            counts_display = f"{DIM}empty{RESET}"
        elif num_images == 0:
            counts_display = f"       {num_books} {DIM}pdf{RESET}"
        elif num_books == 0:
            counts_display = f"{num_images:2d} {DIM}img{RESET}"
        else:
            counts_display = f"{num_images:2d} {DIM}img{RESET} {num_books} {DIM}pdf{RESET}"

        print(f"{version_str}  {YELLOW}{message_padded}{RESET}  {counts_display}")


if __name__ == '__main__':
    main()
