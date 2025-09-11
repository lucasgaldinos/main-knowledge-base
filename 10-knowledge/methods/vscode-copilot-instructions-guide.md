---
title: VS Code Copilot Instructions Guide
description: Comprehensive guide for GitHub Copilot custom instructions, best practices,
  and advanced usage patterns
status: active
created: '2025-09-10'
updated: '2025-09-10'
tags:
- vscode
- github-copilot
- custom-instructions
- ai-assistant
- development-workflow
- best-practices
methodology: deep-research
sources: 15
confidence: high
peer_reviewed: false
version: 1.0.0
authors:
- lucas_galdino
citations: []
---



# VS Code Copilot Instructions Guide

## Executive Summary

GitHub Copilot's custom instructions enable persistent preferences, constraints, and project context to ensure Chat and inline assistance produce output matching engineering standards. This guide consolidates best practices, configuration patterns, and advanced usage for expert teams.

## Core Concepts

### System Architecture

- **System prompt layer**: Custom instructions act as persistent system layer shaping Copilot Chat's default behavior
- **Context layer**: Multiple context providers (selected code, open files, @workspace index, symbols, #file/#symbol mentions)
- **Tool layer**: Participants (@workspace, @terminal, @vscode, @github) with explicit permissions and constraints

### VS Code Copilot Toolsets

#### Available Participants

- **@workspace**: Repository search and citations for cross-file understanding and refactors
- **@vscode**: VS Code command execution for refactors, formatting, file operations
- **@terminal**: Shell command proposals with review approval for scaffolding and testing
- **@github**: Issue/PR interaction (Business/Enterprise) for descriptions and context linking

#### Slash Commands

Common commands include:

- `/explain` - Code explanation and documentation
- `/tests` - Test generation and validation
- `/fix` - Bug fixes and error resolution
- `/optimize` - Performance improvements
- `/doc` - Documentation generation

## Best Practices for Custom Instructions

### 1. Outcome-Focused Design

```yaml
# Good: Specify measurable outcomes
- "Tests created/updated, docs added, no TODOs/PLACEHOLDERs"
- "Performance budgets maintained"
- "Acceptance criteria met"

# Bad: Style-only instructions
- "Use clean code"
- "Follow best practices"
```

### 2. Compact and Layered Structure

**Target**: 200-600 words with clear sections:

- Response contract
- Code style
- Language/framework defaults
- Tool permissions
- Testing/documentation requirements
- Safety & privacy

### 3. Response Contract Definition

```markdown
Response contract:
- Default output: minimal rationale (≤5 lines) + single fenced code block
- No placeholders or TODOs
- Include "Assumptions" and "Validation steps" for complex tasks
- Multi-file edits require plan approval first
```

### 4. Project Signal Integration

```yaml
Bind to real signals:
- Package manager: "pnpm workspace scripts"
- Linters: "ESLint + Prettier configured per package"
- Test frameworks: "Vitest for libraries, Jest for legacy"
- Runtime: "Node 20+, TS strict mode"
```

### 5. Tool Permission Management

```markdown
Tool permissions:
- @terminal: Allow formatting/tests, require approval for destructive ops
- @vscode: Allow safe refactors, require previews for multi-file edits
- @workspace: Encouraged for citations and code navigation
```

## Configuration Patterns

### Scope Management

1. **User Scope**: Personal preferences via Copilot Chat settings (syncs across devices)
2. **Workspace Scope**: Project standards in `.vscode/settings.json` (version controlled)
3. **Profile-Based**: Different instruction sets per VS Code profile (Backend/Frontend/Docs)

### Workspace Configuration Example

```json
// .vscode/settings.json
{
  "github.copilot.chat.welcomeMessage": "never",
  "github.copilot.chat.localeOverride": "en",
  "github.copilot.chat.templateVariables": {
    "PROJECT_TYPE": "TypeScript/React monorepo",
    "PACKAGE_MANAGER": "pnpm",
    "TEST_FRAMEWORK": "Vitest/Jest"
  }
}
```

## Language-Specific Instruction Templates

### TypeScript/React Monorepo

```markdown
Context: Monorepo with packages/* using pnpm. Node 20+, TS strict, ESLint + Prettier, Vitest/Jest, React 18, Vite.

Instructions:
- TypeScript everywhere with strict mode compliance
- Functional components + hooks, React Query for data fetching
- pnpm workspace scripts preferred over package-level
- Vitest for libraries, Jest for legacy packages
- Trust ESLint + Prettier, no formatted diffs
- Update tsconfig references for new packages
```

### Python FastAPI Service

```markdown
Context: Python 3.11, FastAPI, Pydantic v2, Ruff + Black, Pytest, uv/Poetry packaging.

Instructions:
- Type hints + Pydantic models, validate at boundary
- Dependency injection with FastAPI Depends
- HTTPException with structured logging for errors
- Async tests with httpx.AsyncClient for endpoints
- Prefer async I/O libraries (aioboto3, asyncpg)
- Respect pyproject.toml packaging choices
```

### Go Service

```markdown
Context: Go 1.22+, modules enabled, staticcheck/golangci-lint, testing + testify, Wire/fx DI.

Instructions:
- Explicit error handling with fmt.Errorf wrapping
- Small package APIs, avoid name stuttering
- Table-driven tests with testify assertions
- Context propagation, avoid goroutine leaks
- Respect go.mod constraints, justify heavy deps
```

## Advanced Usage Patterns

### Plan-and-Apply Multi-File Edits

```markdown
Workflow:
1. Request explicit plan (files, risks, tests)
2. Review and approve plan
3. Apply edits incrementally with previews
4. Run tests between iterations
5. Validate outcomes

Guardrail: "For multi-file changes, propose plan with file paths and rationale. Wait for approval."
```

### Test-Driven Development

```markdown
TDD Pattern:
1. Use /tests to bootstrap coverage
2. Request "failing tests first" for new features
3. Generate code to pass tests
4. Run tests via @terminal with project commands
5. Report failures succinctly for iteration
```

### Performance Optimization

```markdown
Optimization Workflow:
1. Use /optimize for micro-optimizations
2. Request measurement plans (benchmarks, profiling)
3. Guard against regressions with tests
4. Encourage realistic datasets
5. Validate improvements before commit
```

## Security and Governance

### Safety Guidelines

```markdown
Security requirements:
- Never generate secrets or credentials
- Use environment variables for sensitive data
- Prefer licenses compatible with repository
- No hardcoded tokens or API keys
- Reference secret managers abstractly
```

### Team Adoption Strategy

1. **Start Small**: Basic workspace instructions with clear outcomes
2. **Gather Feedback**: Iterate based on team experience
3. **Expand Gradually**: Add language-specific and role-specific guidance
4. **Measure Impact**: Track PR lead time, review cycles, test coverage

### Maintenance Practices

- Treat instructions as code (PR reviews for changes)
- Update after framework/dependency changes
- Quarterly instruction audits and optimization
- Team playbook integration with common patterns

## Effectiveness Measurement

### Quantitative Metrics

- PR lead time reduction
- Review cycle efficiency
- Unit test coverage improvements
- Lint error reduction per change
- Mean time to resolve defects

### Qualitative Assessment

- Reviewer satisfaction scores
- Code readability improvements
- Correctness perception
- Team adoption rates
- Learning curve acceleration

## Anti-Patterns to Avoid

### Common Mistakes

1. **Overlong Instructions**: Reduces token budget, increases hallucinations
2. **Contradictory Rules**: Conflicts between instruction sections
3. **One-Size-Fits-All**: Single approach for polyglot repositories
4. **Blind Tool Acceptance**: Automatic approval of @terminal proposals
5. **Static Instructions**: Never updating after project evolution

### Failure Modes

- Instructions contradicting repository configurations
- Overfitting to single language in multilingual projects
- Ignoring workspace index drift after refactors
- Security policy violations in generated code
- Inconsistent output formats across team members

## Complete Instruction Template

```markdown
You are GitHub Copilot assisting senior engineers on this repository. Follow these rules unless repository configuration contradicts them.

## Response Contract
- Default: minimal rationale (≤5 lines) + single fenced code block
- No placeholders or TODOs
- Complex tasks: append "Assumptions" and "Validation steps"
- Multi-file edits: show plan, request permission

## Code Style and Conventions
- Infer from repository configs (linters/formatters/tsconfig)
- Repository configs override these instructions
- Prefer composable functions, clear names, strong typing
- Early returns, minimal cognitive complexity

## Tools and Actions
- @workspace: encouraged for code navigation/citations
- @terminal: safe operations default, ask before destructive ops
- @vscode: format/rename approved, preview multi-file edits
- Present dry-run plans for stateful operations

## Testing and Documentation
- Include/update tests when modifying behavior
- Use repository's test framework with realistic fixtures
- Maintain docstrings and update README/CHANGELOG
- Generate runnable examples in documentation

## Security and Compliance
- Never introduce secrets or credentials
- Use environment variables and secret managers
- Ensure license compatibility
- Validate against security policies

## Context Requirements
- Ask clarifying questions when context insufficient
- Request relevant files (#file) before proceeding
- Cite specific files/symbols in responses
- Maintain accuracy in cross-references
```

## Implementation Checklist

### Pre-Implementation

- [ ] Audit current development workflow pain points
- [ ] Identify team's primary languages and frameworks
- [ ] Document existing linting and formatting configurations
- [ ] Establish success metrics and measurement approach

### Configuration

- [ ] Set up workspace-scoped instructions in `.vscode/settings.json`
- [ ] Configure user-scoped personal preferences
- [ ] Create role-specific VS Code profiles if needed
- [ ] Test instruction effectiveness with sample tasks

### Validation

- [ ] Verify tool permissions work as expected
- [ ] Test multi-file edit workflows
- [ ] Validate security compliance in generated code
- [ ] Confirm integration with existing CI/CD pipelines

### Ongoing Maintenance

- [ ] Schedule quarterly instruction reviews
- [ ] Track effectiveness metrics
- [ ] Update instructions after major dependency changes
- [ ] Gather team feedback and iterate

## Conclusion

Well-crafted custom instructions transform GitHub Copilot from a clever assistant to a reliable teammate that understands your project's context, constraints, and quality standards. Success requires treating instructions as living documentation that evolves with your codebase and team practices.

The key is starting with a minimal, enforceable baseline and iterating based on real usage patterns and measurable outcomes. Focus on encoding your team's actual workflow signals rather than generic best practices, and always maintain the balance between guidance and flexibility.

## References

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Copilot Extension Guide](https://code.visualstudio.com/docs/copilot/overview)
- [Copilot Chat Participants Reference](https://code.visualstudio.com/docs/copilot/copilot-chat)
- [VS Code Settings Sync Documentation](https://code.visualstudio.com/docs/editor/settings-sync)
- [Custom Instructions Best Practices](https://github.blog/2024-06-27-how-to-write-better-prompts-for-github-copilot/)
