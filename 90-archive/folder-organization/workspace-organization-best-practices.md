---
title: Workspace Organization Best Practices
description: Documentation for workspace organization best practices
status: draft
created: '2025-09-15'
updated: '2025-09-15'
tags:
- documentation
---

# Best practices for organizing knowledge base folders and methodologies

Executive summary

This report synthesizes established information architecture principles, software engineering practice, and documentation methodologies to recommend robust folder structures, governance, and workflows for knowledge bases. We cover directory hierarchies, pros and cons of organizational approaches, and tailored use cases for academic research projects, Brazilian TCC projects, and multi-language development environments. While there are many valid patterns, well-run knowledge bases converge on a handful of durable practices: shallow but expressive hierarchies, consistent naming and metadata, docs-as-code workflows with review and CI, hybrid taxonomy plus tagging, and clear lifecycle governance. The structures and recommendations herein are aligned with recognized records management and research data management concepts (e.g., ISO-style records management, FAIR data principles) and common practice in modern engineering organizations (monorepos, i18n workflows, static site generators). Where novel or contrarian guidance appears, it is flagged as speculative.

Scope and assumptions

- Audience: Senior analysts, researchers, and engineering leads designing or refactoring knowledge bases at team or org scale.
- Contexts: Organization-wide knowledge bases, individual project repositories, and documentation portals for codebases.
- Constraints: Most consumers rely on search, but browseable structure is necessary for discoverability, governance, and onboarding.
- Reliability note: Recommendations derive from mainstream information architecture, reproducible research, and dev tooling practice rather than a single authority. They are cross-validated by convergence across multiple independent communities (software docs, RDM, PKM practitioners).

Core design principles

1) Make the first click obvious

   - Top-level directories should reflect how users think: by purpose and audience (e.g., guides, references, projects, operations) rather than internal org chart or tool names.
   - Keep the top level stable; evolve beneath it.

2) Prefer shallow hierarchies with rich metadata

    - Depth > 3 begins to harm discoverability. Use tagging, cross-links, and indices instead of deep nesting.
    - Write an index or overview file in every folder that enumerates contents and relationships.

3) Use stable, machine-friendly naming

    - Lowercase, hyphen-separated names; no spaces. Example: data-raw, data-clean, lit-reviews.
    - Date prefixes ISO 8601 for temporal ordering: 2025-09-06-...
    - Use stable identifiers for projects and datasets.

4) Separate source, generated, and published artifacts

    - Keep raw inputs immutable. Generated outputs go to dedicated build or outputs directories; publishable docs go to site or dist.
    - Enables clean rebuilds, reproducibility, and simpler backups.

5) Docs-as-code for governance and scalability

- Keep documentation and knowledge artifacts in version control with code review, CI checks, linting, and automated site builds.
- Write contribution guidelines, PR templates, and codeowners to sustain quality.

6) Hybrid organization: taxonomy plus tags

- Use a consistent folder taxonomy for 80% of navigation and add tags or link graphs to support cross-cutting discovery (topics, methods, domains).
- Avoid overfitting the taxonomy to transient org structures.

7) Lifecycle discipline

- Explicit states: draft, in-review, published, deprecated, archived. Reflect status in metadata and paths where appropriate.
- Regular pruning and archiving reduce entropy.

8) Access and compliance

- Principle of least privilege for sensitive data and drafts. Public mirrors for what must be shared broadly.
- Keep compliance-relevant records (ethics approvals, consent forms, licenses) in predictable locations.

Organizational approaches with pros and cons

Approach A: Subject taxonomy (by domain/topic)

- Example top level: ai-ml, security, devops, data-engineering, product, ux.
- Pros: Intuitive for browsing by topic; aligns with how many users search conceptually.
- Cons: Cross-cutting artifacts (e.g., a pipeline touching AI and data engineering) are hard to place; topics change over time; risk of duplicated content across subjects.
- Use when: Knowledge base is primarily for learning/reference content; projects are secondary.

Approach B: Project-centric (every project is a top-level node)

