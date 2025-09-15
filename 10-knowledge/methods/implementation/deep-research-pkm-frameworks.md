---
title: Deep Research Pkm Frameworks
description: Documentation for deep research pkm frameworks
status: draft
created: '2025-09-15'
updated: '2025-09-15'
tags:
- research
---

# Deep Research: Personal Knowledge Management (PKM) Architectural Styles and Frameworks

## Executive Summary

This deep research report synthesizes the dominant architectural styles and frameworks in Personal Knowledge Management (PKM)—including PARA, Zettelkasten, Johnny Decimal, LYT (Linking Your Thinking), Evergreen Notes, Maps of Content (MOCs), Building a Second Brain (BASB), Getting Things Done (GTD), the Diátaxis documentation framework, and modern knowledge-graph–centric and hybrid systems—into a cohesive set of principles, design patterns, and implementation blueprints.

## Key Findings

### Evidence Base and Reliability

- Most PKM frameworks are practitioner-driven (anecdotal/experiential) rather than supported by controlled studies
- Elements align with robust cognitive science (externalization reduces cognitive load, retrieval practice and spaced repetition aid memory)
- Architectural choice is contingent on primary workload, time horizons, collaboration constraints, and structure tolerance
- Hybrids outperform purism: PARA + MOCs + Evergreen + selective Johnny Decimal + GTD is a high-performing baseline

### Framework Comparative Analysis

#### 1. PARA (Projects, Areas, Resources, Archives)

**Strengths:**

- Clear alignment to action and time horizons
- Reduces "where does this go?" friction
- Easy onboarding; excellent for operational execution
- Works across file systems, Notion databases, and Obsidian folders

**Weaknesses:**

- Topic-knowledge fragmentation across projects
- Inherent duplication risk
- Limited support for networked thought
- Needs complementary indexing (MOCs) and synthesis layers

**Best Fit:** Project-heavy roles, cross-functional execution, consulting, product management, engineering delivery

#### 2. Zettelkasten

**Strengths:**

- Emergent structure from dense interlinking
- Powerful for originality, synthesis, and idea emergence
- Lifelong research scaffolding
- Encourages atomic notes and bidirectional links

**Weaknesses:**

- High onboarding cost
- Maintenance and link hygiene required
- Can become introspective without publishing/synthesis cadence

**Best Fit:** Researchers, writers, analysts, academics, strategists focused on insight generation

#### 3. Johnny Decimal (JD)

**Strengths:**

- Deterministic reference classification with numeric IDs (00–99 areas, 00–99 categories)
- Fosters clarity, reduces naming ambiguity
- Excellent for static reference stores
- Stable structure independent of alphabetical sorting

**Weaknesses:**

- Less flexible for emergent knowledge
- Numeric boundaries can be constraining
- Requires up-front taxonomy work
- Not optimized for networked thought

**Best Fit:** Reference-heavy domains (SOPs, standards, policy, assets), teams needing predictable findability

#### 4. LYT (Linking Your Thinking) and MOCs

**Strengths:**

- Pragmatic middle path to graphs: MOCs curate subgraphs
- Makes networked thought navigable
- Encourages intentional hubs and synthesis pages
- Lowers cognitive load vs raw graphs

**Weaknesses:**

- Curation overhead
- Risk of MOC proliferation
- Needs governance to keep MOCs high-signal

**Best Fit:** General knowledge workers who benefit from graph thinking with guardrails

#### 5. Evergreen Notes

**Strengths:**

- Emphasizes durable, reworkable notes
- Aligns with spaced revisitation and progressive refinement
- Compatible with all systems
- Supports long-term value creation

**Weaknesses:**

- Requires discipline
- Risk of over-refactoring
- Demands clear note state model

**Best Fit:** Any system aspiring to reusable insight and long-term value creation

#### 6. Building a Second Brain (BASB)

**Strengths:**

- Codifies capture to retrieval workflow
- Popularized PARA and Progressive Summarization (layers 0–5)
- Strong on practical workflows, less dogmatic about structure

**Weaknesses:**

- Can bias toward curation over original synthesis
- Evidence base is primarily experiential

**Best Fit:** Professionals needing steady output and sustainable knowledge pipeline

#### 7. Getting Things Done (GTD)

**Strengths:**

- Gold standard for task capture/clarify/organize/reflect/engage
- Stress reduction and execution reliability
- Well-tested methodology

**Weaknesses:**

- Task-centric focus
- Requires integration to prevent divergence from knowledge artifacts

**Best Fit:** Any role; use as the action layer beneath PKM

#### 8. Diátaxis Framework

