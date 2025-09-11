Title: Designing an Enforceable, Hierarchical Knowledge Base and Academic Development Workspace (with Git-based Validation and Pre-commit Enforcement)

Executive summary

- Goal: Define a robust, scalable, and enforceable information architecture for an academic knowledge base and development workspace; specify a hierarchical folder structure; formalize a classification/taxonomy model; and implement automated enforcement and validation via git pre-commit hooks and CI.
- Approach: Combine a clean, discoverable hierarchy (for predictable paths) with controlled, faceted metadata (for flexibility and search), codify policy as machine-readable schemas, and enforce via local hooks and CI. Leverage widely adopted standards and tools (FAIR data, JSON Schema, Conventional Commits, SPDX licenses, Git LFS/DVC/DataLad, frictionless data, pre-commit framework, markdown/yaml linters, secrets scanning, and link checks).
- Outcome: A blueprint you can implement immediately: directory structure, naming conventions, metadata schemas, pre-commit configuration, validation scripts, and CI guidance, including migration, governance, and risk management.

Principles and standards referenced (reliability notes)

- FAIR data principles (Findable, Accessible, Interoperable, Reusable) to structure datasets and metadata. These are widely accepted in research data management.
- ISO 8601 for dates and times (YYYY-MM-DD[Thh:mm:ssZ]) to guarantee lexical sortability and unambiguous timestamps.
- Semantic Versioning (SemVer) for code and dataset versioning (proven in software ecosystems; well-understood by developers).
- SPDX license identifiers and REUSE recommendations for explicit, machine-readable licensing (common compliance frameworks in open-source).
- Conventional Commits for structured commit messages (broadly used; enables automated changelogs and semantic release).
- Dublin Core as a conceptual crosswalk for basic scholarly metadata fields (title, creator, date, subject, etc.). We recommend mapping your metadata fields to DC for interoperability but keep your internal schemas concise.
- Frictionless Data “datapackage.json” or equivalent JSON Schema for dataset descriptors (well-established in open data packaging).
- Git- and CI-based enforcement using the pre-commit framework, GitHub Actions/GitLab CI, and optionally server-side hooks for on-premise Git.
- Cookiecutter Data Science and similar project templates as a proven baseline (we adapt, not adopt verbatim).

Information architecture overview

- Hybrid organization model
  - Hierarchical for path discoverability and predictable policies. Paths encode category semantics and minimize cognitive load when navigating.
  - Faceted metadata via controlled vocabularies/tags for flexibility, cross-cutting classification, and search without re-laying directories.
- Faceted tags are validated (enumerations and controlled vocabularies) so they remain consistent and machine-queriable.
- A single “policy-as-code” file defines allowed directories, filename patterns, required metadata fields, and required files. Hooks read this policy to enforce compliance.

Top-level directory structure (Johnny Decimal-inspired hierarchy with PARA-compatible lifecycle)

- 00-admin/ — Governance and repository meta
  - CODEOWNERS, CONTRIBUTING.md, GOVERNANCE.md, SECURITY.md, .editorconfig, .gitattributes, .gitignore, CITATION.cff
  - .kb/ — Knowledge base policy, schemas, and scripts
    - policy/ — Policy files (YAML/JSON)
    - schemas/ — JSON Schemas for metadata/front matter
    - scripts/ — Validation scripts called by hooks
    - vocab/ — Controlled vocabularies (YAML/CSV) and taxonomy definitions
    - templates/ — Cookiecutter/new-item templates
- 10-knowledge/ — Notes, literature, concepts (Zettelkasten-friendly)
  - notes/ — Atomic notes with unique IDs and YAML front matter
  - lit/ — Literature PDFs, BibTeX, and summaries
    - library.bib, pdfs/YYYY/AuthorYear-ShortTitle-key.pdf
    - betterbibtex-keys.md (documentation of citation key policy)
  - glossaries/ — Domain glossaries, term definitions