- Example top level: proj-abc, proj-xyz, proj-delta.
- Pros: Strong encapsulation; clean permissions; straightforward archiving when projects end; excellent for reproducibility.
- Cons: Harder to find cross-project learning; duplication of boilerplate; users must know project names.
- Use when: Portfolio of short- to medium-lived projects; compliance and reproducibility matter.

Approach C: Function or audience-based (guides, references, operations)

- Example top level: guides, reference, tutorials, runbooks, decisions, standards.
- Pros: Aligns with documentation types; supports docs-as-code sites like Docusaurus, MkDocs, Sphinx; powerful for onboarding and operations.
- Cons: Requires metadata to indicate domain and projects; contributors must classify content correctly.
- Use when: Organization-wide knowledge base; mixed audience; you will run a documentation site.

Approach D: PARA (Projects, Areas, Resources, Archives)

- Pros: Flexible across individual and team use; clean separation of active vs evergreen vs reference.
- Cons: PARA boundaries can blur in large teams; requires governance to apply consistently; not self-evident to all users.
- Use when: You need a simple, memorable pattern for mixed-use knowledge bases or personal/team PKM.

Approach E: Johnny Decimal system

- Numeric index like 10-19 Strategy, 20-29 Operations, etc.; folders prefixed by numbers for sortable, unambiguous placement.
- Pros: Forces uniqueness; reduces where-does-this-go anxiety; scales with indices.
- Cons: Requires maintaining a registry; numbers are opaque to new users without an index.
- Use when: You want strict structure, stable placement, and are willing to maintain an index.

Approach F: Zettelkasten and graph-first (atomic notes linked bidirectionally)

- Pros: Excellent for research synthesis and idea development; promotes serendipity via backlinks and tags.
- Cons: Weak hierarchical affordances; can devolve into a link jungle without discipline; less approachable for operations.
- Use when: Early-stage research and literature synthesis; complement with a taxonomy for publishable outputs.

Recommendation: Hybridize. Combine a stable top-level functional taxonomy (e.g., guides, reference, projects, operations) with project folders for execution and a tag system for topics. For personal or small-team research, PARA or Johnny Decimal can provide discipline; map it onto the org-wide taxonomy when publishing.

Cross-cutting best practices

Naming conventions

- Lowercase, hyphen-separated: project-acronym, method-name.
- Use short, stable IDs: proj-abc, dataset-1234.
- Prefixes for type or lifecycle: draft-..., wip-..., archived-.... Avoid dates embedded in file names when version control provides history; use dates for externally sourced snapshots.
- Avoid ambiguous abbreviations; publish a naming cheatsheet.

Folder depth and size

- Aim for 2–3 levels deep for most content. If a folder exceeds 30–50 items, split by logical subcategory.
- Use index files (README.md or _index.md) at every level listing contents and linking related pages.

Metadata and front matter

- Use YAML front matter for docs and notes:

```yaml
---
title: Model evaluation rubric
authors: [jdoe]
tags: [ml, evaluation, metrics]
status: published
updated: 2025-09-06
related: [proj-abc, metric-f1]
---
```

- Standard fields: title, authors, tags, status, created/updated, related, source, license, confidentiality.

Separation of concerns

- src for source code, docs for documentation source, data-raw for immutable inputs, data-clean for curated datasets, notebooks or analysis for exploratory scripts, outputs for generated artifacts, site or dist for published assets.
- Do not commit large binaries to git; use git LFS or DVC.

Versioning and releases

- Semantic versioning for public docs and standards (e.g., standards/v1.2). For research outputs, version datasets and analysis environments together.
- Tag releases and publish site snapshots for reproducibility.

Permissions and access control

- Public, internal, restricted tiers. Reflect in folder layout when possible or enforce via repository boundaries.
- Use codeowners for critical areas; enforce branch protection and review.

Retention and archival

- Archive projects on completion: move to archives with a frozen site snapshot and a short executive summary.
- Keep raw data per compliance requirements; document retention and destruction policies.

Automation and CI

