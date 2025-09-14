---
applyTo: AI Agents, GitHub Copilot, LLM Tools
description: Rules for AI-generated content creation and organization in academic
  knowledge base
title: AI Content Generation Rules
status: active
created: '2025-09-10'
updated: '2025-09-10'
tags:
- .github
- instructions
- ai-content
- content-generation
- academic-standards
version: 1.0.0
authors:
- lucas_galdino
citations: []
---



# AI Content Generation Rules

## 🤖 Mandatory Rules for AI Agents

### **1. Content Placement Rules**

#### **ALWAYS** use appropriate academic directories

- **Knowledge Documentation**:
  - `knowledge/foundations/` → Core concepts, definitions, foundational knowledge
  - `knowledge/methods/` → Methodologies, processes, implementation guides, how-to documents
  - `knowledge/applications/` → Use cases, examples, applied knowledge, practical implementations
  - `knowledge/synthesis/` → Research synthesis, meta-analysis, comprehensive reviews

- **Project Content**:
  - `projects/active/` → Currently active projects and work-in-progress
  - `projects/completed/` → Finished projects with completion reports
  - `projects/archived/` → Deprecated or archived project materials

- **Supporting Materials**:
  - `resources/literature/` → Research papers, academic articles, literature reviews
  - `resources/tools/` → Tool documentation, guides, reference materials
  - `resources/data/` → Datasets, data sources, data documentation

### **2. YAML Frontmatter Requirements**

#### **MANDATORY** frontmatter for ALL new `.md` files

```yaml
---
title: [Clear, descriptive title]
description: [Concise description of content purpose]
status: [draft|active|completed|archived]
created: '[YYYY-MM-DD]'
updated: '[YYYY-MM-DD]'
tags:
  - [relevant]
  - [descriptive]
  - [tags]
version: [X.Y.Z]
---
```

#### **Additional frontmatter for specific content types**

**Research Documents**:

```yaml
methodology: [research methodology used]
sources: [number of sources]
confidence: [high|medium|low]
peer_reviewed: [true|false]
```

**Tool Documentation**:

```yaml
tool_category: [category from comprehensive-tools-reference.md]
compatibility: [system requirements]
last_tested: '[YYYY-MM-DD]'
```

**Project Reports**:

```yaml
project_status: [active|completed|archived]
completion_date: '[YYYY-MM-DD]'
team_size: [number]
```

### **3. Content Quality Standards**

#### **ALWAYS** include

1. **Deep Research Foundation**:
   - Use `mcp_deep-research_deep-research` tool for comprehensive background
   - Minimum 5 authoritative sources for any knowledge document
   - Include source citations in academic format

2. **Structured Content**:
   - Clear hierarchical headings (H1 → H2 → H3)
   - Executive summary for documents > 1000 words
   - Table of contents for comprehensive guides

3. **Academic Rigor**:
   - Fact-checking with multiple sources
   - Methodology transparency
   - Limitation acknowledgments

### **4. Database Integration Requirements**

#### **ALWAYS** consider database storage for

- **Knowledge Articles** → Store in `knowledge.db`
- **Citations and References** → Store in `citations.db`
- **Tool Usage Patterns** → Store in `analytics.db`
- **Process Documentation** → Store in `workflows.db`

### **5. Cross-Reference Requirements**

#### **ALWAYS** maintain consistency

- Link to existing content when relevant
- Update related documents when adding new content
- Check for duplicate or overlapping content
- Maintain internal link integrity

### **6. Automation Compliance**

#### **ALWAYS** after content creation

1. Run YAML frontmatter enforcer:
   ```bash
   python3 .kb/scripts/yaml-frontmatter-enforcer.py --fix
   ```

2. Validate academic structure compliance
3. Update database entries if applicable
4. Check governance framework adherence

## 🚫 Prohibited Content Actions

### **NEVER**

1. Create content outside the academic directory structure
2. Skip YAML frontmatter for any `.md` file
3. Place `.github/` or `.vscode/` outside root directory
4. Create flat directory structures without hierarchy
5. Generate content without research backing
6. Ignore existing governance framework
7. Duplicate content without cross-referencing
8. Skip database integration opportunities

## 📋 Content Creation Checklist

Before marking content as complete, verify:

- [ ] Content placed in appropriate academic directory
- [ ] YAML frontmatter complete and compliant
- [ ] Deep research conducted with sources cited
- [ ] Academic quality standards met
- [ ] Database integration considered/implemented
- [ ] Cross-references updated
- [ ] Governance framework followed
- [ ] Automation tools executed

## 🔄 Content Maintenance Rules

### **Regular Maintenance Tasks**

1. **Monthly Review**: Update status fields in YAML frontmatter
2. **Quarterly Audit**: Run comprehensive compliance checks
3. **Semi-Annual**: Database optimization and cleanup
4. **Annual**: Governance framework review and updates

### **Update Triggers**

- Source material changes
- Tool deprecation or updates
- Methodology improvements
- Governance framework evolution

## 🎯 Quality Metrics

### **Success Criteria**

- 100% YAML frontmatter compliance
- Academic directory structure adherence
- Research-backed content (minimum 3 sources)
- Database integration where applicable
- Cross-reference accuracy
- Governance framework compliance

### **Performance Indicators**

- Content findability score
- Cross-reference coverage
- Database utilization rate
- Academic standard compliance
- User engagement metrics

---

**Enforcement**: This instruction file is automatically enforced through:

- YAML frontmatter validation scripts
- Directory structure monitoring
- Database integration checks
- Governance framework audits

**Compliance**: All AI agents must demonstrate adherence to these rules before content approval.

**Last Updated**: 2025-09-10
**Next Review**: 2025-11-10