- 20-projects/ — Active and historical projects (one folder per project)
  - PRJ-<year><seq>-<slug>/ (e.g., PRJ-2025A3-graph-embeddings)
    - docs/, notebooks/, src/, tests/, env/, ci/, reports/
    - data/ (symlinks to 30-data datasets or DVC/DataLad tracked artifacts)
    - experiments/ (see 50-experiments for centralized tracking)
    - manuscripts/ (if project-specific)
- 30-data/ — Datasets (versioned, FAIR-aligned)
  - DSET-<slug>/
    - raw/, interim/, processed/, external/
    - datapackage.json or dataset.json (JSON Schema/Frictionless descriptor)
    - README.md, LICENSE, MANIFEST.csv/manifest.json with checksums
    - .gitattributes rules; optionally DVC/DataLad configs
- 40-code/ — Shared libraries, tooling, reusable modules
  - py/ or lang-separated (py/, r/, js/, etc.) with conventional src/ layout
  - VERSION, LICENSE, README, pyproject.toml/requirements.txt
- 50-experiments/ — Reproducible experiments and runs
  - EXP-<yyyymmdd>-<slug>/
    - config/, runs/, artifacts/, metrics/, notebooks/
    - mlflow/ or dvc.yaml if applicable
- 60-manuscripts/ — Papers, theses, grants, and reviews
  - MS-<yyyy>-<venue>-<slug>/
    - text/ (md or tex), figs/, tables/, supp/, refs.bib
    - metadata.yaml with authors (ORCIDs), affiliations, target journal
- 70-presentations/ — Talks, seminars, posters
  - PRES-<yyyy>-<event>-<slug>/ (source + exported PDF)
- 80-resources/ — Templates, style guides, reusable checklists
  - cookiecutters/, pandoc/, latex/, word/, slides/
- 90-archive/ — Cold storage for retired projects/materials
  - mirror structure; only archived items moved here with status=archived

Rationale

- Discoverability: Johnny Decimal-like numerical prefixes provide stable, human-sortable categories. PARA concepts (Projects/Areas/Resources/Archives) align with 20/80/90 groups.
- Reproducibility: Clear separation of raw/interim/processed data and code vs experiments supports provenance tracking.
- Portability: Minimal coupling to any one tool; viable in GitHub/GitLab, local, or on-prem environments.

Classification model (hierarchical + faceted)