- Lint docs (e.g., markdownlint), spellcheck, linkcheck in CI.
- Build and deploy static sites automatically; generate indices, sitemaps, and search indices (including embeddings if applicable).
- Pre-commit hooks enforce naming, front matter presence, and broken link detection.

Search and semantic discovery

- Combine exact search (ripgrep, grep) with full-text indexing (OpenSearch) and optional vector search for semantic queries.
- Generate and maintain a knowledge graph of cross-links and references for advanced navigation.

Reference directory templates

Template 1: Organization-wide knowledge base (docs-as-code)

```
kb/
  README.md                 # How to navigate, contribution guide
  CONTRIBUTING.md
  GOVERNANCE.md             # Roles, review SLAs, taxonomy rules
  .github/
    workflows/              # CI for lint, linkcheck, site build
  .vale/                    # Style guide for prose linting (optional)
  docs/
    _index.md               # Landing page
    guides/                 # How-to, tasks, tutorials
      _index.md
      onboarding/
      data/
      ml/
    reference/              # APIs, schemas, definitions, standards
      _index.md
      api/
      schemas/
      standards/
    decisions/              # ADRs (architecture decision records)
      _index.md
      2025-01-12-adopt-bazel.md
    operations/             # Runbooks, SLOs, incident playbooks
      _index.md
      runbooks/
      incidents/
    projects/               # Lightweight overview pages linking to repos
      _index.md
      proj-abc.md
      proj-xyz.md
    glossary/
      _index.md
      terms.md
    tags/                   # Auto-generated tag indices (optional)
  site/                     # Built site artifacts (ignored from VCS)
  scripts/
  mkdocs.yml or docusaurus.config.js
```

Template 2: Academic research project (reproducible)

```
proj-abc/
  README.md                 # Project abstract, key files map
  LICENSE
  CITATION.cff              # Citation metadata
  .gitignore
  .dvc/                     # If using DVC for data pipelines
  env/                      # Environment specs
    conda-environment.yml
    requirements.txt
    Dockerfile
  data/
    data-raw/               # Immutable inputs (DVC tracked)
    data-external/          # Third-party; include source metadata
    data-interim/           # Intermediate outputs
    data-clean/             # Curated, analysis-ready datasets
  notebooks/
    exploration/            # EDA notebooks
    reports/                # Polished, parameterized notebooks
  src/
    proj_abc/               # Python or language package
    scripts/                # CLI entry points
  analysis/
    methods/                # Statistical analysis scripts
    models/                 # Training and evaluation
    results/                # Figures, tables (generated)
  docs/
    manuscript/             # Paper drafts (LaTeX or Markdown)
    supplements/            # Supplementary materials
    protocols/              # Lab or data collection SOPs
    ethics/                 # IRB/ethics approvals, consent forms
  outputs/
    figures/
    tables/
    logs/
  tests/
  Makefile or tox.ini
```

Template 3: TCC project (ABNT-friendly and bilingual optional)

```
TCC-joao-silva-2025/
  README.md                 # Scope, advisor, deadlines, defense requirements
  .gitignore
  env/
    latex/                  # TeX dependencies
    refs/                   # Citation manager exports
  docs/
    tcc/                    # Main manuscript
      src/
        pre-textual/        # Capa, folha de rosto, resumo, abstract
        textual/            # Introdução, metodologia, resultados, conclusão
        post-textual/       # Referências, apêndices, anexos
      templates/            # ABNT templates
      figures/
      tables/
    presentation/           # Slides for defense
    artifacts/
      questionnaire/        # Instruments used
      approvals/            # Ethics/committee letters
  research/
    literature/
      to-read/
      notes/                # Atomic lit notes with citation keys
      synthesis/            # Thematic summaries
    data/
      data-raw/
      data-clean/
      codebook.md
    analysis/
      notebooks/
      scripts/
      outputs/
  src/                      # If software is part of the TCC
  ci/                       # Automated builds for PDF, references
  Makefile
```

Template 4: Multi-language development monorepo with documentation and i18n

