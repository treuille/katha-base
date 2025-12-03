"""
Versioning utilities for the katha picture book project.

Provides functions for managing version folders, computing prompt hashes,
and reading/writing manifests.
"""

import hashlib
import subprocess
import threading
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Module-level lock for thread-safe manifest updates
_manifest_lock = threading.Lock()

__all__ = [
    'OUT_DIR',
    'IMAGES_DIR',
    'get_latest_version',
    'get_version_path',
    'compute_prompt_hash',
    'find_existing_image',
    'get_prompt_path',
    'get_image_path',
    'read_manifest',
    'write_manifest',
    'get_git_commit',
    'create_new_version',
    'update_manifest_image',
    'update_manifest_book',
]

OUT_DIR = Path('out')
VERSIONS_DIR = OUT_DIR / 'versions'
IMAGES_DIR = OUT_DIR / 'images'


def get_latest_version() -> int:
    """Get the latest version number from out/versions/ directory.

    Scans for directories named with 2-digit numbers (01, 02, etc.)
    Returns 0 if no version folders exist.
    """
    if not VERSIONS_DIR.exists():
        return 0

    max_version = 0
    for path in VERSIONS_DIR.iterdir():
        if path.is_dir() and path.name.isdigit() and len(path.name) == 2:
            version = int(path.name)
            max_version = max(max_version, version)

    return max_version


def get_version_path(version: int) -> Path:
    """Get the path for a specific version folder."""
    return VERSIONS_DIR / f'{version:02d}'


def compute_prompt_hash(prompt: str, seed: int | None = None, ref_images: list[str] | None = None) -> str:
    """Compute a 5-character hash from prompt text, optional seed, and reference images.

    Uses SHA-256 and takes first 5 hex characters.
    If seed is provided, it's included in the hash to ensure different
    seeds produce different hashes (and thus different cached images).
    If ref_images is provided, the sorted list of image paths is included
    to ensure different reference images produce different hashes.

    Args:
        prompt: The prompt text
        seed: Optional seed for reproducible generation
        ref_images: Optional list of reference image paths

    Returns:
        5-character hex hash
    """
    content = prompt
    if seed is not None:
        content = f"{content}|seed={seed}"
    if ref_images:
        # Sort to ensure consistent ordering
        content = f"{content}|refs={','.join(sorted(ref_images))}"
    return hashlib.sha256(content.encode()).hexdigest()[:5]


def get_prompt_path(page_stem: str, prompt_hash: str) -> Path:
    """Get path for prompt TXT file in shared images directory.

    Args:
        page_stem: The page identifier (e.g., "p01-arthur-cullan")
        prompt_hash: The 5-char prompt hash

    Returns:
        Path: out/images/{page_stem}-{prompt_hash}.txt
    """
    return IMAGES_DIR / f'{page_stem}-{prompt_hash}.txt'


def get_image_path(page_stem: str, prompt_hash: str) -> Path:
    """Get path for image file in shared images directory.

    Args:
        page_stem: The page identifier (e.g., "p01-arthur-cullan")
        prompt_hash: The 5-char prompt hash

    Returns:
        Path: out/images/{page_stem}-{prompt_hash}.jpg
    """
    return IMAGES_DIR / f'{page_stem}-{prompt_hash}.jpg'


def find_existing_image(page_stem: str, prompt_hash: str) -> Path | None:
    """Find an existing image with matching page stem and prompt hash.

    Looks in the shared out/images/ directory.

    Args:
        page_stem: The page identifier (e.g., "p01-arthur-cullan")
        prompt_hash: The 5-char prompt hash

    Returns:
        Path to existing image if found, None otherwise.
    """
    expected_path = get_image_path(page_stem, prompt_hash)

    if expected_path.exists():
        return expected_path

    return None


def get_git_commit() -> str:
    """Get the current git commit hash (short form, 7 chars)."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short=7', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return 'unknown'


def read_manifest(version: int) -> dict | None:
    """Read the manifest for a specific version.

    Returns None if manifest doesn't exist.
    """
    manifest_path = get_version_path(version) / 'manifest.yaml'

    if not manifest_path.exists():
        return None

    with open(manifest_path) as f:
        return yaml.safe_load(f)


def write_manifest(version: int, data: dict) -> None:
    """Write or update the manifest for a specific version.

    Creates the version folder if it doesn't exist.
    """
    version_path = get_version_path(version)
    version_path.mkdir(parents=True, exist_ok=True)

    manifest_path = version_path / 'manifest.yaml'

    with open(manifest_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def create_new_version(message: str, style: str) -> int:
    """Create a new version folder with initial manifest.

    Args:
        message: User-provided commit message
        style: Style ID being used

    Returns:
        The new version number
    """
    new_version = get_latest_version() + 1

    manifest = {
        'version': new_version,
        'created': datetime.now(timezone.utc).isoformat(),
        'commit': get_git_commit(),
        'message': message,
        'style': style,
        'images': {},
        'books': [],
    }

    write_manifest(new_version, manifest)
    return new_version


def update_manifest_image(version: int, page_stem: str, filename: str, prompt_hash: str) -> None:
    """Add or update an image entry in the manifest (thread-safe)."""
    with _manifest_lock:
        manifest = read_manifest(version)
        if manifest is None:
            raise ValueError(f"No manifest found for version {version}")

        manifest['images'][page_stem] = {
            'file': filename,
            'prompt_hash': prompt_hash,
        }

        write_manifest(version, manifest)


def update_manifest_book(version: int, book_filename: str) -> None:
    """Add a book to the manifest if not already present (thread-safe)."""
    with _manifest_lock:
        manifest = read_manifest(version)
        if manifest is None:
            raise ValueError(f"No manifest found for version {version}")

        if book_filename not in manifest['books']:
            manifest['books'].append(book_filename)

        write_manifest(version, manifest)
