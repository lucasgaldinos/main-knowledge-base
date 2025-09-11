---
title: Task List and Priorities
description: '---'
status: draft
created: '2025-09-10'
updated: '2025-09-10'
tags:
- /
- AI knowledge base
- Documents
- StudiesVault v2
- TODO.md
version: 1.0.0
---

---
title: Task List and Priorities  
description: Academic knowledge base task management and completion status
status: completed
created: 2025-09-10
updated: 2025-09-11
tags: [todo, tasks, priorities, implementation, completed]
version: 2.0.0
---

# TODO - Academic Knowledge Base

## ✅ IMPLEMENTATION COMPLETED

All three phases of the academic knowledge base organization framework have been successfully completed:

### ✅ Phase 1: Governance Framework (COMPLETED)
- [x] Implemented comprehensive .kb/ governance structure
- [x] Created automated validation with Python scripts
- [x] Established JSON schemas for metadata validation
- [x] Set up pre-commit hooks for continuous compliance
- [x] Developed academic taxonomy (00-90 directory structure)

### ✅ Phase 2: Systematic Content Migration (COMPLETED)
- [x] Complete knowledge/ directory migration to 10-knowledge/
- [x] Migrated projects/, current-work/, and outputs/ to appropriate locations
- [x] Consolidated resources/ and tools/ documentation
- [x] Archived legacy content in 90-archive/
- [x] Updated cross-references and internal links
- [x] Validated complete migration with governance scripts

### ✅ Phase 3: Advanced Automation and User Training (COMPLETED)
- [x] Created comprehensive user documentation
- [x] Developed advanced automation scripts
- [x] Implemented continuous validation workflows
- [x] Created training materials and examples
- [x] Generated final implementation report

## ✅ Validation and Compliance (COMPLETED)
- [x] Structure validation: PASSED
- [x] Metadata consistency verified across all files
- [x] Pre-commit hooks functional and tested
- [x] Governance policy enforcement operational

## ✅ Documentation Updates (COMPLETED)
- [x] Updated all README files to reflect new structure
- [x] Created comprehensive user onboarding guide
- [x] Documented migration procedures for future use
- [x] Updated project documentation with new organization

## ✅ System Integration (COMPLETED)
- [x] Academic taxonomy structure fully operational
- [x] Enhanced maintenance tools implemented
- [x] Template system for content creation ready
- [x] Automated reporting and analytics available

## ✅ Quality Assurance (COMPLETED)
- [x] All migrated content reviewed for accuracy
- [x] No broken cross-references remaining
- [x] Tag consistency validated and maintained
- [x] Duplicate content removed or consolidated

## 🎯 FRAMEWORK NOW READY FOR PRODUCTIVE USE

The academic knowledge base organization framework is complete and operational. Users can:

1. **Create Content**: Use templates in `.kb/templates/`
2. **Maintain Quality**: Run validation scripts in `.kb/scripts/`
3. **Monitor Health**: Use enhanced maintenance tool in `40-code/`
4. **Follow Best Practices**: Reference user guide in `00-admin/`
5. **Troubleshoot Issues**: Use comprehensive documentation

## 📚 Key Resources for Users

- **Quick Start**: `00-admin/user-guide.md`
- **Templates**: `.kb/templates/` directory
- **Validation**: `python3 .kb/scripts/validate_structure.py`
- **Maintenance**: `python3 40-code/maintain_kb_enhanced.py --scan`
- **Governance**: `.kb/policy/kb-policy.yaml`

## 🔄 Ongoing Maintenance Tasks

### Daily
- Use templates for new content creation
- Run validation before commits

### Weekly  
- Execute enhanced maintenance scan
- Review and address any issues found

### Monthly
- Archive completed projects over 1 year old
- Update outdated content and metadata

### Quarterly
- Review governance policies for updates
- Assess framework performance and optimization opportunities

---

**Framework Status**: ✅ PRODUCTION READY  
**Last Updated**: September 11, 2025  
**Version**: 2.0.0 (Academic Taxonomy with Advanced Automation)  
**Implementation**: COMPLETE - Ready for productive academic use