```
monorepo/
  README.md
  CODEOWNERS
  .github/workflows/
  tools/
    bazel/ or pants/ or nx/ # Build orchestration
    scripts/
  packages/
    python/
      lib-ml/
        src/
        tests/
        pyproject.toml
      service-analytics/
        src/
        tests/
        requirements.txt
    js/
      web-app/
        src/
        tests/
        package.json
      docs-site/
        docusaurus.config.js
    rust/
      data-pipeline/
        src/
        tests/
        Cargo.toml
  services/
    api-gateway/
      src/
      tests/
      openapi/
  shared/
    schemas/
    protobuf/
    components/
  docs/
    i18n/
      en/
        guides/
        reference/
      pt-BR/
        guias/
        referencia/
    guides/
    reference/
    adr/
  config/
    dev/
    prod/
  data/
    samples/
  scripts/
```

Notes on the monorepo template

- Keep each language ecosystem encapsulated with its native tooling, but provide top-level orchestration via Bazel, Pants, NX, or Makefiles.
- Use shared for cross-language assets (schemas, messages), never embed copies.
- docs/i18n mirrors the default docs structure; use locale directories not branches to reduce drift.

Methodologies and workflows

Docs-as-code workflow

- Contribution: Changes via PRs, with mandatory review from content owners defined in CODEOWNERS.
- Validation: CI runs prose linters, spellcheck, linkcheck, schema checks for front matter, and build checks for static site.
- Preview: PR deploy previews to review content in final rendered form.
- Release: Regular site builds; versioned docs for breaking changes.

Content lifecycle

- Draft: Clearly marked; optional drafts/ subfolders gated from public builds.
- In-review: PR labels; review SLAs; reviewers assigned via codeowners.
- Published: Merged; indexed in tag pages and indices.
- Deprecated: Mark front matter status: deprecated and add replacement links.
- Archived: Moved to archives with a summary; excluded from default navigation but kept searchable.

Taxonomy governance

- Maintain a controlled vocabulary for tags and top-level categories; review new tags.
- Avoid synonyms proliferating; establish preferred terms and redirects.
- Quarterly taxonomy review to adjust for new domains.

Decision records

- Use ADRs for decisions with long-term implications; store in decisions or adr folder.
- Link ADRs to impacted docs and code via related metadata.

Multilingual content methodology

- Foldering: Separate locale roots, e.g., docs/i18n/en and docs/i18n/pt-BR, mirroring structure.
- String externalization: For apps, maintain translations in messages files (JSON, YAML) with keys; for docs, keep separate localized files.
- Source of truth: Author in one primary locale (often English) and track translation status in front matter (status: needs-translation or needs-update).
- Glossary and termbase: Maintain bilingual term lists with definitions to ensure consistency across translators and contributors.
- Automation: CI detects changes in source docs and opens translation issues; optional integration with CAT tools.

Research- and compliance-specific practices

- Data provenance: Capture source metadata (who, when, license, method) in data-external and data-raw README files.
- Reproducibility: Pin environments (conda, Docker), seed randomness, record versions of data and code at time of analysis; use Makefiles or pipelines.
- Ethics and privacy: Keep consent and approvals in docs/ethics; document anonymization in protocols.
- FAIR alignment: Findable via stable IDs and indices; Accessible via documented paths and permissions; Interoperable via standard schemas; Reusable via licenses and codebooks.

Tools that reinforce structure

- Static site generators: MkDocs (+Material), Docusaurus, Sphinx. Choose based on ecosystem and need for versioning/i18n.
- Prose linters: Vale for style, markdownlint.
- Search: Algolia, Lunr, or OpenSearch. For semantic search, build embeddings (e.g., OpenAI or local models) and index YAML front matter plus body.
- Build systems: Bazel, Pants, NX/Turborepo for polyglot repos; ensure docs build as a first-class target.
- Data management: DVC for data pipelines; git LFS for binaries; Quilt or LakeFS for data catalogs.
- Citations: Zotero or Mendeley; export BibTeX; use CITATION.cff for repo-level citation.

Use case deep dives

1) Academic research projects
Goals

- Reproducibility, transparent provenance, easy collaboration, and clear publication pipelines.

Key practices