**Components:** Tutorials, How-To, Explanation, Reference

**Strengths:**

- Proven in documentation contexts
- Maps cleanly to note types
- Forces clarity of audience and goal
- Excellent for refactoring raw notes into consumable outputs

**Weaknesses:**

- Demands editorial investment
- May feel heavy for personal notes if applied universally

**Best Fit:** Turning personal notes into durable guides, SOPs, and explainers; backbone for MOCs and Evergreens

**Practical Application:**

- **Tutorials:** Step-by-step guides for future self
- **How-To:** Goal-oriented checklists/SOPs
- **Explanations:** Conceptual descriptions
- **Reference:** Canonical facts, APIs, commands, formulas (JD-coded where stable)

## Architectural Patterns and Hybrid Systems

### Recommended Hybrid Archetypes

#### The Delivery Researcher (Consultant/PM-Analyst)

- PARA as spine
- MOCs per client/domain
- Evergreens for reusable insights
- GTD for actions
- JD for reference SOPs

#### The Deep Synthesist (Academic/Strategist/Writer)

- Zettelkasten + Evergreens
- MOCs as domain maps
- Minimal PARA (projects as publishing units)
- Typed links mandatory

#### The Engineering Manager

- PARA structure
- JD for team SOPs
- Diátaxis for internal docs
- MOCs for architecture domains
- Tasks in GTD tool linked to project notes

#### The Founder/Generalist

- PARA + MOCs + Evergreens
- Light ZK for ideation
- Notion for CRM/ops
- Obsidian for thinking
- Periodic export bridges

### Note and Metadata Schema

**Frontmatter Example (Obsidian YAML):**

```yaml
---
title: Short, atomic, declarative title
slug: slug-or-uid
created: 2025-09-14
updated: 2025-09-14
status: evergreen | draft | literature | fleeting | archived
type: concept | claim | how-to | reference | project | area | decision | literature
source:
  - type: paper | book | article | conversation | web | internal
  - citation: "Author, Title (Year)"
  - url: https://...
relationships:
  supports: [NoteA, NoteB]
  contrasts: [NoteC]
  part_of: [ParentConcept]
paradigms: [PKM, architecture]
para: project | area | resource | archive
jd_code: 12.34.01
summary: >
  One-paragraph synopsis in your own words.
claims:
  - statement: Core claim
    evidence: [Source1, Source2]
    confidence: 0.7
review:
  cadence: quarterly
  next_review: 2025-12-01
---
```

## Tool-Specific Implementations

### Obsidian

**Key Plugins:**

- Dataview (query notes by metadata)
- Templater (note templates)
- Canvas (concept mapping)
- Periodic Notes (daily/weekly cadence)
- QuickAdd (capture)

**Structure:**

- PARA folders
- /ZK for atomic notes
- /MOCs as folders with index notes
- /Reference JD-coded subfolders

### Roam Research

**Approach:**

- Daily notes as capture
- Page-per-concept
- Heavy use of block references
- Queries for status and type filtering

### Notion

**Databases:**

- Notes, Projects, Areas, Resources, People, Sources
- Relations between Notes-Projects, Notes-Sources
- Rollups to count links and recency

## Advanced Concepts

### Typed Links and Knowledge Graphs

**Motivation:** Un-typed backlinks bloat graphs and degrade signal. Typed links enforce intent and enable queries.

**Practical Encoding:**

```yaml
relationships:
  supports: []
  contrasts: []
  part_of: []
  depends_on: []
```

**Link Types:**

- supports, contradicts, extends, refines
- part_of, depends_on, alternative_to
- superseded_by

### Maps of Content (MOCs) Design

**Anatomy of a Good MOC:**

- Purpose and scope statement
- Key concepts
- Curated pathways
- Related MOCs
- Open problems
- Last-reviewed date

**Metrics:**

- Coverage (proportion of relevant notes linked)
- Navigability (avg clicks to reach key notes)
- Recency (time since last update)
- Usage (views/entries if tracked)

## Lifecycle Workflows and Cadences

### Daily (15-30 minutes)

- Capture in inbox (fleeting notes, tasks, highlights)
- Triage to project/area or literature
- Link-and-title pass
- Seed 1 evergreen

### Weekly Review (90-120 minutes)

**Projects:**

- Clarify next actions (GTD)
- Prune stale tasks

**Knowledge:**

- Promote 2–5 notes to evergreen
- Update at least one MOC
- Review orphan notes and link or archive

**System Health:**

- Report KPI snapshot (orphan rate, link density, time-to-retrieval samples)

