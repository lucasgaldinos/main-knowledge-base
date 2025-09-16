---
title: Migration and Maintenance Guide
description: Complete guide for system migration, maintenance, and evolution
status: active
created: 2025-09-11
updated: 2025-09-11
tags: [migration, maintenance, automation, governance]
version: 1.0.0
---

# Migration and Maintenance Guide

## Overview

This guide provides comprehensive instructions for migrating content to the academic knowledge base system, maintaining the organization over time, and evolving the framework as needs change.

## Content Migration

### Planning a Migration

#### 1. Assessment Phase

```bash
# Analyze current structure
find . -type f -name "*.md" | wc -l
find . -type d | wc -l

# Identify content categories
ls -la | grep "^d"

# Check for existing metadata
grep -r "^---" . --include="*.md" | wc -l
```

#### 2. Categorization Matrix

```
Content Type           → Target Location
─────────────────────────────────────────
Research notes         → 10-knowledge/notes/
Methods & processes    → 10-knowledge/methods/
Applications examples  → 10-knowledge/applications/
Academic literature    → 10-knowledge/literature/

Current projects       → 20-projects/active/
Finished projects      → 20-projects/completed/
Old projects          → 20-projects/archived/

Datasets              → 30-data/
Scripts/code          → 40-code/
Experiments           → 50-experiments/
Publications          → 60-manuscripts/
Presentations         → 70-presentations/
Tools & references    → resources/
Deprecated content    → 90-archive/
```

### Migration Execution

#### 1. Preparation Steps

```bash
# Create backup
git add -A && git commit -m "Pre-migration backup"

# Create target directories
mkdir -p {00-admin,10-knowledge,20-projects,30-data,40-code,50-experiments,60-manuscripts,70-presentations,resources,90-archive}

# Set up governance framework
cp -r .kb/ ./ # If not already present
```

#### 2. Content Migration Commands

```bash
# Preserve Git history with git mv
git mv old-directory/ 10-knowledge/category/

# Bulk file migration
for file in source-dir/*.md; do
    git mv "$file" "10-knowledge/notes/$(basename "$file")"
done

# Directory restructuring
git mv projects/active/* 20-projects/active/
git mv scripts/* 40-code/
git mv data/* 30-data/
```

#### 3. Post-Migration Validation

```bash
# Run all validation scripts
python3 .kb/scripts/validate_structure.py
python3 .kb/scripts/validate_metadata.py
python3 .kb/scripts/check_filenames.py

# Fix common issues
python3 40-code/organization/yaml-frontmatter-enforcer.py --fix

# Verify cross-references
grep -r "\[.*\](.*/" . --include="*.md"
```

### YAML Frontmatter Migration

#### 1. Automated Frontmatter Addition

```python
# Use the frontmatter enforcer
python3 40-code/organization/yaml-frontmatter-enforcer.py --scan
python3 40-code/organization/yaml-frontmatter-enforcer.py --fix
```

#### 2. Manual Frontmatter Template

```yaml
---
title: [Document Title]
description: [Brief description]
status: [draft|active|completed|archived]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
tags: [tag1, tag2, tag3]
version: [1.0.0]
authors: [author1, author2]
citations: [cite1, cite2]
---
```

## Daily Maintenance

### Routine Tasks

#### 1. Weekly Validation

```bash
#!/bin/bash
# Weekly maintenance script

echo "Running weekly knowledge base maintenance..."

# Structure validation
echo "Checking structure compliance..."
python3 .kb/scripts/validate_structure.py

# Metadata validation
echo "Validating metadata..."
python3 .kb/scripts/validate_metadata.py

# Filename compliance
echo "Checking filenames..."
python3 .kb/scripts/check_filenames.py

# Cross-reference validation
echo "Checking cross-references..."
grep -r "\[.*\](.*/" . --include="*.md" | grep -v "http"

echo "Maintenance complete!"
```

#### 2. Content Lifecycle Management

```bash
# Find outdated content
find . -name "*.md" -mtime +365 | head -10

# Check for draft status items over 30 days
grep -r "status: draft" . --include="*.md" | \
  xargs stat -c '%Y %n' | \
  awk '$1 < systime() - 2592000'

# Archive completed projects older than 1 year
find 20-projects/completed/ -name "*.md" -mtime +365
```

### Content Quality Assurance

#### 1. Metadata Consistency

```bash
# Check for missing titles
grep -L "title:" $(find . -name "*.md")

# Verify tag consistency
grep -h "tags:" $(find . -name "*.md") | sort | uniq -c | sort -nr

# Check status values
grep -h "status:" $(find . -name "*.md") | sort | uniq -c
```

#### 2. Link Validation

