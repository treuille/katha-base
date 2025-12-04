#!/usr/bin/env python3
"""
Streamlit app for merging picture book versions.

Allows interactive selection of images from multiple versions to create
a merged "best-of" version with PDFs for all 6 characters.

State is persisted in the manifest file so work can be resumed after disconnection.

Usage:
    uv run streamlit run scripts/merge_app.py
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Add parent directory to path so we can import from scripts package
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import versioning
from scripts.gen_book import (
    _create_character_pdfs,
    _get_characters_from_stem,
    CHILDREN,
    STORY_DIR,
)

# Page configuration
st.set_page_config(
    page_title="Version Merger",
    page_icon="📚",
    layout="wide",
)


# =============================================================================
# Helper Functions
# =============================================================================


def load_all_versions() -> dict[int, dict]:
    """Load manifests for all existing versions."""
    versions = {}
    latest = versioning.get_latest_version()
    for v in range(1, latest + 1):
        manifest = versioning.read_manifest(v)
        if manifest:
            versions[v] = manifest
    return versions


def get_in_progress_merges(all_versions: dict[int, dict]) -> list[int]:
    """Find versions that are in-progress merges (style=merged, books=[])."""
    return [
        v
        for v, manifest in all_versions.items()
        if manifest.get("style") == "merged" and not manifest.get("books")
    ]


def get_non_merged_versions(all_versions: dict[int, dict]) -> dict[int, dict]:
    """Get versions that can be used as sources (not merged versions)."""
    return {
        v: manifest
        for v, manifest in all_versions.items()
        if manifest.get("style") != "merged"
    }


def get_all_page_stems() -> list[str]:
    """Get all unique page stems from the story directory."""
    if not STORY_DIR.exists():
        return []
    return sorted([p.stem for p in STORY_DIR.glob("p*.yaml")])


def get_pages_for_character(character: str) -> list[str]:
    """Get sorted list of page stems for a character."""
    if not STORY_DIR.exists():
        return []

    pages = []
    for page_file in sorted(STORY_DIR.glob("p*.yaml")):
        stem = page_file.stem
        characters = _get_characters_from_stem(stem)
        if character in characters:
            pages.append(stem)
    return pages


def create_merge_version(message: str) -> int:
    """Create a new in-progress merge version."""
    new_version = versioning.get_latest_version() + 1
    manifest = {
        "version": new_version,
        "created": datetime.now(timezone.utc).isoformat(),
        "commit": versioning.get_git_commit(),
        "message": message,
        "style": "merged",
        "source_versions": [],
        "images": {},
        "books": [],
    }
    versioning.write_manifest(new_version, manifest)
    return new_version


def update_source_versions(version: int, source_versions: list[int]):
    """Update the source_versions list in manifest."""
    manifest = versioning.read_manifest(version)
    if manifest:
        manifest["source_versions"] = source_versions
        versioning.write_manifest(version, manifest)


def select_image(
    version: int, page_stem: str, source_version: int, filename: str, prompt_hash: str
):
    """Record an image selection in the manifest."""
    manifest = versioning.read_manifest(version)
    if manifest:
        manifest["images"][page_stem] = {
            "file": filename,
            "prompt_hash": prompt_hash,
            "source_version": source_version,
        }
        versioning.write_manifest(version, manifest)


def clear_image_selection(version: int, page_stem: str):
    """Remove an image selection from the manifest."""
    manifest = versioning.read_manifest(version)
    if manifest and page_stem in manifest.get("images", {}):
        del manifest["images"][page_stem]
        versioning.write_manifest(version, manifest)


def generate_pdfs(version: int):
    """Generate all 6 character PDFs from manifest selections."""
    manifest = versioning.read_manifest(version)
    if not manifest:
        return

    image_paths = {
        stem: versioning.IMAGES_DIR / info["file"]
        for stem, info in manifest["images"].items()
    }
    _create_character_pdfs(image_paths, version, CHILDREN)


def generate_character_pdf(version: int, character: str):
    """Generate PDF for a single character from manifest selections."""
    manifest = versioning.read_manifest(version)
    if not manifest:
        return

    image_paths = {
        stem: versioning.IMAGES_DIR / info["file"]
        for stem, info in manifest["images"].items()
    }
    _create_character_pdfs(image_paths, version, [character])


def get_image_for_page(
    page_stem: str, source_version: int, all_versions: dict[int, dict]
) -> Path | None:
    """Get the image path for a page from a specific version."""
    manifest = all_versions.get(source_version)
    if not manifest:
        return None

    image_info = manifest.get("images", {}).get(page_stem)
    if not image_info:
        return None

    image_path = versioning.IMAGES_DIR / image_info["file"]
    if not image_path.exists():
        return None

    return image_path


# =============================================================================
# Session State Initialization
# =============================================================================


def init_session_state():
    """Initialize session state with defaults."""
    if "all_versions" not in st.session_state:
        st.session_state.all_versions = load_all_versions()
    if "active_merge_version" not in st.session_state:
        st.session_state.active_merge_version = None


# =============================================================================
# UI Components
# =============================================================================


def render_initial_screen():
    """Render the initial screen for selecting or creating a merge."""
    st.title("📚 Version Merger")
    st.write(
        "Select images from multiple versions to create a merged 'best-of' version."
    )

    all_versions = st.session_state.all_versions
    in_progress = get_in_progress_merges(all_versions)

    # Build options for selectbox
    options = ["➕ Start New Merge"]
    for v in sorted(in_progress):
        manifest = all_versions[v]
        msg = manifest.get("message", "")[:40]
        options.append(f"v{v:02d}: {msg}")

    st.subheader("Resume or Start New")

    selected = st.selectbox(
        "Choose an action", options, index=0, label_visibility="collapsed"
    )

    if selected == "➕ Start New Merge":
        # Show form to create new merge
        st.write("---")
        st.subheader("Create New Merge")

        message = st.text_input(
            "Version message",
            placeholder="Describe this merged version...",
            key="new_merge_message",
        )

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Create", type="primary", disabled=not message.strip()):
                new_version = create_merge_version(message.strip())
                st.session_state.all_versions = load_all_versions()
                st.session_state.active_merge_version = new_version
                st.rerun()
    else:
        # Resume existing merge
        # Extract version number from "v##: message"
        match = re.match(r"v(\d+):", selected)
        if match:
            version = int(match.group(1))

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Resume", type="primary"):
                    st.session_state.active_merge_version = version
                    st.rerun()

            # Show some info about the selected merge
            manifest = all_versions[version]
            st.write("---")
            st.write(f"**Message:** {manifest.get('message', 'N/A')}")
            st.write(f"**Created:** {manifest.get('created', 'N/A')[:19]}")
            source_versions = manifest.get("source_versions", [])
            if source_versions:
                st.write(
                    f"**Source versions:** {', '.join(f'v{v:02d}' for v in source_versions)}"
                )
            num_selected = len(manifest.get("images", {}))
            total_pages = len(get_all_page_stems())
            st.write(f"**Progress:** {num_selected} of {total_pages} pages selected")


def render_sidebar():
    """Render the sidebar with source version selection."""
    version = st.session_state.active_merge_version
    manifest = st.session_state.all_versions.get(version, {})

    st.sidebar.title(f"v{version:02d}")
    st.sidebar.caption(manifest.get("message", ""))

    # Back button
    if st.sidebar.button("← Back", use_container_width=True):
        st.session_state.active_merge_version = None
        st.rerun()

    st.sidebar.divider()

    # Source version selection
    st.sidebar.subheader("Source Versions")
    st.sidebar.caption("Select 2+ versions to compare")

    non_merged = get_non_merged_versions(st.session_state.all_versions)

    if not non_merged:
        st.sidebar.warning("No source versions available")
        return

    # Get currently selected source versions from manifest
    current_sources = manifest.get("source_versions", [])

    # Build dataframe with Select column pre-populated from manifest
    version_rows = []
    for v in sorted(non_merged.keys()):
        m = non_merged[v]
        version_rows.append(
            {
                "Select": v in current_sources,  # Pre-select if in manifest
                "Ver": f"{v:02d}",
                "Message": (m.get("message", "") or "")[:20],
                "Img": len(m.get("images", {})),
                "_version": v,  # Hidden column for lookup
            }
        )

    df = pd.DataFrame(version_rows)

    # Use data_editor with checkbox column for selection
    edited_df = st.sidebar.data_editor(
        df[["Select", "Ver", "Message", "Img"]],
        column_config={
            "Select": st.column_config.CheckboxColumn(
                "Select",
                help="Select this version as a source",
                default=False,
            ),
            "Ver": st.column_config.TextColumn("Ver", disabled=True),
            "Message": st.column_config.TextColumn("Message", disabled=True),
            "Img": st.column_config.NumberColumn("Img", disabled=True),
        },
        hide_index=True,
        use_container_width=True,
        key=f"source_version_editor_{version}",
    )

    # Get selected versions from edited dataframe
    selected_indices = edited_df[edited_df["Select"]].index.tolist()
    selected_versions = [version_rows[i]["_version"] for i in selected_indices]

    # Update manifest if selection changed
    if set(selected_versions) != set(current_sources):
        update_source_versions(version, selected_versions)
        st.session_state.all_versions = load_all_versions()

        # Check if any current selections are from deselected versions
        current_images = manifest.get("images", {})
        for page_stem, info in list(current_images.items()):
            if info.get("source_version") not in selected_versions:
                clear_image_selection(version, page_stem)

        st.session_state.all_versions = load_all_versions()
        st.rerun()

    st.sidebar.divider()

    # Character selector in sidebar
    st.sidebar.subheader("Character")
    source_versions = manifest.get("source_versions", [])
    character_disabled = len(source_versions) < 2

    character = st.sidebar.selectbox(
        "Select character",
        CHILDREN,
        format_func=lambda x: x.title(),
        key="character_selector",
        disabled=character_disabled,
        label_visibility="collapsed",
    )

    if character_disabled:
        st.sidebar.caption("Select 2+ source versions first")

    # Progress tracking in sidebar
    st.sidebar.divider()
    st.sidebar.subheader("Progress")
    all_pages = get_all_page_stems()
    total_pages = len(all_pages)
    current_selections = st.session_state.all_versions.get(version, {}).get(
        "images", {}
    )
    selected_pages = len(current_selections)

    if total_pages > 0:
        progress = selected_pages / total_pages
        st.sidebar.progress(progress)
        st.sidebar.caption(f"{selected_pages} of {total_pages} pages selected")

        # Character-specific progress (if a character is selected)
        if "character_selector" in st.session_state and not character_disabled:
            character = st.session_state.character_selector
            character_pages = get_pages_for_character(character)
            char_total = len(character_pages)
            char_selected = sum(1 for p in character_pages if p in current_selections)
            if char_total > 0:
                char_progress = char_selected / char_total
                st.sidebar.progress(char_progress)
                char_remaining = char_total - char_selected
                if char_remaining > 0:
                    st.sidebar.caption(
                        f"{character.title()}: {char_remaining} remaining"
                    )
                    # Find first unselected page and add jump button
                    first_unselected = next(
                        (p for p in character_pages if p not in current_selections),
                        None,
                    )
                    if first_unselected:
                        if st.sidebar.button(
                            "Jump to next unselected",
                            use_container_width=True,
                            type="primary",
                        ):
                            st.session_state.scroll_to = first_unselected
                            st.rerun()
                else:
                    st.sidebar.caption(f"{character.title()}: complete")
                    # Show button to generate this character's PDF early
                    if st.sidebar.button(
                        f"Generate {character.title()} PDF",
                        use_container_width=True,
                        type="primary",
                    ):
                        with st.spinner(f"Generating {character.title()}'s PDF..."):
                            generate_character_pdf(version, character)
                            st.session_state.all_versions = load_all_versions()
                        st.balloons()
                        st.sidebar.success(f"{character.title()}'s PDF generated!")

        # Generate All PDFs button (always visible, enabled when all pages selected)
        all_pages = get_all_page_stems()
        total_pages = len(all_pages)
        current_selections = st.session_state.all_versions.get(version, {}).get(
            "images", {}
        )
        selected_pages = len(current_selections)
        all_selected = selected_pages == total_pages
        remaining = total_pages - selected_pages

        help_text = None if all_selected else f"Select {remaining} more images first"

        if st.sidebar.button(
            "Generate All PDFs",
            use_container_width=True,
            type="primary" if all_selected else "secondary",
            disabled=not all_selected,
            help=help_text,
        ):
            with st.spinner("Generating PDFs for all 6 characters..."):
                generate_pdfs(version)
                st.session_state.all_versions = load_all_versions()
            st.balloons()
            st.sidebar.success("All PDFs generated!")

    # Preview settings
    st.sidebar.divider()
    st.sidebar.subheader("Preview")
    preview_width = st.sidebar.slider(
        "Image width",
        min_value=150,
        max_value=800,
        value=400,
        step=5,
        key="preview_width",
        help="Width of each image preview in pixels",
    )

    # System commands at the bottom
    st.sidebar.divider()
    with st.sidebar.expander("System Commands"):
        if st.button("Refresh", use_container_width=True):
            st.session_state.all_versions = load_all_versions()
            st.rerun()


def render_main_area():
    """Render the main area with image comparison."""
    version = st.session_state.active_merge_version
    manifest = st.session_state.all_versions.get(version, {})
    source_versions = manifest.get("source_versions", [])
    current_selections = manifest.get("images", {})

    st.title("Image Selection")

    # Check if we have enough source versions
    if len(source_versions) < 2:
        st.info(
            "Select at least 2 source versions in the sidebar to begin comparing images."
        )
        return

    # Get character from sidebar selector
    if "character_selector" not in st.session_state:
        st.info("Select a character in the sidebar.")
        return

    character = st.session_state.character_selector

    # Get pages for this character
    character_pages = get_pages_for_character(character)

    if not character_pages:
        st.warning(f"No pages found for {character}")
        return

    # Display each page
    for i, page_stem in enumerate(character_pages):
        # Determine the next page stem for scrolling
        next_page_stem = (
            character_pages[i + 1] if i + 1 < len(character_pages) else None
        )
        render_page_comparison(
            page_stem, source_versions, current_selections, version, next_page_stem
        )

    # Handle scroll-to after selection
    if "scroll_to" in st.session_state and st.session_state.scroll_to:
        scroll_target = st.session_state.scroll_to
        st.session_state.scroll_to = None
        components.html(
            f"""
            <script>
                const target = window.parent.document.getElementById("{scroll_target}");
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            </script>
            """,
            height=0,
        )


def render_page_comparison(
    page_stem: str,
    source_versions: list[int],
    current_selections: dict,
    merge_version: int,
    next_page_stem: str | None = None,
):
    """Render the image comparison for a single page using horizontal flex layout."""
    # Create an anchor for this page
    st.markdown(f'<div id="{page_stem}"></div>', unsafe_allow_html=True)

    # Check if this page is already selected
    current_selection = current_selections.get(page_stem)
    selected_source = (
        current_selection.get("source_version") if current_selection else None
    )

    # Show page header with status indicator
    if selected_source is not None:
        st.markdown(
            f'<h3 style="color: #28a745;">✓ {page_stem}</h3>', unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<h3 style="color: #dc3545;">✗ {page_stem}</h3>', unsafe_allow_html=True
        )

    # Get available images from each source version
    available_images = []
    for src_v in sorted(source_versions):
        image_path = get_image_for_page(page_stem, src_v, st.session_state.all_versions)
        if image_path:
            manifest = st.session_state.all_versions[src_v]
            image_info = manifest.get("images", {}).get(page_stem, {})
            available_images.append(
                {
                    "version": src_v,
                    "path": image_path,
                    "message": manifest.get("message", ""),
                    "filename": image_info.get("file", ""),
                    "prompt_hash": image_info.get("prompt_hash", ""),
                }
            )

    if not available_images:
        st.error(f"No images available for this page from selected versions")
        st.divider()
        return

    # Get preview width from session state
    preview_width = st.session_state.get("preview_width", 400)

    # Use horizontal flex container for images
    flex_container = st.container(horizontal=True, gap="medium")

    for img_data in available_images:
        is_selected = selected_source == img_data["version"]

        # Each image in its own container with fixed width
        with flex_container:
            img_container = st.container(width=preview_width, border=is_selected)

            with img_container:
                # Version label
                label = f"**v{img_data['version']:02d}**"
                if is_selected:
                    label += " ✓"
                st.markdown(label)

                # Display image
                st.image(str(img_data["path"]), use_container_width=True)

                # Version message as caption
                if img_data["message"]:
                    st.caption(img_data["message"][:40])

                # Selection button
                button_label = "✓ Selected" if is_selected else "Select"
                button_type = "primary" if is_selected else "secondary"

                if st.button(
                    button_label,
                    key=f"select_{page_stem}_{img_data['version']}",
                    type=button_type,
                    use_container_width=True,
                ):
                    select_image(
                        merge_version,
                        page_stem,
                        img_data["version"],
                        img_data["filename"],
                        img_data["prompt_hash"],
                    )
                    st.session_state.all_versions = load_all_versions()
                    # Set scroll target for next page
                    if next_page_stem:
                        st.session_state.scroll_to = next_page_stem
                    st.rerun()

    st.divider()


# =============================================================================
# Main App
# =============================================================================


def main():
    """Main entry point."""
    init_session_state()

    if st.session_state.active_merge_version is None:
        # Show initial screen
        render_initial_screen()
    else:
        # Show merge UI
        render_sidebar()
        render_main_area()


if __name__ == "__main__":
    main()