- Hierarchical classification encodes primary category semantics in the path (e.g., 30-data/DSET-genomics/processed). This reduces ambiguity and supports policy-by-path.
- Faceted classification via controlled tags in metadata front matter or metadata.yaml:
  - facets: domain, modality, method, topic, status, sensitivity, license, reproducibility-level, stage
  - controlled vocab: maintain vocab/*.yaml for enumerations and synonyms
  - example: domain: [nlp, bioinformatics], sensitivity: [public, restricted, controlled]
- Authority control: Use identifiers where possible
  - Authors with ORCID
  - Datasets with DOI or internal persistent ID (PID)
  - Papers with DOI/arXiv ID

Metadata conventions

- YAML front matter in Markdown files for notes, manuscripts, experiment logs
  - Required fields (example for a note):
    - id: 20250911-143210-zk12
    - title: Short descriptive title
    - created: 2025-09-11T14:32:10Z
    - updated: 2025-09-11T15:06:20Z
    - tags: [topic/ml, method/graph, priority/medium]
    - links: [PRJ-2025A3-graph-embeddings, DSET-openwebtext]
    - status: draft|active|archived
- Dataset metadata (dataset.json or datapackage.json)
  - name, title, description, version (SemVer), created, modified
  - contributors (name, orcid, role), license (SPDX), keywords/tags
  - sources (DOIs/URLs)
  - schema/resources (field names, types, constraints)
  - distribution (access URLs, formats), size, checksums
- Manuscripts metadata (metadata.yaml)
  - title, abstract, authors (with orcid, affiliation), venue, keywords
  - related datasets/code (PIDs), funding info (grant IDs), license
- Map core fields to Dublin Core for interoperability (internal fields remain concise; crosswalk doc in 00-admin/).

Naming conventions

- Filenames and directory names use lower-kebab-case or snake_case; avoid spaces.
- Time: ISO 8601 dates (YYYY-MM-DD) and timestamps for IDs. Example ID generator: yyyymmddhhmmss + short slug.
- Projects: PRJ-<year><alphanum-seq>-<slug> (e.g., PRJ-2025A3-graph-embeddings). The alphanum sequence avoids collisions by team.
- Experiments: EXP-<yyyymmdd>-<slug> (day-level grouping; runs nested inside with a hash/UUID or run-001).
- Datasets: DSET-<slug>; versions via SemVer in metadata, not filename. Instead, processed/1.2.0 directory or DVC tags.
- Manuscripts: MS-<yyyy>-<venue>-<slug> and keep the canonical text as index.md or main.tex.
- PDF literature: AuthorYear-ShortTitle-key.pdf to align with BibTeX keys.
- Branch names: type/short-description (feat/add-graph-encoder), where type in {feat, fix, chore, docs, refactor, test, perf}.
- Commit messages: Conventional Commits.

Automated enforcement stack

- Local: pre-commit hooks enforce structure, formatting, metadata, and security before commits land.
- Remote: CI re-runs validations for defense-in-depth; branch protection requires CI green.
- Optional: Server-side Git hooks (on self-hosted Git) for last-mile enforcement.

Pre-commit configuration (example)

- Save as .pre-commit-config.yaml at repo root.

```
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: detect-private-key
      - id: check-added-large-files
        args: ['--maxkb=51200']  # 50 MB threshold; rely on LFS/DVC beyond this

  - repo: https://github.com/adrienverge/yamllint
    rev: v1.35.1
    hooks:
      - id: yamllint

  - repo: https://github.com/codespell-project/codespell
    rev: v2.3.0
    hooks:
      - id: codespell

  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.41.0
    hooks:
      - id: markdownlint

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black

  - repo: https://github.com/nbQA-dev/nbQA
    rev: 1.9.0
    hooks:
      - id: nbqa-ruff
        additional_dependencies: ['ruff==0.6.9']
      - id: nbqa-black
        additional_dependencies: ['black==24.10.0']

  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets

  - repo: local
    hooks:
      - id: kb-structure-validate
        name: Validate knowledge base structure
        entry: python3 .kb/scripts/validate_tree.py
        language: system
        pass_filenames: false
      - id: kb-metadata-validate
        name: Validate metadata schemas
        entry: python3 .kb/scripts/validate_metadata.py
        language: system
        files: '\\.(md|yaml|yml|json)$'
      - id: kb-filename-policy
        name: Enforce filename policy
        entry: python3 .kb/scripts/check_filenames.py
        language: system
        files: '.*'

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.30.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

Notes

- The local hooks use language: system to keep control. Ensure Python deps are installed (see .kb/requirements.txt). Alternative: language: python with additional_dependencies to auto-install PyYAML/jsonschema.
- Install hooks with: pre-commit install && pre-commit install -t commit-msg.

Policy-as-code (folder and metadata validation)

- Core policy file (example: .kb/policy/kb-policy.yaml)

```
version: 1
naming:
  case: kebab  # kebab|snake
  forbid_spaces: true
  allowed_chars: '^[a-z0-9._\-/]+'  # simple guard; scripts enforce stricter patterns per path
paths:
  - path: '10-knowledge/notes'
    filename: '^[0-9]{8,14}-[a-z0-9-]+\\.md$'
    require_front_matter: true
    schema: '.kb/schemas/note.schema.json'
  - path: '10-knowledge/lit/pdfs'
    filename: '^[A-Z][a-zA-Z]+[0-9]{4}-[A-Za-z0-9-]+-[-_A-Za-z0-9]+\\.pdf$'
  - path: '20-projects/PRJ-[0-9A-Z]+-[a-z0-9-]+'
    required_files: ['README.md', 'docs/']
  - path: '30-data/DSET-[a-z0-9-]+'
    required_files: ['README.md', 'dataset.json']
    schema: '.kb/schemas/dataset.schema.json'
  - path: '50-experiments/EXP-[0-9]{8}-[a-z0-9-]+'
    required_files: ['config/', 'runs/']

require:
  - path: '00-admin/CITATION.cff'
  - path: '00-admin/CONTRIBUTING.md'
  - path: '.pre-commit-config.yaml'

metadata:
  controlled_vocabs:
    status: ['draft', 'active', 'archived']
    sensitivity: ['public', 'restricted', 'controlled']
    license_spdx: ['CC-BY-4.0', 'MIT', 'Apache-2.0']
```

- Note front matter schema (note.schema.json)

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/schemas/note.schema.json",
  "type": "object",
  "required": ["id", "title", "created", "status"],
  "properties": {
    "id": { "type": "string", "pattern": "^[0-9]{8,14}-[a-z0-9]{2,6}$" },
    "title": { "type": "string", "minLength": 3 },
    "created": { "type": "string", "format": "date-time" },
    "updated": { "type": "string", "format": "date-time" },
    "status": { "type": "string", "enum": ["draft", "active", "archived"] },
    "tags": { "type": "array", "items": { "type": "string" } },
    "links": { "type": "array", "items": { "type": "string" } }
  },
  "additionalProperties": true
}
```

- Dataset schema (dataset.schema.json) minimal example

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/schemas/dataset.schema.json",
  "type": "object",
  "required": ["name", "title", "version", "license", "created"],
  "properties": {
    "name": { "type": "string", "pattern": "^DSET-[a-z0-9-]+$" },
    "title": { "type": "string" },
    "version": { "type": "string", "pattern": "^\n?\n?\n?([0-9]+)\.([0-9]+)\.([0-9]+)$" },
    "created": { "type": "string", "format": "date-time" },
    "modified": { "type": "string", "format": "date-time" },
    "license": { "type": "string" },
    "contributors": { "type": "array", "items": { "type": "object", "properties": {
      "name": { "type": "string" },
      "orcid": { "type": "string", "pattern": "^\n?\n?\n?0000-000[0-9]-[0-9]{4}-[0-9]{3}[0-9X]$" },
      "role": { "type": "string" }
    } } },
    "keywords": { "type": "array", "items": { "type": "string" } },
    "resources": { "type": "array" }
  },
  "additionalProperties": true
}
```

Implementation scripts (sketches)

- .kb/scripts/validate_tree.py: validates required paths, required files, and filename regex policies against kb-policy.yaml.

```
#!/usr/bin/env python3
import os, re, sys, yaml

POLICY = '.kb/policy/kb-policy.yaml'

class Violation(Exception):
    pass

def load_policy():
    with open(POLICY, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def check_required(repo_root, policy):
    errors = []
    for req in policy.get('require', []):
        path = os.path.join(repo_root, req['path'] if isinstance(req, dict) else req)
        if not os.path.exists(path):
            errors.append(f"Missing required path: {path}")
    return errors


def match_any(patterns, relative_path):
    for p in patterns:
        if re.search(p, relative_path):
            return True
    return False


def check_paths(repo_root, policy):
    errors = []
    path_rules = policy.get('paths', [])
    # Pre-compile regex and expand rules
    compiled = []
    for r in path_rules:
        compiled.append({
            'path': re.compile(r['path']),
            'filename': re.compile(r['filename']) if 'filename' in r else None,
            'required_files': r.get('required_files', []),
        })
    # Walk
    for root, dirs, files in os.walk(repo_root):
        rel = os.path.relpath(root, repo_root)
        if rel == '.':
            continue
        for rule in compiled:
            if rule['path'].search(rel):
                # Check filenames under this path
                if rule['filename']:
                    for fn in files:
                        if not rule['filename'].match(fn):
                            errors.append(f"Filename policy violation in {rel}: {fn}")
                # Check required files
                for rf in rule['required_files']:
                    if not os.path.exists(os.path.join(root, rf)):
                        errors.append(f"Missing required file in {rel}: {rf}")
    return errors


def main():
    repo_root = os.getcwd()
    policy = load_policy()
    errors = []
    errors += check_required(repo_root, policy)
    errors += check_paths(repo_root, policy)
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

- .kb/scripts/validate_metadata.py: extracts front matter from .md files and validates according to JSON Schema; validates standalone YAML/JSON against schema.

```
#!/usr/bin/env python3
import os, sys, json, yaml
from jsonschema import validate, Draft202012Validator

# map path patterns to schemas, fallback to front matter schema specified in policy if any
SCHEMA_MAP = {
    '10-knowledge/notes': '.kb/schemas/note.schema.json',
    '30-data/DSET-': '.kb/schemas/dataset.schema.json',
}


def load_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_front_matter_md(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines or not lines[0].strip().startswith('---'):
        return None
    # find end of front matter
    for i in range(1, len(lines)):
        if lines[i].strip().startswith('---'):
            fm = ''.join(lines[1:i])
            return yaml.safe_load(fm) or {}
    return None


def applicable_schema_for(path):
    rel = path.replace('\\', '/')
    for k, v in SCHEMA_MAP.items():
        if k in rel:
            return v
    return None


def validate_obj(obj, schema_path):
    schema = load_schema(schema_path)
    v = Draft202012Validator(schema)
    errs = sorted(v.iter_errors(obj), key=lambda e: e.path)
    return [f"{e.message} at {list(e.path)}" for e in errs]


def main(paths):
    errors = []
    for path in paths:
        if path.endswith('.md'):
            fm = extract_front_matter_md(path)
            schema_path = applicable_schema_for(path)
            if schema_path and fm is not None:
                errs = validate_obj(fm, schema_path)
                errors += [f"{path}: {e}" for e in errs]
        elif path.endswith('.yaml') or path.endswith('.yml'):
            schema_path = applicable_schema_for(path)
            if schema_path:
                with open(path, 'r', encoding='utf-8') as f:
                    obj = yaml.safe_load(f) or {}
                errs = validate_obj(obj, schema_path)
                errors += [f"{path}: {e}" for e in errs]
        elif path.endswith('.json'):
            schema_path = applicable_schema_for(path)
            if schema_path:
                with open(path, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                errs = validate_obj(obj, schema_path)
                errors += [f"{path}: {e}" for e in errs]
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # pre-commit passes filenames by default; but we configured files: to select types
        print('No files to validate; exiting.')
        sys.exit(0)
    main(sys.argv[1:])
```

- .kb/scripts/check_filenames.py: enforces global naming policy (kebab/snake, no spaces, allowed characters).

```
#!/usr/bin/env python3
import os, re, sys, yaml

POLICY = '.kb/policy/kb-policy.yaml'


def load_policy():
    with open(POLICY, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main(paths):
    policy = load_policy()
    forbid_spaces = policy.get('naming', {}).get('forbid_spaces', True)
    allowed_chars = policy.get('naming', {}).get('allowed_chars', None)
    pattern = re.compile(allowed_chars) if allowed_chars else None

    errors = []
    for path in paths:
        # skip .git and virtual envs
        if '/.git/' in path or '/.venv/' in path or path.startswith('.git/'):
            continue
        name = os.path.basename(path)
        if forbid_spaces and ' ' in name:
            errors.append(f"Spaces not allowed: {path}")
        if pattern and not all(pattern.match(ch) for ch in name):
            # coarse filter: check entire name against allowed set via substitution
            if not re.match(r'^[a-z0-9._\-]+$', name):
                errors.append(f"Disallowed chars in: {path}")
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit(0)
    main(sys.argv[1:])
```

Dependency setup

- .kb/requirements.txt
  - pyyaml>=6.0.1
  - jsonschema>=4.21.0

- Install before enabling pre-commit: pip install -r .kb/requirements.txt

Complementary CI enforcement

- GitHub Actions example (.github/workflows/validate.yml)

```
name: validate
on: [push, pull_request]
jobs:
  precommit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pre-commit
      - run: pip install -r .kb/requirements.txt
      - run: pre-commit run --all-files
```

- Protect main branches: require status checks to pass, signed commits if policy requires.

Data and large file handling

- Git LFS for large binaries (configure a threshold in pre-commit “check-added-large-files” and .gitattributes patterns). Example .gitattributes:

```
*.ipynb filter=nbstripout
*.csv text eol=lf
*.tsv text eol=lf
*.pdf binary
*.png binary
*.jpg binary
*.zip filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text
30-data/** filter=lfs diff=lfs merge=lfs -text
```

- For rigorous provenance and versioning, consider DVC or DataLad (reliable tools for data pipelines and annexed storage). Both integrate with Git and CI.

Reproducible environments and tasks

- Standardize environment files: env/conda.yaml or pyproject.toml/requirements.txt. Pin at least major/minor versions for determinism.
- Task runner: Makefile or just/Taskfile for common workflows (lint, test, docs, validate, build).
- Reproducible notebooks: nbstripout to remove outputs; nbQA to lint; prefer modular code in src/ with notebooks as thin wrappers.

Literature and citation management

- Manage references in Zotero; export to library.bib; enforce citation key policy (Better BibTeX) documented in 10-knowledge/lit.
- Store annotated PDFs with consistent naming; avoid committing large libraries without LFS.
- Link notes to BibTeX keys in front matter (links: [@Smith2023Deep]).

Manuscripts and docs

- Authoring in Markdown + Pandoc or LaTeX; keep refs.bib per manuscript or reference 10-knowledge/lit/library.bib.
- Ensure CITATION.cff at 00-admin/ to make citation metadata discoverable by code hosts.

Validation suite details (beyond pre-commit defaults)

- Link checking for Markdown: lychee or markdown-link-check in CI.
- DOI/ORCID patterns check: custom pre-commit or embed in jsonschema “pattern”.
- Metadata completeness checks (e.g., no dataset without license; no manuscript without venue).
- Manifest validation: require manifest with checksums for 30-data DSET-*/processed.
- Secrets scanning: detect-secrets baseline file .secrets.baseline; update via detect-secrets scan.

