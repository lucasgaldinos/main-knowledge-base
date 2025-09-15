---
title: Script Standardization Guidelines
description: Governance framework for choosing between Shell and Python scripts in
  infrastructure automation
status: active
created: '2025-09-10'
updated: '2025-09-15'
tags:
- infrastructure
- scripting
- governance
- automation
- standards
version: 1.1.0
---


# Script Standardization Guidelines

## Executive Summary

This document establishes clear governance for script technology choices in the infrastructure automation suite, based on complexity thresholds and functional requirements.

## Technology Selection Criteria

### Use Shell/Bash For

**Complexity Threshold**: ≤50 lines, simple logic
**Functional Criteria**:

- Basic file system operations (move, copy, delete)
- Simple Git operations and repository maintenance
- Environment setup and validation
- Quick utility scripts without complex logic
- CI/CD pipeline steps with standard Unix tools
- System command orchestration

**Example Use Cases**:

```bash
# Simple file organization
#!/bin/bash
set -euo pipefail
mv docs/*.md knowledge/foundations/
echo "✅ Files moved successfully"
```

### Use Python For

**Complexity Threshold**: >50 lines OR complex logic
**Functional Criteria**:

- YAML/JSON processing and content analysis
- Database operations and analytics
- Multi-step workflows with error recovery
- External API integrations
- Complex data processing and validation
- Content classification and intelligent metadata generation

**UV Environment Requirements**:

- All Python scripts must be compatible with UV package manager
- Use `uv run script.py` for execution in CI/CD environments
- Declare dependencies in `pyproject.toml` with appropriate version constraints
- Support virtual environment isolation through UV's built-in environment management

**Example Use Cases**:

```python
# Complex automation with error handling
import yaml
import sqlite3
from pathlib import Path

def process_frontmatter(file_path):
    # Complex logic with proper error handling
    pass
```

## Standardized Interfaces

### Common Command-Line Arguments

All scripts must support:

```bash
--verbose       # Detailed output
--dry-run       # Preview mode without changes
--help         # Usage information
--quiet        # Minimal output for CI/CD
```

### Exit Codes

```bash
0    # Success
1    # General error
2    # Invalid usage/arguments
3    # Missing dependencies
```

### UV Environment Management

**Project Structure Requirements**:

```toml
# pyproject.toml - Root level configuration
[project]
name = "workspace-automation"
version = "0.1.0"
description = "Academic workspace automation scripts"
dependencies = [
    "pyyaml>=6.0",
    "rich>=13.0",
    "click>=8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1.0",
]
```

**Execution Patterns**:

```bash
# Preferred execution method for Python scripts
uv run scripts/maintain_organization.py --verbose

# Task automation integration
uv run --no-project scripts/validate_structure.py

# Development and testing
uv run pytest scripts/test_*.py
```

**Environment Validation**:

```python
# Check UV environment availability
def check_uv_environment():
    """Validate UV environment and dependencies."""
    try:
        import subprocess
        result = subprocess.run(['uv', '--version'], capture_output=True)
        if result.returncode == 0:
            logger.info(f"UV available: {result.stdout.decode().strip()}")
            return True
    except FileNotFoundError:
        logger.warning("UV not found, falling back to system Python")
    return False
```

### Logging Format

```log
[TIMESTAMP] [LEVEL] [SCRIPT_NAME] MESSAGE
[2025-09-10 15:30:45] [INFO] [yaml-enforcer] Processing 45 files
[2025-09-10 15:30:46] [ERROR] [yaml-enforcer] Invalid YAML in file.md
```

### Output Format

- **Structured Data**: JSON for machine consumption
- **Human Output**: Clear, actionable messages with emoji indicators
- **CI/CD Output**: Concise, parseable format

## Migration Thresholds

### Automatic Migration Triggers

**Shell → Python Migration Required When**:

- Script exceeds 40 lines (warning at 35 lines)
- Needs complex error handling or retry logic
- Requires data structure manipulation
- Needs external API calls or database operations
- Becomes difficult to test or debug

**Python → Shell Migration Considered When**:

- Script only performs basic file operations
- No complex logic or data processing
- Pure system command orchestration
- Performance is critical for simple operations

## Quality Standards

### Shell Script Requirements

