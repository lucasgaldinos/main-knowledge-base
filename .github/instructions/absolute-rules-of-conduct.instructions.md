---
applyTo: '**'
description: Organize the workspace following best practices.
title: Absolute Rules Of Conduct.Instruction
status: draft
created: '2025-09-10'
updated: '2025-09-15'
tags:
- .github
- /
- AI knowledge base
- Documents
- StudiesVault v2
---

- you shall NEVER use `2>/dev/null || true` or similar to hide errors.
- you must ALWAYS review your Agent/mcp tool usage before proceeding.
- you must ALWAYS think step by step and write down your reasoning.
- you must ALWAYS create a Tree of thoughts (ToT) and for each of them a Chain of thought.
- you must ALWAYS generate the document from deep-research with sources after the deep-research. YOU SHALL NEVER skip the document generation step
  - generate it in the appropriate folder.
- you must ALWAYS follow script standardization guidelines: Python for complex logic (>50 lines), Shell for simple operations (<50 lines).
- you must ALWAYS use UV environment for Python script execution: `uv run script.py` instead of direct Python execution.
- you must ALWAYS declare Python dependencies in pyproject.toml with appropriate version constraints for UV compatibility.
- you must ALWAYS use standardized interfaces: --verbose, --dry-run, --help flags and proper exit codes (0=success, 1=error, 2=invalid usage).
- you must ALWAYS validate script complexity and migrate when thresholds are exceeded.
- Every time you generate a script, you must ALWAYS maintain one single language type.
- **Every time you use `think` command, you must break down the task into detailed steps and preselect your tools.**
