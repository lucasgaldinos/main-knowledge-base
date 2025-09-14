---
title: Git Practical Guide with Examples
description: Practical guide for Git usage, automation, and academic workflows (beginner to intermediate)
status: active
created: 2025-09-12
updated: 2025-09-12
tags:
  - git
  - version-control
  - automation
  - academic-workflows
  - pre-commit
  - VSCode
  - best-practices
version: 1.0.0
authors:
  - lucas_galdino
sources:
  - deep-research-analysis
  - official-git-documentation
  - academic-research-patterns
citations: []
---

# Git Complete Guide with Examples

## Executive Summary

This guide covers Git usage from beginner to advanced, with a focus on academic and research workflows, automation, and integration with modern tools like VS Code, DVC, and pre-commit. It includes practical command examples, configuration templates, and troubleshooting tips.

## Table of Contents

1. [Mental Model: How Git Works](<#mental-model-how-git-works>)
2. [Setup and Configuration](<#setup-and-configuration>)
3. [Beginner to Intermediate Usage Patterns](<#beginner-to-intermediate-usage-patterns>)
4. [Advanced Git Features and Patterns](<#advanced-git-features-and-patterns>)
5. [Git Hooks and Pre-commit Automation](<#git-hooks-and-pre-commit-automation>)
6. [Academic Research & Development Workflows](<#academic-research--development-workflows>)
7. [Git Automation Tools and Ecosystem](<#git-automation-tools-and-ecosystem>)
8. [Troubleshooting and Recovery](<#troubleshooting-and-recovery>)
9. [Best Practices](<#best-practices>)
10. [Git and VS Code Integration](<#git-and-vs-code-integration>)
11. [Practical Checklists](<#practical-checklists>)
12. [Command Snippets Reference](<#command-snippets-reference>)

---

## 1. Mental Model: How Git Works

- **Objects**: blob (file), tree (directory), commit (snapshot), tag (pointer)
- **References**: branches, tags, HEAD, reflog
- **Index**: staging area for next commit
- **Porcelain vs Plumbing**: user-friendly vs low-level commands

## 2. Setup and Configuration

### Global Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
git config --global init.defaultBranch main
git config --global pull.ff only
git config --global core.editor "code --wait"
git config --global commit.gpgSign true
```

### .gitignore and .gitattributes

- Use templates for your stack (Python, LaTeX, Jupyter, etc.)
- Normalize line endings: `* text=auto eol=lf` in `.gitattributes`

### Credential Management

- Use OS keychain helpers and enable 2FA

### Commit Message Template

- Use `commit.template` for consistent, rich messages

## 3. Beginner to Intermediate Usage Patterns

### Daily Flow

```bash
git clone <url>
git switch -c feat/my-feature
git add -p
git commit -v
git fetch --prune
git rebase origin/main
git push --set-upstream origin feat/my-feature
git tag -a v1.0.0 -m "..."
git push --tags
```

### Branching Policies

- Short-lived feature branches, protected main, PR review
- Use `--ff-only` for main, merge for complex integration

### Useful Commands

```bash
git log --graph --decorate --oneline --all
git diff --word-diff=color
git restore --staged <file>
git switch <branch>
```

## 4. Advanced Git Features and Patterns

### Rebase Mastery

```bash
git rebase -i origin/main
git commit --fixup <hash>
git rebase -i --autosquash
git rebase --rebase-merges
```

### Merge Strategies

- Use `ort` strategy, enable `rerere` for conflict reuse
- Set `merge.conflictStyle zdiff3` for better conflict context

### Cherry-pick, Bisect, Patch

```bash
git cherry-pick A^..B
git bisect start; git bisect bad HEAD; git bisect good <good>
git bisect run ./ci/test-regression.sh
git format-patch -n; git am; git apply
```

### Worktrees, Sparse Checkout, Partial Clone

```bash
git worktree add ../proj-feat feat/my-feature
git clone --filter=blob:none <url> proj
git -C proj sparse-checkout init --cone
git -C proj sparse-checkout set src/ docs/
```

### History Rewriting

- Use `git filter-repo` for history surgery

### Submodules vs Subtrees

- Prefer subtrees for vendored code, submodules for co-development

### Large Files and Datasets

- Use Git LFS, git-annex, or DVC for large data

### Performance

- Enable background maintenance: `git maintenance start`
- Use commit-graph, fsmonitor, and untracked cache for large repos

## 5. Git Hooks and Pre-commit Automation

### Local Hooks

- Place scripts in `.git/hooks/` (pre-commit, commit-msg, pre-push, etc.)
- Use pre-commit framework for hermetic, cross-platform hooks

#### Example `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
        args: ["--maxkb=512"]
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.4
    hooks:
      - id: ruff
        args: ["--fix"]
  - repo: https://github.com/jupyter/nbdime
    rev: 3.2.2
    hooks:
      - id: nbdime-difft
      - id: nbdime-merged
  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout
```

### Server-side Policies

- Use protected branches, required checks, signed commits/tags
- For self-hosted: pre-receive/update hooks for invariants

## 6. Academic Research & Development Workflows

### Repository Structure

```
src/           # code
notebooks/     # exploratory, outputs stripped
models/        # tracked by DVC/annex/LFS
paper/         # LaTeX/Markdown, figures, bib
ci/            # automation
env/           # environment specs
scripts/       # orchestration
```

### Branching for Experiments

- Use `exp/<topic>-<date>-<id>`
- Tag reproducible milestones, capture parameters in commit trailers

### Reproducibility

- Pin environments (uv/poetry, renv, Nix, Docker)
- Use DVC for data/artifact pipelines
- Publish with CITATION.cff, Zenodo DOIs

### Paper Writing and LaTeX

- Build PDFs in CI, attach to releases
- Lint with chktex, format with latexindent
- Use Overleaf Git bridge or mirror

### Notebooks

- Strip outputs with nbstripout
- Use nbdime for merges/diffs
- Run nbQA for code quality

### Releases and Changelogs

- Use Conventional Commits, semantic-release
- Sign tags/releases, attach artifacts

### Access Control

- Protect main, require reviews, enforce DCO/signed commits
- Use detect-secrets, rotate credentials if leaks occur

## 7. Git Automation Tools and Ecosystem

- git-town, git-machete: workflow automation
- gh (GitHub CLI), glab (GitLab CLI): PRs, releases from terminal
- jj (Jujutsu), git-branchless: modern DAG-first UIs
- Dependabot/Renovate: dependency PRs
- pre-commit.ci: run hooks in CI
- semantic-release: automated versioning/changelogs
- Danger bots: PR conventions
- DVC, Metaflow, Pachyderm: data/ML pipelines

## 8. Troubleshooting and Recovery

- Use `git reflog` to recover lost commits
- Use `git fsck` for repo health
- Use `git maintenance run` for performance
- For merge conflicts: enable `zdiff3`, use rerere, nbdime for notebooks
- For large files: migrate to LFS, remove from history with filter-repo
- For submodule issues: always run `git submodule update --init --recursive`

## 9. Best Practices

- Keep commits small, atomic, and message-rich
- Prefer rebase for private, merge for shared branches
- Never rebase public branches without coordination
- Automate formatting/linting
- Sign commits/tags, archive releases
- Document onboarding in CONTRIBUTING.md
- Regularly prune remotes, clean stale branches
- Mirror critical repos, create bundles for backup

## 10. Git and VS Code Integration

- Use Source Control view for staging, branching, stashing
- Use GitLens, Git Graph for history and authorship
- Use GitHub/GitLab extensions for PR review
- Use EditorConfig, Markdown, LaTeX, Jupyter extensions
- Run pre-commit as a VS Code Task
- Use Dev Containers for reproducible environments
- Use nbdime for notebook diffs/merges
- Use VS Code auth for GitHub/GitLab

## 11. Practical Checklists

### New Repo Bootstrap

```bash
git init
git config --local init.defaultBranch main
touch .gitignore .gitattributes LICENSE README.md CONTRIBUTING.md CITATION.cff
pre-commit install
# Set up DVC or LFS as needed
# Add CI workflows
```

### Daily Developer Loop

```bash
git fetch --prune
git worktree add ../feature feature-branch
git add -p
git commit -v
git rebase --autosquash origin/main
git push
pre-commit run --all-files
# Open PR
```

### Release

```bash
# Ensure CHANGELOG is up to date
# Bump version, sign tag
# Build and attach artifacts
# Publish, archive with DOI
```

### Emergency Recovery

```bash
git reflog
git branch rescue HEAD@{2}
git reset --hard HEAD@{1}
```

## 12. Command Snippets Reference

- Safe pull policy:
  ```bash
  git config --global pull.ff only
  git config --global pull.rebase true
  git config --global rebase.autoStash true
  ```
- One-time fixup flow:
  ```bash
  git commit --fixup=<hash>
  git rebase -i --autosquash origin/main
  ```
- Recover last state before a reset:
  ```bash
  git reflog
  git reset --hard HEAD@{1}
  ```
- Partial clone + sparse checkout:
  ```bash
  git clone --filter=blob:none <url> repo
  cd repo && git sparse-checkout init --cone
  git sparse-checkout set path1/ path2/
  ```
- Remove a secret everywhere (filter-repo):
  ```bash
  git filter-repo --path .env --invert-paths
  git push --force-with-lease --all
  git push --force-with-lease --tags
  ```
- Enforce conventional commits (commit-msg hook via commitlint in pre-commit or CI)

---

## Closing Guidance

Pick a small set of patterns and automate them. The winning combination for most academic and research teams is:

- Pre-commit hooks for formatting, linting, secrets, and notebook hygiene
- DVC or git-annex for datasets and pipelines
- Worktrees + stacked diffs for complex projects
- CI that builds tests, papers, and artifacts on every PR and release
- VS Code with GitLens, Dev Containers, and domain-specific extensions
- Signing, protected branches, and routine maintenance

Revisit your workflow quarterly; automate new pain points, keep your history clean and reproducible, and focus on high-quality, actionable commits.