- Separate raw and processed data. Raw data is append-only; processed can be recreated.
- Parameterize notebooks and scripts; avoid manual one-off transformations.
- Use a codebook and data dictionary in data-clean; maintain variable naming standards.
- Keep a protocols directory capturing data collection, cleaning, and analysis SOPs; reference versioned datasets and commits.
- Maintain a manuscript folder independent of analysis to decouple prose from computation; link to figures and tables generated into outputs.
- Register DOIs for datasets or releases when publishing.

Anti-patterns to avoid

- Committing large raw files without LFS/DVC.
- Embedding results or figures inside notebooks only; export artifacts and list them in outputs.
- Inconsistent environment management across collaborators.

2) TCC projects (Brazilian undergraduate or graduate capstone)
Goals

- Conformity to institutional standards (e.g., ABNT formatting), clear audit trail for methodology, and presentable artifacts (manuscript, slides, code/data when applicable).

Key practices

- Use a docs/tcc structure matching pre-textual, textual, post-textual ABNT sections; keep templates and class files in templates.
- Store references in refs with a single source of truth (BibTeX or citation manager exports); add a Make target to regenerate bibliography.
- If research involves human subjects or data collection, store approvals in docs/artifacts/approvals; keep instrument versions and consent forms.
- For bilingual deliverables, mirror key documents in pt-BR and en, keeping translation status in front matter.
- Treat the TCC like a project: timeline, milestones, and a Makefile or tasks workflow for building PDFs and slides.

Anti-patterns

- Writing directly in a single monolithic word processor file with embedded figures and no version control.
- Mixing final and draft figures in the same folder without naming or status metadata.

3) Multi-language development environments
Goals

- Encapsulation per language with shared standards; fast builds; clear ownership; coherent docs and i18n.

Key practices

- Decide monorepo vs polyrepo based on dependency coupling, shared libraries, and team scale.
  - Monorepo pros: Atomic changes across languages; unified tooling; simpler refactors; shared CI.
  - Monorepo cons: Tooling complexity; repo size; permissions granularity.
  - Polyrepo pros: Isolation; per-repo permissions; smaller clones; simpler per-team autonomy.
  - Polyrepo cons: Coordinating changes across repos; duplicated tooling; version skew.
- If monorepo, use a build orchestrator (Bazel, Pants, NX) to manage cross-language dependencies and caching.
- Co-locate documentation next to code while also publishing to a central site via docs aggregation.
- Use shared directories for cross-language schemas (OpenAPI, protobuf, JSON Schema). Generate clients in language-specific packages as build outputs, not hand-maintained sources.
- Manage i18n for docs in docs/i18n; for apps, keep translations in messages files per locale and domain.
- Enforce language-specific linters and formatters; pre-commit orchestrates all.

Contrarian but useful practices (flagged speculative)

- Maintain an org-wide ontology in YAML or JSON-LD that enumerates core concepts, synonyms, and relationships. Use it to validate tags and generate glossaries. This is a light-weight semantic layer that improves cross-domain search and disambiguation.
- Auto-generate hub pages: A nightly job builds topic hubs from tags and backlink analysis, including curated summaries with LLM assistance. Keep human-in-the-loop review.
- Embedding-powered search augmentation: Generate vector embeddings for docs and code, then surface semantically related items alongside traditional search results. This reduces dependence on strict folder memorization.

Decision framework and checklist

Decision questions

- Primary user mode: browse vs search? If browse high, emphasize clear taxonomy and indices; if search high, invest in metadata and search quality.
- Content mix: project-heavy vs evergreen guides? Choose project-centric or function-based top levels accordingly.
- Sensitivity: Do you handle confidential data? Plan for separate repos or restricted segments and public mirrors.
- Scale: Contributor count and velocity? Adopt stricter governance, codeowners, and CI as scale increases.
- Internationalization: Need multilingual docs? Plan i18n foldering and translation workflows early.
- Reproducibility: Research focus? Enforce raw/clean separation, environment pinning, and data versioning.

Implementation checklist

