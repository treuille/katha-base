#!/usr/bin/env python3
"""
Generate images for all storybook pages in parallel.

Usage:
    uv run scripts/gen_all_images.py [--workers N] [--backend MODEL]

Options:
    --workers N     Number of concurrent image generations (default: 5)
    --backend MODEL Model backend to use: openai or prompt (default: openai)

Examples:
    uv run scripts/gen_all_images.py
    uv run scripts/gen_all_images.py --workers 10
    uv run scripts/gen_all_images.py --backend prompt --workers 20
"""

import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
import argparse


def find_all_pages() -> List[Path]:
    """Find all page YAML files in the pages/ directory."""
    pages_dir = Path("pages")
    if not pages_dir.exists():
        print(f"Error: {pages_dir} directory not found")
        sys.exit(1)

    # Find all .yaml files in pages/
    pages = sorted(pages_dir.glob("*.yaml"))

    if not pages:
        print(f"Error: No .yaml files found in {pages_dir}")
        sys.exit(1)

    return pages


def generate_image(page_path: Path, backend: str) -> Tuple[Path, bool, str]:
    """
    Generate image for a single page.
    Returns (page_path, success, message).
    """
    page_id = page_path.stem

    try:
        # Print header for this worker
        print(f"\n{'='*80}")
        print(f"[{page_id}] Starting generation...")
        print(f"{'='*80}\n")

        # Call gen_image.py as subprocess, letting output flow through
        result = subprocess.run(
            ["uv", "run", "scripts/gen_image.py", backend, str(page_path)],
            timeout=180,  # 3 minute timeout per image
        )

        # Print footer for this worker
        print(f"\n{'='*80}")
        print(f"[{page_id}] Finished (exit code: {result.returncode})")
        print(f"{'='*80}\n")

        if result.returncode == 0:
            return (page_path, True, f"✓ {page_id}")
        else:
            return (page_path, False, f"✗ {page_id}: Exit code {result.returncode}")

    except subprocess.TimeoutExpired:
        print(f"\n{'='*80}")
        print(f"[{page_id}] TIMEOUT after 3 minutes")
        print(f"{'='*80}\n")
        return (page_path, False, f"✗ {page_id}: Timeout (>3min)")
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"[{page_id}] ERROR: {str(e)}")
        print(f"{'='*80}\n")
        return (page_path, False, f"✗ {page_id}: {str(e)[:100]}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate images for all storybook pages in parallel"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Number of concurrent image generations (default: 5)",
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="openai",
        choices=["openai", "prompt"],
        help="Model backend to use (default: openai)",
    )

    args = parser.parse_args()

    # Find all pages
    pages = find_all_pages()
    total = len(pages)

    print(f"Found {total} pages to process")
    print(f"Using {args.workers} concurrent workers")
    print(f"Backend: {args.backend}")
    print("=" * 80)

    # Process pages in parallel
    successes = []
    failures = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        future_to_page = {
            executor.submit(generate_image, page, args.backend): page
            for page in pages
        }

        # Process results as they complete
        completed = 0
        for future in as_completed(future_to_page):
            page_path, success, message = future.result()
            completed += 1

            print(f"[{completed}/{total}] {message}")

            if success:
                successes.append(page_path)
            else:
                failures.append((page_path, message))

    # Print summary
    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Total pages:    {total}")
    print(f"  Successful:     {len(successes)}")
    print(f"  Failed:         {len(failures)}")

    if failures:
        print(f"\nFailed pages:")
        for page_path, message in failures:
            print(f"  - {page_path.name}: {message}")
        sys.exit(1)
    else:
        print(f"\n✓ All images generated successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
