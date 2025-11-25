# Katha Base

A storybook generation system for creating illustrated story pages.

## Project Structure

```
katha-base/
├── lib/              # Reusable system components
│   ├── scripts/      # Image generation and processing scripts
│   └── templates/    # YAML templates and prompt templates
│
└── content/          # Story-specific content
    ├── ref-images/   # Reference images for visual style
    └── out-images/   # Generated illustrations (git-ignored)
```

### lib/

Contains the abstract framework - scripts, templates, and tools that define how the storybook generation system works. These components are reusable across different stories.

### content/

Contains the particular content for your specific story - world definitions, character descriptions, story pages, reference images, and generated outputs.

