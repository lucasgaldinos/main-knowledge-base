---
title: VS Code Toolsets Comprehensive Guide
description: Best practices for Python development, data science, academic writing, and general productivity in VS Code
status: active
created: 2025-01-11
updated: 2025-01-11
tags:
  - vscode
  - toolsets
  - python
  - data-science
  - academic-writing
  - productivity
  - best-practices
version: 1.0.0
authors:
  - lucas_galdino
citations:
  - VS Code Documentation
  - Python Development Best Practices
  - Data Science Workflows
  - Academic Writing Guides
---

# VS Code Toolsets Comprehensive Guide

## Table of Contents

1. [Introduction](<#introduction>)
2. [Guiding Principles](<#guiding-principles>)
3. [Profiles and Workspaces](<#profiles-and-workspaces>)
4. [Python Development Best Practices](<#python-development-best-practices>)
5. [Data Science Workflows](<#data-science-workflows>)
6. [Academic Writing and Reproducible Documents](<#academic-writing-and-reproducible-documents>)
7. [General Productivity](<#general-productivity>)
8. [Extension Recommendations](<#extension-recommendations>)
9. [Configuration Examples](<#configuration-examples>)
10. [Automation and CI/CD](<#automation-and-cicd>)
11. [Security and Compliance](<#security-and-compliance>)
12. [Troubleshooting and Performance](<#troubleshooting-and-performance>)
13. [References](<#references>)

## Introduction

Visual Studio Code can be configured as a cohesive, high-performance environment spanning Python software engineering, data science, academic writing, and general productivity. This guide provides a deeply integrated blueprint for achieving a seamless development experience.

### Key Objectives

- **Standardize Toolchains**: Use modern, fast, and integrated tools
- **Isolate Environments**: Keep toolchains reproducible with profiles and containers
- **Automate Workflows**: Encode conventions into tasks, pre-commit hooks, and CI
- **Enhance Productivity**: Leverage VS Code features for navigation, debugging, and collaboration

### Target Audience

- Python Developers
- Data Scientists
- Academic Researchers
- Anyone looking to optimize their VS Code setup for productivity

## Guiding Principles

- **Single Source of Truth**: Centralize configuration in `pyproject.toml`, `.vscode/`, and `devcontainer.json`
- **Reproducibility First**: Prefer hermetic environments (devcontainers, uv, micromamba)
- **Fast Feedback**: On-save formatting, on-type diagnostics, and quick-launch tests
- **Notebook Discipline**: Keep runtime state deterministic and version control clean
- **Minimal Viable Toolchain**: Fewer, faster, modern tools outperform sprawling stacks
- **Automation Over Documentation**: Encode conventions into tasks and CI

## Profiles and Workspaces

Use VS Code Profiles to curate extensions, settings, and UI for distinct activities:

- **Python Engineering**: Python, Pylance, Ruff, GitLens, Test Explorer, Error Lens, Docker/Dev Containers
- **Data Science**: Jupyter, Data Wrangler, Plotly, SQLTools, DVC/MLflow extensions
- **Academic Writing**: Quarto, LaTeX Workshop, Markdown All in One, LanguageTool, Citations
- **General Productivity**: GitHub Pull Requests, Todo Tree, Bookmarks, REST Client

Pin workspace-recommended extensions in `.vscode/extensions.json` and use workspace settings to avoid polluting user settings.

## Python Development Best Practices

### Environment and Packaging

- **`uv` (Astral)**: Recommended for speed and simplicity (`uv init`, `uv add`, `uv lock`)
- **Alternatives**: `rye`, `poetry`, `micromamba`/`conda`
- **Configuration**: Centralize in `pyproject.toml` for `ruff`, `black`, `pytest`, etc.

**Example `pyproject.toml` for `ruff`:**

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "UP", "B", "N", "C90"]
ignore = ["E203", "W503"]
fix = true

[tool.ruff.isort]
known-first-party = ["your_package"]
```

### Linting, Formatting, and Types

- **`ruff`**: Linter, import sorter, and optional formatter
- **`black`**: Dedicated formatter for byte-for-byte consistency
- **`Pylance` / `pyright`**: Static type checking (`strict` mode recommended)
- **`mypy`**: For complex typing scenarios, run in CI

### Testing and Coverage

- **`pytest`**: Test framework with parametrization, markers, and fixtures
- **`coverage.py`**: Code coverage analysis via `pytest-cov`
- **`Hypothesis`**: Property-based testing
- **VS Code Integration**: Use Test Explorer for discovery, execution, and debugging

**Example `tasks.json` for testing:**

```json
{
  "label": "test",
  "type": "shell",
  "command": "uv run pytest -q --cov=your_package --cov-report=term-missing",
  "problemMatcher": "$pytest-stone"
}
```

### Debugging and Profiling

- **Debugging**: `launch.json` with configurations for modules, tests, and apps
- **Profiling**: `py-spy`, `scalene`, `cProfile` + `snakeviz`
- **VS Code Integration**: Use built-in debugger and profiling UI

### Reproducibility and CI

- **`pre-commit` hooks**: `ruff`, `black`, `nbstripout`, `codespell`
- **CI (GitHub Actions)**: `uv install`, `ruff check`, `pytest`, `pyright`
- **`.editorconfig`**: For consistent line endings, indentation, and charset

## Data Science Workflows

### Notebooks vs. Scripts

- **`.py` percent cells (`# %%`)**: For exploratory work with clean VCS diffs
- **`jupytext`**: Sync notebooks to `.py` or `.qmd` for version control
- **`nbQA`**: Apply `ruff`, `black`, `mypy` to notebooks
- **`nbstripout`**: Strip notebook outputs pre-commit

**Example `pre-commit-config.yaml` for notebooks:**

```yaml
repos:
  - repo: https://github.com/nbQA-dev/nbQA
    rev: 1.9.0
    hooks:
      - id: nbqa-ruff
        args: ["--fix"]
      - id: nbqa-black
      - id: nbqa-mypy
  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks: [{ id: nbstripout }]
```

### Environments and Kernels

- Match Jupyter kernel with project environment (`uv`, `conda`)
- Pin kernel in notebook metadata for reproducibility
- Use devcontainers with CUDA for GPU work

### Visualization and Data Inspection

- **Built-ins**: Variable Explorer, Data Viewer
- **`Plotly`**: Interactive charts
- **`Data Wrangler`**: Exploratory data transformation
- **`Polars`**: High-performance data wrangling

### Experiment Tracking and Data Versioning

- **`DVC`**: Data versioning
- **`MLflow` / `Weights & Biases`**: Experiment tracking
- **`Hydra` / `Pydantic Settings`**: Configuration management

## Academic Writing and Reproducible Documents

### Toolchain Options

- **`Quarto`**: Recommended for integrating Markdown, Jupyter, citations, and cross-references
- **`LaTeX Workshop`**: For native LaTeX editing with build recipes
- **`Pandoc`**: For custom document conversion pipelines

### Citations and Bibliography

- **`Zotero` + `Better BibTeX`**: For stable citekeys and bibliography management
- **`Citations` extension**: For inserting citations from Zotero

### Language Quality

- **`LanguageTool`**: Grammar and style checking
- **`Vale`**: Style linting against custom rules
- **`Code Spell Checker`**: Inline spell checking

### Reproducibility and Automation

- **`Papermill`**: Parameterize and execute notebooks
- **`tasks.json`**: Automate document builds (`quarto render`)
- **CI/CD**: Publish artifacts to GitHub Releases or Pages

## General Productivity

### Core Navigation and Editing

- **Command Palette**: `Ctrl/Cmd+Shift+P`
- **Multi-cursor**: `Alt+Click`, `Ctrl/Cmd+D`
- **Sticky Scroll** and **CodeLens**: For context-aware navigation

### Git and Reviews

- **`GitLens`**: Code authorship and history context
- **`GitHub Pull Requests and Issues`**: In-editor code reviews
- **`Conventional Commits`**: For consistent commit messages

### Tasks, Macros, and Snippets

- **`tasks.json`**: Orchestrate build, test, and lint pipelines
- **User and workspace snippets**: For common boilerplate code

### Remote Development

- **`Remote - SSH`**: For connecting to remote servers
- **`Remote - WSL`**: For Windows Subsystem for Linux
- **`Dev Containers`**: For hermetic, reproducible environments
- **`GitHub Codespaces`**: For cloud-based development

## Extension Recommendations

### Python Core

- **Python** (`ms-python.python`)
- **Pylance** (`ms-python.vscode-pylance`)
- **Ruff** (`charliermarsh.ruff`)
- **Error Lens** (`usernamehw.errorlens`)

### Data Science

- **Jupyter** (`ms-toolsai.jupyter`)
- **Data Wrangler** (`ms-toolsai.datawrangler`)
- **SQLTools** (`mtxr.sqltools`)

### Academic Writing

- **Quarto** (`quarto.quarto`)
- **LaTeX Workshop** (`James-Yu.latex-workshop`)
- **LanguageTool** (`denniske.LangTool-extension`)
- **Citations** (`usernamehw.citations`)

### Dev Environment and Ops

- **Dev Containers** (`ms-vscode-remote.remote-containers`)
- **Remote - SSH** (`ms-vscode-remote.remote-ssh`)
- **GitLens** (`eamodio.gitlens`)
- **GitHub Pull Requests and Issues** (`github.vscode-pull-request-github`)

### AI Assistants

- **GitHub Copilot** (`github.copilot`)
- **Continue** (`continue.continue`) for self-hosted models

## Configuration Examples

### `.vscode/settings.json`

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
  },
  "python.analysis.typeCheckingMode": "basic",
  "python.testing.pytestEnabled": true,
  "ruff.lint.run": "onType",
  "ruff.format": true,
  "files.exclude": {
    "**/.git": true,
    "**/.venv": true,
    "**/__pycache__": true
  }
}
```

### `.vscode/tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    { "label": "fmt", "type": "shell", "command": "uv run ruff format && uv run ruff --fix" },
    { "label": "lint", "type": "shell", "command": "uv run ruff" },
    { "label": "test", "type": "shell", "command": "uv run pytest -q" },
    { "label": "docs:quarto", "type": "shell", "command": "quarto render" }
  ]
}
```

### `.devcontainer/devcontainer.json`

```json
{
  "name": "Python Data Science",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "uv sync",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "charliermarsh.ruff",
        "ms-toolsai.jupyter"
      ],
      "settings": { "python.defaultInterpreterPath": "/usr/local/bin/python" }
    }
  }
}
```

## Automation and CI/CD

- **`just` / `make`**: For task orchestration
- **`nox` / `tox`**: For multi-environment testing
- **GitHub Actions**: For CI/CD pipelines with dependency caching
- **`semantic-release`**: For automated versioning and changelogs

## Security and Compliance

- **Workspace Trust**: Keep enabled and scrutinize untrusted repositories
- **Secrets Management**: Use `.env` files or secret managers
- **Security Scanning**: `bandit` or `Semgrep` in CI
- **Supply Chain Security**: Pin dependencies and use `Dependabot`

## Troubleshooting and Performance

### Common Pitfalls

- Mixing global and project Python environments
- Not committing lockfiles or environment specifications
- Letting notebooks accrue stateful magic
- Tool sprawl (consolidate with `ruff`)

### Performance Hygiene

- Exclude heavy folders from watchers and search (`.venv`, `__pycache__`)
- Disable or profile slow extensions
- Use workspace-scoped extension activation

## References

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Quarto Documentation](https://quarto.org/docs/guide/)
- [Dev Containers](https://containers.dev/)

---

**Note**: This guide provides a comprehensive blueprint for an optimized VS Code setup. Adapt the recommendations to your specific needs and team conventions. The key is to maintain a consistent, reproducible, and automated development environment.
