---
applyTo: '**'
description: Enforce academic folder structure and organization rules for AI knowledge
  base
title: Folder Structure Enforcement Instruction
status: active
created: '2025-09-10'
updated: '2025-09-11'
tags:
- .github
- instructions
- folder-structure
- academic-organization
- governance
version: 1.1.0
authors:
- lucas_galdino
citations: []
---



# Folder Structure Enforcement Rules

## � RECENT UPDATES (2025-09-11)

### ✅ Workspace Reorganization Completed

- **TODO.md** and **TASKS.md** moved to root level for operational efficiency
- **current-work/** directory created for active development files
- Kebab-case naming enforced: `mcp_servers_guide` → `mcp-servers-guide`
- Completion reports moved to `projects/completed/`
- Research literature moved to `resources/literature/`

## �🏗️ Academic Directory Structure

### **ROOT LEVEL MANDATORY STRUCTURE**

```tree
/
├── .github/          # GitHub configuration, workflows, instructions (ROOT ONLY)
├── .vscode/          # VS Code settings and configuration (ROOT ONLY)
├── TODO.md           # Operational task management (ROOT LEVEL)
├── TASKS.md          # Task analysis and planning (ROOT LEVEL)
├── current-work/     # Active development and work-in-progress files
├── knowledge/        # Academic knowledge repository
├── projects/         # Project lifecycle management
├── resources/        # Supporting materials and references
├── infrastructure/   # Scripts, automation, and maintenance tools
├── outputs/          # Generated content and publications
├── database/         # SQLite databases for persistent storage
├── mcp-servers-guide/ # MCP server documentation (kebab-case)
├── GOVERNANCE.md     # Academic governance framework
├── CITATION.cff      # Academic citation standards
└── README.md         # Primary documentation
```

## 🎯 Mandatory Rules for AI Agents

### **1. Directory Placement Rules**

- **NEVER** move `.github/` or `.vscode/` from root directory
- **ALWAYS** place new documentation in appropriate academic category:
  - `knowledge/foundations/` - Core concepts and foundational knowledge
  - `knowledge/methods/` - Methodologies, processes, and implementation guides
  - `knowledge/applications/` - Applied knowledge, use cases, and examples
  - `knowledge/synthesis/` - Research synthesis and meta-analysis
- **ALWAYS** use `projects/` for project-related content with lifecycle stages:
  - `projects/active/` - Currently active projects
  - `projects/completed/` - Finished projects with completion reports
  - `projects/archived/` - Archived or deprecated projects
- **ALWAYS** place supporting materials in `resources/`:
  - `resources/literature/` - Research papers, articles, and academic references
  - `resources/tools/` - Tool documentation and guides
  - `resources/data/` - Datasets and data sources

### **2. File Creation and Modification Rules**

- **ALWAYS** add YAML frontmatter to new `.md` files using the academic template:

```yaml
---
title: [Descriptive Title]
description: [Brief description]
status: [draft|active|completed|archived]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
tags: [relevant, tags, list]
version: [X.Y.Z]
---
```

- **ALWAYS** run YAML frontmatter enforcer after bulk operations:
  ```bash
  python3 infrastructure/scripts/organization/yaml-frontmatter-enforcer.py --fix
  ```

### **3. Database Integration Rules**

- **ALWAYS** consider database integration for persistent knowledge management
- **USE** appropriate database for content type:
  - `knowledge.db` - Knowledge articles and documentation
  - `citations.db` - Academic citations and references
  - `analytics.db` - Usage analytics and metrics
  - `workflows.db` - Process documentation and workflows

### **4. Content Migration Rules**

- **NEVER** create new top-level directories without governance approval
- **ALWAYS** migrate legacy content to appropriate academic structure
- **PRESERVE** all existing content during reorganization
- **UPDATE** internal references after moving files

### **5. Automation and Scripts Rules**

- **ALWAYS** place automation scripts in `infrastructure/scripts/`
- **USE** existing automation tools before creating new ones
- **FOLLOW** governance framework for script development
- **TEST** scripts before deployment to avoid data loss

## 🚫 Prohibited Actions

1. **NEVER** remove `.github/` or `.vscode/` from root
2. **NEVER** create flat directory structures without academic hierarchy
3. **NEVER** skip YAML frontmatter validation
4. **NEVER** ignore database integration opportunities
5. **NEVER** bypass governance framework for structural changes

## ✅ Compliance Validation

Before completing any task, verify:

- [ ] Academic directory structure maintained
- [ ] YAML frontmatter compliant on all modified files
- [ ] Database integration considered and implemented where appropriate
- [ ] Governance framework followed
- [ ] No prohibited directory movements occurred

## 🔄 Continuous Improvement

This instruction file should be updated when:

- New academic categories are added
- Database schema changes
- Governance framework evolves
- Automation tools are enhanced

**Last Updated**: 2025-09-10
**Next Review**: 2025-10-10