# Task List and Priorities

## 🚀 IMMEDIATE Priority - Workspace Reorganization

- [ ] **Workspace Reorganization - Phase 1** ⚡ READY FOR IMPLEMENTATION
  - **Analysis**: ✅ Actor-critic analysis completed (15 thoughts, 7 rounds)
  - **Plan**: ✅ Comprehensive reorganization plan created in workspace-reorganization-plan.md
  - **Core Issue**: Task management files (TODO.md, TASKS.md) buried in deep hierarchy
  - **Solution**: Move TODO.md and TASKS.md to root level for immediate access
  - **Tools Preselected**: grep_search, create_directory, run_in_terminal (git mv), replace_string_in_file, file_search
  - **Risk Level**: MINIMAL (2 file moves with git history preservation)
  - **Timeline**: 15-30 minutes
  - **Success Criteria**: 1-click access to task files from VS Code root
  - **Status**: ⏳ READY TO EXECUTE

## HIGH Priority Tasks

- [x] ✅ **COMPLETED: Tool Reference & Toolset Enhancement**
  - Update comprehensive-tools-reference.md with 1NF table of all tools
  - Add 3+ new tool categories (AI Reasoning, Diagram/Visualization, Research/Academic)
  - Migrate toolsets to prefer "arxiv_improved" over current ArXiv tools
  - Refine custom_toolset.toolsets.jsonc with optimized tool groupings
  - Create usage examples for every available tool
  - **Status: COMPLETED 2025-09-10**

- [x] ✅ **COMPLETED: VS Code Copilot Instructions Guide** 2025-09-10
  - Created comprehensive guide for GitHub Copilot custom instructions
  - Includes best practices, configuration examples, and advanced usage patterns
  - Located: `knowledge/methods/vscode-copilot-instructions-guide.md`
- [x] ✅ **COMPLETED: Documentation Best Practices Research** 2025-09-10
  - Deep research on documentation best practices and standards
  - Comprehensive guide covering Sphinx, frameworks, architecture
  - Includes implementation roadmap and measurement strategies
  - Located: `knowledge/methods/documentation-best-practices-comprehensive.md`
- [x] ✅ **COMPLETED: Custom Toolset Configuration Optimization** 2025-09-10  
  - Fixed non-existent "arxiv_improved" tool references
  - Added complete ArXiv MCP server integration (`mcp_arxiv-mcp-ser_*` tools)
  - Enhanced all 10 toolsets with 23 new tool integrations
  - Aligned configurations with academic research workflows
  - Located: `projects/completed/custom-toolset-optimization-completion-report.md`
- [ ] 🔧 **IN PROGRESS: VS Code Workspace Configuration Resolution** 2025-09-11
  - **Issue**: Workspace-level toolsets partially working vs profile-level toolsets
  - **Root Cause Identified**: Empty markdown files causing git reference errors + configuration precedence issues
  - **Phase 1**: ✅ Created comprehensive .gitignore, identified 8+ empty files
  - **Phase 2**: 🔄 Content recovery for empty files using conversation history
  - **Phase 3**: ⏳ Workspace vs profile toolset configuration optimization
  - **Phase 4**: ⏳ Prevention scripts and validation automation
  - **Files Affected**: `system-design-and-software-patterns-guide.md`, `arxiv-mcp-*.md`, `mcp_servers_guide/*`
- [x] ✅ **COMPLETED: Testing Best Practices Research** 2025-09-10
  - Deep research on testing best practices using 50k token budget
  - Comprehensive guide covering Python (pytest, Ruff, Black, Pylance, Pydantic) and JavaScript (Vitest, Jest, Playwright)
  - Includes VS Code integration, automation frameworks, security testing, and 4-phase implementation roadmap
  - Located: `knowledge/methods/testing-comprehensive-guide.md`
  - make a deep research on testing best practices with vscode.
  - tokenBudget 50000 - temperature 0.2
