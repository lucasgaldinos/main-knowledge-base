---
mode: "enhanced-loop-recreation"
name: "Systematic Content Recreation"
description: "A comprehensive methodology for creating high-quality content with external validation using a structured loop approach. Transforms the proven 'continue where you stopped' pattern into a reusable systematic process."
tags: ["content-creation", "research", "academic", "validation", "systematic", "documentation"]
---

# Systematic Content Recreation Prompt

This prompt implements a proven methodology for creating comprehensive content with external validation. It follows the enhanced loop structure that has successfully recreated high-quality documentation in academic and technical domains.

## #think

Before executing this prompt, analyze the following:

1. **Scope Definition**: What specific content areas need to be addressed?
2. **Tool Preselection**: Which tools from `docs/tools/comprehensive-tools-reference.md` are most appropriate?
3. **External Validation Requirements**: What types of sources (web, academic, technical) are needed?
4. **Quality Standards**: What level of depth and validation is required?
5. **Integration Strategy**: How will external findings be synthesized with created content?

## Core Implementation

### Phase 1: Planning and Preparation

**Task Breakdown Template:**

```yaml
## Loop N: [Topic/Task Name]

### Task Breakdown and Tool Preselection
**Task**: [Clear, specific objective]
**Smaller Steps**:  `
1. [Concrete step 1]
2. [Concrete step 2] 
3. [Concrete step 3]
4. [Concrete step 4]

**Tool Preselection** (from comprehensive-tools-reference.md):
- **Research**: some tool from [here](docs/tools/comprehensive-tools-reference.md) (e.g. vscode-websearchforcopilot_webSearch, mcp_deep-research_deep-research)
- **File Creation**: create_file, replace_string_in_file
- **Academic Search**: mcp_alex-mcp_*, mcp_google-schola_*, mcp_arxiv-mcp-ser_*
- **Validation**: think, actor_critical_thinking, mcp_sequentialthi_sequentialthinking
- **Domain-Specific**: [Add relevant specialized tools]
```

### Phase 2: Content Creation Foundation

1. **Create Structured File**
   - Use `create_file` with comprehensive template structure
   - Include placeholders for external content integration
   - Establish clear sections and formatting standards
   - Add examples and implementation details where applicable

2. **Initial Content Development**
   - Build foundational content using existing knowledge
   - Include practical examples and use cases
   - Maintain consistent formatting and style
   - Prepare integration points for external validation

### Phase 3: External Validation and Research

#### 3.1 Current Information Search

- **Tool**: `vscode-websearchforcopilot_webSearch`
- **Purpose**: Find latest industry practices, current trends, recent developments
- **Strategy**: Search for "current best practices [topic] 2024", "latest [topic] trends", "industry standards [topic]"

#### 3.2 Deep Research (Optional for Complex Topics)

- **Tool**: `mcp_deep-research_deep-research`
- **Purpose**: Comprehensive multi-source analysis with quality control
- **Parameters**:
  - depth: 3-5 (based on complexity)
  - breadth: 3-4 (for balanced coverage)
  - sourcePreferences: "avoid SEO listicles, prioritize authoritative sources"

#### 3.3 Academic Validation

- **Tools**: `mcp_alex-mcp_search_works`, `mcp_google-schola_search_google_scholar_advanced`, `mcp_arxiv-mcp-ser_search_arxiv`
- **Purpose**: Peer-reviewed validation, theoretical foundations, recent research
- **Strategy**:
  - Search for foundational papers and recent developments
  - Focus on highly-cited works and recent publications
  - Cross-reference findings across multiple academic sources

#### 3.4 Technical Documentation (for Technical Topics)

- **Tools**: `mcp_github_search_code`, `mcp_deepwiki_ask_question`
- **Purpose**: Implementation examples, best practices, real-world usage
- **Strategy**: Find authoritative repositories and documentation sources

### Phase 4: Integration and Enhancement

1. **Synthesize Findings**
   - Combine web search results with academic research
   - Identify consensus and contradictions between sources
   - Prioritize authoritative and recent information
   - Note gaps between current practice and academic research

2. **Content Enhancement**
   - Use `replace_string_in_file` to integrate validated information
   - Add citations and references appropriately
   - Include specific examples from real-world implementations
   - Update recommendations based on latest findings

3. **Quality Validation**
   - Ensure all external sources are properly integrated
   - Verify technical accuracy of implementations
   - Check for completeness against original objectives
   - Validate formatting and consistency

### Phase 5: Documentation and Lessons Learned

1. **Register Enhanced Findings**
   - Document methodology used and sources consulted
   - Note particularly valuable sources for future reference
   - Record any limitations or gaps in available information
   - Update tool selection rationale for similar future tasks

2. **Quality Metrics**
   - External sources consulted: [number and types]
   - Academic references validated: [number and quality]
   - Implementation examples included: [specific cases]
   - Last updated: [current date]

## Specialized Workflows

### Academic Bulk Processing Workflow

For content requiring multiple academic sources:

```text
1. Search Phase:
   - mcp_alex-mcp_search_works (comprehensive academic search)
   - mcp_google-schola_search_google_scholar_advanced (current research)
   - mcp_arxiv-mcp-ser_search_arxiv (latest preprints)

2. Collection Phase:
   - mcp_arxiv-mcp-ser_load_article_to_context (for immediate analysis)
   - mcp_arxiv-mcp-ser_download_article (for reference library)

3. Analysis and Synthesis Phase:
   - Process papers in groups of 3-5
   - Use sequential thinking for complex synthesis
   - Document common themes and contradictions
```

### Technical Implementation Workflow

For technical content requiring code examples:

```text
1. Research Phase:
   - mcp_github_search_code (find implementation examples)
   - vscode-websearchforcopilot_webSearch (current best practices)

2. Validation Phase:
   - mcp_deepwiki_ask_question (repository-specific guidance)
   - semantic_search (internal codebase patterns)

3. Implementation Phase:
   - Include tested code examples
   - Reference authoritative repositories
   - Document version compatibility
```

## Success Criteria

✅ **Content Quality**

- Comprehensive coverage of topic with multiple perspectives
- Integration of current industry practices with academic foundations
- Practical examples and implementation guidance
- Clear, well-structured presentation

✅ **External Validation**

- Minimum 3-5 authoritative web sources
- At least 2-3 academic references for theoretical topics
- Recent sources (within 1-2 years for rapidly evolving topics)
- Cross-validation of key claims across multiple sources

✅ **Technical Accuracy**

- Working code examples where applicable
- Version-specific implementation details
- Compatibility and dependency information
- Real-world usage patterns and limitations

✅ **Documentation Standards**

- Consistent formatting and style
- Proper citations and references
- Clear section organization
- Integration with existing documentation structure

## Adaptation Guidelines

This methodology can be adapted for different content types:

- **Technical Documentation**: Emphasize code examples and implementation guides
- **Research Summaries**: Focus on academic sources and peer review validation
- **Best Practices Guides**: Prioritize current industry standards and real-world examples
- **Educational Content**: Balance theoretical foundations with practical applications

The key is maintaining the systematic approach while adjusting tool selection and validation criteria to match the specific content requirements.