Workflows

- Create a new project
  - cookiecutter .kb/templates/project -> prompts for PRJ id, creates skeleton.
  - Pre-commit ensures names and required files are present.
- Add a new dataset
  - Create 30-data/DSET-<slug>/; copy template dataset.json; fill metadata; use frictionless validate or schema validation.
  - For large artifacts, add to DVC or LFS. Commit manifest hashes.
- Write an atomic note
  - Use a script .kb/scripts/new_note.py to generate ID and template front matter. Place in 10-knowledge/notes.
- Run validations locally
  - pre-commit run --all-files
- Release
  - Tag with SemVer for code libraries; for datasets, update version in dataset.json and tag with dset/<name>@<version>.

Governance and roles

- Code owners: CODEOWNERS mapping to paths (e.g., 30-data/ -> Data steward; 60-manuscripts/ -> PI + corresponding author).
- Approvals: Protected branches require review by owner of the path touched.
- Policy evolution: policy versioned in .kb/policy; changes require RFC-style PR with migration notes.

Migration plan

- Inventory current repos and content; classify mapping to target structure.
- Automate renames and moves with a script that (a) adds front matter to Markdown, (b) generates dataset.json from existing README where possible, (c) updates links.
- Introduce pre-commit in “warn-only” mode in CI first (non-blocking), then make blocking after a grace period.
- Provide training and quick-reference guides; include a “why” doc to reduce resistance.