```bash
# Find broken internal links
grep -r "\[.*\](.*\.md)" . --include="*.md" | \
  awk -F: '{print $2}' | \
  sed 's/.*\[.*\](\(.*\.md\)).*/\1/' | \
  while read link; do
    if [ ! -f "$link" ]; then
      echo "Broken link: $link"
    fi
  done
```

## Advanced Maintenance

### Database Maintenance

#### 1. Knowledge Database Updates

```python
# Update knowledge database
import sqlite3
import os
from datetime import datetime

def update_knowledge_db():
    conn = sqlite3.connect('30-data/database/knowledge.db')
    cursor = conn.cursor()
    
    # Add new content entries
    for root, dirs, files in os.walk('10-knowledge'):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                # Process and update database
                # Implementation depends on schema
    
    conn.commit()
    conn.close()
```

#### 2. Citation Management

```bash
# Update bibliography
bibtex 10-knowledge/literature/library.bib

# Extract citations from content
grep -r "@[a-zA-Z]" . --include="*.md" | \
  sed 's/.*@\([a-zA-Z][a-zA-Z0-9]*\).*/\1/' | \
  sort | uniq > citations.tmp
```

### Automated Workflows

#### 1. Git Hooks Setup

```bash
# Install pre-commit hooks
cp .kb/scripts/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Pre-push validation
cp .kb/scripts/pre-push.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

#### 2. Continuous Integration

```yaml
# .github/workflows/validation.yml
name: Knowledge Base Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install -r .kb/requirements.txt
      - name: Validate structure
        run: python3 .kb/scripts/validate_structure.py
      - name: Validate metadata
        run: python3 .kb/scripts/validate_metadata.py
      - name: Check filenames
        run: python3 .kb/scripts/check_filenames.py
```

## System Evolution

### Framework Updates

#### 1. Policy Evolution

```yaml
# Update .kb/policy/kb-policy.yaml
version: "2.1.0"
updated: "2025-12-01"
changes:
  - "Added new content categories"
  - "Updated validation rules"
  - "Enhanced automation features"
```

#### 2. Schema Updates

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "version": "2.1.0",
  "title": "Enhanced Note Schema",
  "properties": {
    "title": {"type": "string"},
    "description": {"type": "string"},
    "status": {"enum": ["draft", "active", "completed", "archived", "deprecated"]},
    "priority": {"enum": ["low", "medium", "high", "critical"]},
    "category": {"type": "string"},
    "complexity": {"enum": ["beginner", "intermediate", "advanced", "expert"]}
  }
}
```

### Performance Optimization

#### 1. Search Indexing

```bash
# Create search index
find . -name "*.md" -exec grep -l "tag" {} \; | \
  xargs grep -h "tags:" | \
  sed 's/tags: \[\(.*\)\]/\1/' | \
  tr ',' '\n' | \
  sort | uniq -c | sort -nr > tag-index.txt
```

#### 2. Content Analytics

```python
# Generate usage statistics
import os
import yaml
from collections import Counter

def analyze_content():
    stats = {
        'total_files': 0,
        'by_status': Counter(),
        'by_category': Counter(),
        'by_tag': Counter()
    }
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                stats['total_files'] += 1
                # Parse frontmatter and update stats
    
    return stats
```

## Troubleshooting

### Common Issues

#### 1. Validation Failures

```bash
# Structure issues
python3 .kb/scripts/validate_structure.py --verbose

# Metadata problems
python3 .kb/scripts/validate_metadata.py --fix-common

# Filename violations
python3 .kb/scripts/check_filenames.py --auto-rename
```

#### 2. Performance Problems

```bash
# Large file detection
find . -name "*.md" -size +1M

# Deep directory nesting
find . -type d | awk -F/ 'NF > 6 {print NF-1, $0}' | sort -nr

# Orphaned files
find . -name "*.md" ! -path "./.git/*" ! -path "./.kb/*" | \
  xargs grep -L "^---"
```

### Recovery Procedures

#### 1. Structure Recovery

```bash
# Reset to last good state
git log --oneline -10
git reset --hard [commit-hash]

# Rebuild structure
python3 .kb/scripts/rebuild_structure.py

# Validate recovery
python3 .kb/scripts/validate_structure.py
```

#### 2. Data Recovery

```bash
# Backup restoration
cp -r backup/ .

# Database rebuild
python3 30-data/database/setup_databases.py

# Re-index content
python3 40-code/rebuild_indexes.py
```

## Documentation Updates

### Keeping Documentation Current

#### 1. Regular Reviews

- Monthly policy review
- Quarterly framework assessment
- Annual major updates
- User feedback integration

#### 2. Version Management

```bash
# Document version updates
git tag -a v2.1.0 -m "Framework update with enhanced automation"
git push origin v2.1.0

# Update version references
grep -r "version:" . --include="*.md" | head -5
```

This maintenance guide ensures the knowledge base remains organized, compliant, and evolving with your research needs while maintaining the high standards established by the academic framework.