- Define and document top-level taxonomy and naming rules.
- Establish docs-as-code toolchain: repo, CI, linters, static site build, preview.
- Create templates: README index template, ADR template, protocol template, codebook template.
- Configure search: index body and metadata; consider embeddings.
- Set up access controls and codeowners.
- Schedule lifecycle reviews and pruning cadence.
- Provide onboarding: short guide on where things go and how to contribute.

Migration strategy from ad hoc structures

- Inventory: Crawl existing content; extract metadata (author, date, tags) and map to new taxonomy.
- Design: Socialize the proposed taxonomy and folder templates; pilot with a subset.
- Migrate: Automate moves with scripts that also insert front matter and create redirects.
- Communicate: Publish a migration guide with before/after examples and mapping rules.
- Validate: Run linkcheck and search indexing; collect user feedback.
- Retire: Archive legacy paths with redirects for a defined period.

Risks and anti-patterns

- Overly deep hierarchies: Users get lost; navigation becomes brittle. Mitigate with indices and tags.
- Taxonomy churn: Frequent top-level changes break muscle memory. Stabilize top-level and adjust sublevels.
- Folksonomy sprawl: Uncontrolled tags create noise. Govern a controlled vocabulary.
- Orphaned content: Docs not linked from any index decay. Enforce link coverage checks.
- Binary bloat in git: Use LFS/DVC and artifacts stores.
- Single-owner knowledge silos: Require codeowners and shared review to reduce bus factor.

Metrics and continuous improvement

- Findability: Time-to-doc and search success rates; click depth from landing to target.
- Health: Broken link rate, stale content ratio (no updates > 12 months), review SLA adherence.
- Coverage: Percentage of folders with index READMEs and front matter compliance.
- Performance: Site build times, search latency.
- Adoption: Contributor count, PR throughput, and distribution across teams.

Appendix A: README index template

```markdown
# Folder overview

Purpose: Brief purpose of this folder and how it fits in the taxonomy.

Contents
- Subfolder A: what it contains, when to use it.
- Subfolder B: ...

Related
- See also: links to related guides, projects, ADRs.

Ownership
- Owner: team or person
- Reviewers: list

Status
- Last reviewed: YYYY-MM-DD
```

Appendix B: Naming cheatsheet

- Use lowercase and hyphens: data-raw, data-clean, model-eval.
- Prefix by type if helpful: adr-2025-01-12-..., rfc-..., sop-....
- Dates: YYYY-MM-DD for time-series content; avoid ambiguous formats.
- Identifiers: proj-xyz, dataset-2025-ml-001.

Appendix C: Example front matter fields

```yaml
---
title: Title here
authors: [handle]
status: draft | in-review | published | deprecated | archived
tags: [domain, technology, method]
confidentiality: public | internal | restricted
created: 2025-09-06
updated: 2025-09-06
related: [links or IDs]
license: CC-BY-4.0
---
```

Closing recommendations

- Choose a stable, function-oriented top-level taxonomy, then maintain project spaces beneath it and use tags for cross-cuts. Keep hierarchies shallow, name consistently, and document everything with front matter and index files.
- Treat the knowledge base as a product: define owners, SLAs, CI, and metrics. Automate checks and previews to keep quality high as contributors scale.
- For research and TCCs, prioritize reproducibility and compliance: separate raw/processed data, pin environments, track approvals, and keep manuscripts alongside but decoupled from computation.
- For multi-language development, prefer monorepo with orchestration if teams frequently coordinate across languages; otherwise polyrepo with a strong docs aggregation site. Always co-locate docs with code and publish to a central, searchable portal with i18n support.
- Revisit the taxonomy quarterly, prune aggressively, and keep the first click obvious. These habits sustain a living knowledge base rather than a slowly decaying archive.

## Sources

The research was conducted using the Deep Research MCP tool with academic-grade source evaluation, covering established information architecture principles, software engineering practices, and documentation methodologies. Sources include mainstream dev tooling practices, reproducible research methodologies, and recognized records management standards (ISO-style records management, FAIR data principles) validated across software documentation, research data management, and personal knowledge management communities.

---