Metrics and KPIs

- Structural compliance: % of files passing filename and path policies.
- Metadata completeness: % of notes/datasets/manuscripts satisfying required fields.
- Link health: # of broken links over time.
- Secrets incidents: count and time-to-remediation.
- Reproducibility: % of experiments with runnable configs and environment lockfiles; % successful reruns in CI on clean runner.
- Time-to-locate: median time to locate a dataset/manuscript/note in user tests.

Risks and mitigations

- Over-rigidity causing friction
  - Mitigation: Light-touch defaults, clear exemptions (e.g., allow legacy area 90-archive/* to be less strict), provide autofix scripts and templates.
- False positives in validation
  - Mitigation: Staged rollout; log-only mode first; tune regexes; maintain allowlists.
- Tool sprawl
  - Mitigation: Consolidate into pre-commit and a single CI pipeline; document minimal required tools.
- Large files clogging Git
  - Mitigation: Enforce size threshold; mandate LFS or DVC; add CI guard to refuse blobs over limit in non-LFS paths.
- Sensitive data leakage
  - Mitigation: secrets scanning; clear sensitivity facet; require encryption or external storage for restricted datasets; maintain data access policy.

Contrarian and forward-looking options (flagged as speculative)

- Tag-first, flat directories with heavy faceting and search (e.g., Obsidian/Tana/Notion as UI). Pros: flexibility; Cons: weak policy enforcement across tools; migration risk.
- Content-addressable storage (CAS) for datasets (ipfs/nerdctl registry); stable by-hash references; Cons: onboarding cost.
- Nix or Guix for fully reproducible environments; strong determinism with higher adoption barrier.
- Monorepo vs multi-repo: a single lab monorepo simplifies global policy enforcement; multi-repo isolates risk and access but duplicates policy. Consider a monorepo for knowledge + templates and project repos for heavy code/data.
- CRDT-based notes (e.g., local-first) synced to Git to reduce merge conflicts in note-taking; early but promising.

Roadmap (phased delivery)

- Phase 0 (1–2 weeks): Draft policy, directory map, and schemas; pilot in a sandbox repo; prepare templates.
- Phase 1 (2–4 weeks): Implement pre-commit, CI, and minimal scripts; migrate 1–2 representative projects and 1 dataset; collect feedback.
- Phase 2 (4–8 weeks): Broader migration; add link checking, secrets baseline, and DVC/DataLad for heavy datasets; train team.
- Phase 3 (ongoing): Tune taxonomies, add dashboards for KPIs, automate doc site generation (e.g., mkdocs) from knowledge/ and datasets.

Appendix A: Example README skeletons

- 20-projects/PRJ-*/README.md
  - Overview, objectives, scope
  - Structure map with brief descriptions
  - Data dependencies (DSET-*) and licenses
  - Environment and quickstart (make setup, make test)
  - Contacts and governance

- 30-data/DSET-*/README.md
  - Description, provenance, license
  - Schema and fields
  - Versioning policy; changelog
  - Access instructions and sensitivity designation

Appendix B: Commit message policy (Conventional Commits)

- feat:, fix:, docs:, style:, refactor:, perf:, test:, chore:
- Optional scope: feat(experiments): …
- Body includes rationale and links to PRJ/EXP IDs; footer with BREAKING CHANGE if applicable.

Appendix C: Editor settings (.editorconfig)

```
root = true
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
indent_style = space
indent_size = 2
[*.py]
indent_size = 4
```

Appendix D: CITATION.cff (skeleton)

```
cff-version: 1.2.0
title: Example Lab Knowledge Base and Workspace
authors:
  - family-names: Doe
    given-names: Jane
    orcid: https://orcid.org/0000-0002-1825-0097
identifiers:
  - type: doi
    value: 10.1234/example.doi
license: MIT
message: >
  If you use this repository, please cite it using the metadata above.
```

Appendix E: Practical policies for reliability

- Do not rely exclusively on filenames for semantics; always mirror in front matter/metadata.
- Keep schemas small and stable; evolve via versioning and migration scripts.
- Prefer enumerations for high-value facets (status, sensitivity, license) to reduce entropy.
- Require READMEs at key nodes (dataset, project, manuscript) with minimal, validated front matter.

Closing recommendations

- Start with the proposed hierarchy and minimal schema set; enforce with pre-commit to create immediate, low-latency feedback.
- Add CI as a second line of defense and to protect shared branches.
- Invest in templates and small CLI helpers; consistency grows when the easiest path is also the compliant one.
- Review metrics quarterly; tune policies to reduce toil while increasing signal.
- Treat policy as code: tests, reviews, versioning, and changelogs apply equally to your knowledge base governance.

## Sources