### Monthly

- Refactor one domain MOC
- Consolidate duplicates
- Archive one area's stale resources

### Quarterly

- Taxonomy review (Johnny Decimal ranges, tag culls)
- Backup and integrity checks
- Publish a synthesis artifact

## Digital Note-Taking Best Practices

1. **Titles as claims or clear concepts** - avoid "Note about X"
2. **One note = one idea** - if two ideas, split and link
3. **Capture in your own words** - quotes only for essential phrasing
4. **Use progressive summarization** - raw → highlights → bold/layered summary → executive synthesis
5. **Prefer typed links** over indiscriminate backlinks
6. **Make MOCs navigable** - short intro, table of contents, key pathways
7. **Ritualize deletion and archiving** - stale notes have a cost
8. **Separate tasks from notes** but link both ways
9. **Automate where safe** - templates, link suggestions
10. **Keep judgment manual** - claims, conclusions

## Synthesis Techniques for Experts

### Claims–Evidence Ledger

Transform literature notes into claim statements linked to evidence notes. Track confidence per claim.

### Dialectical Pairing

Create "contrasts-with" links and write reconciliations to reduce confirmation bias.

### Concept Stacking

Build evergreen stack from low-level to high-level abstractions; each higher note explicitly lists dependencies.

### Narrative MOCs

Convert MOC into story arc for presentations or essays; supports rapid publishing.

### Pattern Mining

Quarterly export graph and compute communities/betweenness; inspect top hubs and gaps.

## Metrics and Evaluation

### Key Performance Indicators

- **Retrieval Time (TTR):** Median time to locate item; target < 20 seconds for high-frequency items
- **Reuse Rate:** % of new outputs that reuse at least one evergreen; target > 60% for research-heavy roles
- **Link Density:** Average links per note (typed); aim for 3–10 depending on domain
- **Orphan Rate:** % notes without inbound links; keep < 15%
- **Staleness:** Notes with next_review past due; keep < 10% for mission-critical domains
- **Synthesis Velocity:** Time from reading to published synthesis; track trend downwards

## AI and Automation

### Practical Patterns

- **Embedding Search:** Build local embedding index for semantic search
- **Auto-link Suggestions:** Use embeddings + BM25 to suggest candidate links
- **RAG Assistants:** Chat with vault through retrieval layer
- **Summarization:** Batch summarize literature notes with progressive layers

### Cautions and Mitigations

- **Model Drift:** Keep humans in the loop
- **Hallucination:** Require citations to vault notes
- **Privacy Leakage:** Use local models or providers with strong privacy terms
- **Provenance:** Store prompt, model, date, and input hashes in note metadata

## Anti-Patterns to Avoid

1. **Purist Monocultures:** Zettelkasten without projects, or PARA without synthesis
2. **Tag Explosion:** Uncontrolled tags with synonyms
3. **Link Soup:** Backlinks without semantics
4. **Sunk-cost Hoarding:** Legacy notes that never influence outputs
5. **Hidden Tasks:** Actions buried in prose without explicit task entities

## 30/60/90-Day Adoption Plan

### 0–30 Days

- Stand up vault/workspace
- Implement PARA containers
- Define note schema
- Create 3 MOCs
- Start daily capture
- Weekly reviews

### 31–60 Days

- Introduce typed links
- Convert top 30 notes to Evergreens
- Integrate GTD task system
- Add claim-evidence pattern
- Instrument metrics

### 61–90 Days

- Refactor one domain using Diátaxis
- Begin AI-assisted link suggestions with provenance
- Export graph, analyze hubs
- Publish one synthesis artifact

## Tool Selection Quick Guidance

- **Maximal control, offline files, extensibility:** Obsidian
- **Outline thinking, blocks, frictionless linking:** Roam
- **Dashboards, relations, collaboration/ops integration:** Notion
- **Hybrid approach:** Authoring/thinking in Obsidian + operational dashboards in Notion

## Closing Recommendations

Start with a hybrid spine—PARA containers, MOCs for curation, Evergreen notes for durable knowledge, GTD for action—and selectively add Zettelkasten mechanics for research. Introduce typed links and Diátaxis for structure and reuse. Instrument your system with retrieval and reuse metrics; prune aggressively. Use AI as an accelerant with provenance guarantees. Evolve your architecture quarterly based on measured outcomes rather than doctrine.

## Sources

This research synthesizes information from multiple authoritative sources on personal knowledge management, cognitive science, information architecture, and digital productivity methodologies. The findings integrate academic research with practitioner experiences to provide evidence-based recommendations for PKM system design and implementation.