```bash
#!/bin/bash
# Script description and purpose
# Usage: script.sh [options]

set -euo pipefail  # Strict error handling

# Global variables in UPPER_CASE
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERBOSE=false

# Function definitions with documentation
# Args: $1 - description
# Returns: 0 on success, 1 on error
function_name() {
    local arg1="$1"
    # Function implementation
}

# Main execution with error handling
main() {
    # Script logic
}

# Only execute if run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### Python Script Requirements

```python
#!/usr/bin/env python3
"""
Script description and purpose.

Usage:
    script.py [options]
    uv run script.py [options]  # Preferred execution method

Examples:
    uv run script.py --verbose --dry-run
    python script.py --help
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)

def main() -> int:
    """Main execution function."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    
    args = parser.parse_args()
    
    try:
        # Script logic
        return 0
    except Exception as e:
        logger.error(f"Script failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

**UV Integration Requirements**:

- Scripts must work with `uv run` for dependency isolation
- Dependencies declared in `pyproject.toml` for version management
- Support both direct execution and UV execution modes
- Include UV compatibility testing in CI/CD validation

## Testing Standards

### Shell Script Testing

```bash
# test_script.sh
#!/bin/bash
source "$(dirname "$0")/script.sh"

test_function_name() {
    local result
    result=$(function_name "test_input")
    assert_equals "expected_output" "$result"
}

# Run tests
test_function_name
echo "✅ All shell tests passed"
```

### Python Script Testing

```python
# test_script.py
import unittest
from script import main_function

class TestScript(unittest.TestCase):
    def test_main_function(self):
        result = main_function("test_input")
        self.assertEqual("expected_output", result)

if __name__ == '__main__':
    unittest.main()
```

## Current Script Assessment

### maintain-organization.sh Analysis

**Current Status**: 105 lines, complex logic
**Assessment**: Exceeds complexity threshold (>50 lines)
**Recommendation**: Migrate to Python for better maintainability

**Migration Rationale**:

- Contains legacy structure references (old `docs/` organization)
- Complex directory validation logic
- Needs integration with new academic structure
- Would benefit from proper error handling and testing

### yaml-frontmatter-enforcer.py Assessment

**Current Status**: Complex Python script
**Assessment**: Correctly implemented in Python
**Recommendation**: Maintain as Python script

**Rationale**:

- Complex YAML processing and content analysis
- Database integration requirements
- Sophisticated error handling and logging
- Extensive configuration and metadata generation

## Implementation Roadmap

### Phase 1: Standards Establishment (Week 1)

- [ ] Create script standards documentation ✅
- [ ] Establish testing frameworks for both technologies  
- [ ] Set up pre-commit hooks for script validation
- [ ] Create migration templates and decision flowcharts
- [ ] **NEW**: Configure UV environment requirements and pyproject.toml ✅
- [ ] **NEW**: Update all VS Code tasks to use `uv run` execution pattern ✅

### Phase 2: Current Script Migration (Week 2)

- [ ] Migrate maintain-organization.sh to maintain_organization.py ✅
- [ ] Update script for new academic directory structure ✅
- [ ] Add comprehensive testing and error handling
- [ ] Update CI/CD pipeline integration
- [ ] **NEW**: Ensure all Python scripts work with UV execution
- [ ] **NEW**: Validate dependency declarations in pyproject.toml

### Phase 3: Governance Implementation (Week 3)

- [ ] Implement automated complexity analysis
- [ ] Create script inventory and assessment dashboard
- [ ] Establish quarterly review process
- [ ] Document decision rationale for all scripts
- [ ] **NEW**: Create UV environment validation checks
- [ ] **NEW**: Integrate UV-based execution into all automation workflows

## Decision Documentation Template

For each script, document:

```yaml
script_name: example-script
technology: python|shell
rationale: |
  Brief explanation of technology choice based on:
  - Complexity requirements
  - Functional needs
  - Maintenance considerations
complexity_score: 1-10
last_reviewed: YYYY-MM-DD
migration_candidate: true|false
```

## Monitoring and Maintenance

### Quarterly Review Process

1. **Script Inventory**: List all infrastructure scripts
2. **Complexity Assessment**: Measure lines of code and functional complexity
3. **Performance Review**: Evaluate execution time and resource usage
4. **Migration Candidates**: Identify scripts exceeding thresholds
5. **Standards Compliance**: Verify adherence to coding standards

### Automated Monitoring

```python
# Script complexity monitor
def analyze_script_complexity(script_path: Path) -> dict:
    """Analyze script complexity metrics."""
    return {
        'line_count': count_lines(script_path),
        'complexity_score': calculate_complexity(script_path),
        'technology': detect_technology(script_path),
        'migration_recommended': should_migrate(script_path)
    }
```

## Best Practices Summary

### DO

- Use shell for simple file operations and system commands
- Use Python for complex logic and data processing
- Follow standardized interfaces and error handling
- Document technology choice rationale
- Test all scripts thoroughly
- Monitor complexity and migrate when appropriate

### DON'T

- Mix technologies without clear rationale
- Create complex shell scripts without considering Python migration
- Skip error handling or logging
- Ignore testing requirements
- Let scripts grow beyond complexity thresholds
- Forget to update documentation after changes

## Conclusion

This standardization framework ensures consistent, maintainable, and appropriate technology choices for infrastructure automation. By following these guidelines, we maintain code quality while using the right tool for each specific job.

Regular review and adherence to these standards will prevent technical debt accumulation and ensure our automation suite scales effectively with project requirements.