- [ ] HIGH Search and register how to use vscode toolsets effectively. Create a search plan for that.
  - tokenBudget 50000 - temperature 0.2
- [ ] HIGH how to create an mcp that does specific step by step processes or how to combine mcps: arxiv-mcp-improved + deep-research + deep code research on a repository.
  - example deep-code-research, deep-research and arxiv-mcp, maybe using langchain.
  - parallel processes/agents are also important
- [ ] ULTRA HIGH deep-research secifically fo vscode update docs. Currently, it's separated by date, but I want it to be separated by topics. Input it into `docs/{vscode_docs_folder}/`. Use gemini-2.5-pro due to higher context.
  - REF:
    1. <https://code.visualstudio.com/updates/>

       Explore all `<nav id="docs-navbar" aria-label="Updates" class="docs-nav updates-nav visible-md visible-lg">`, but only this source.
- [ ] ULTRA HIGH Vscode copilot should also have its docs, guides and examples:
  1. for instructions
  2. for prompts
  3. for agent toolsets
  4. for mcp configurations and servers, specifically following vscode github copilots.
- [ ] ULTRA HIGH `deep-research` on how to automate task creation (JIRA mcp/extension or github actions. Ideally both).
- [ ] ULTRA HIGH full complte guide on git, with multipl examples by difficulty generated in the appropriate folder
  - `deep-research` on git usage
  - `deep-research` on git hooks, precommit hooks, and etc. for code quality and automation.
  - `deep-research` on other git automation tools
  - `deep-research` on other git features and best practices.

- [ ] add `mcp-deep-code-research` to `arxiv-mcp-improved` to analyze the code and suggest improvements.
- [ ] add `yaml` proper tags to all `.md` files.
- [ ] `python-testing-guide.md` needs proper formatting, specially for formulas.
Documents/StudiesVault_v2/AI-knowledge-base/main-knowledge-base ./.github/.knowledge_base` automatically.
  - Make a deep research in automated testing for python and js.
- [ ] **USE DEEP-CODE-RESEARCH-MCP TO EVALAUTE THE CODE FOR EXCESSIVE BOILER PLATE, POOR DESIGN PATTERNS, POOR ARCHITECTURE, POOR SYSTEM DESIGN, POOR FOLDER ORGANIZATION.**
- [ ] how to test based on the testing and testing flags in arxiv-mcp-improved chat
- [ ] full documentation update on docs following documentations in `.knowledge_base/folder-organization/workspace-organization-best-practices.md`
- [ ] update memory-mcp to support dates
- [ ] what is `ZOD`?
- [ ] full guide on the steps used in `mcp-deep-code-research` and how to develop good processes for software development.
- [ ] add `arxiv-mcp-improved` to `mcp-deep-code-research` to analyze the code and suggest improvements.
- [ ] fix human in the loop mcp to stop using the dumb tool box and use the proper tools in prompt, either by letting me pass the proper inputs inside the chat. it also should work with vscode.
- [ ] update `tools_and_mcps.md` with `recommended models
- [ ] Search github repositories focusing on mcps that generate code step by step
- [ ] Code research on software creation good practices.
- [ ] create or find an mcp to generate code appropriately.
- [ ] mcp that breaks and do your prompts step by step.
  - **Plan how to do the following task step by, selecting correct tools and fallbacks from your tool list.**
  - Please, search github repositories focusing on mcps that generate code step by step.
- [ ] deep research on system design, software architectural styles, development methodologies.
- [ ] multi agent mcp
- Finish TCC and go back to the html extension
  - add cool functionalities, similar to `markdown all in one`, but with the other framework of `markdown-extended-extension`.

- [x] add a task for the `user environement setup` to always use `smart_ln -s` when creatinv a repo with `uv`:
  - add alias to `.bashrc` or `.zshrc`:
    - `alias ln_tracked='smart_ln -s'`
  - add a function to create a repo with `uv` and create the symlink for `smart_ln -srv /home/lucas_galdino/
