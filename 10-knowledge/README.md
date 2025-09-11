---
title: Knowledge Base
type: directory
created: 2025-01-11T19:00:00Z
status: active
---

# 10-knowledge: Consolidated Knowledge Base

This directory contains the unified knowledge base consolidating content from the previous `docs/` and `knowledge/` directories following academic best practices.

## Structure

### `notes/`

Atomic notes with unique identifiers and metadata following Zettelkasten principles:

- Format: `YYYYMMDDHHMMSS-topic-slug.md`
- Required YAML frontmatter with ID, title, created, status, tags
- Cross-linked to projects, datasets, and other notes

### `literature/`

Academic literature, papers, and reference materials:

- `library.bib` - Central BibTeX bibliography
- Organized literature reviews and summaries
- DOI and citation management

### `methods/`

Methodologies, processes, and best practices:

- Implementation guides and procedures
- Testing and validation approaches
- Documentation standards and templates

## Migration Status

This directory will consolidate content from:

- `docs/` → `10-knowledge/methods/` and `10-knowledge/literature/`
- `knowledge/` → `10-knowledge/notes/` and specialized subdirectories
- Cross-references will be updated systematically

## Naming Conventions

- All directories use kebab-case
- Notes follow timestamp-slug pattern
- Methods and literature use descriptive kebab-case names
- YAML frontmatter required for all content

## Related Directories

- `80-resources/` - Templates and reusable assets
- `20-projects/` - Project-specific documentation
- `resources/literature/` - Legacy literature (to be migrated)
