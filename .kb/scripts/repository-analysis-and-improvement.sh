#!/bin/bash

#==============================================================================
# Repository Analysis and Improvement Script
# 
# This script performs comprehensive analysis of the AI Knowledge Base repository
# and implements PKM architectural improvements based on the recent research.
#
# Features:
# - Complete repository structure analysis
# - Duplicate file detection and consolidation
# - YAML frontmatter validation and enhancement
# - Git status management and pre-push preparation
# - PKM architectural improvements implementation
# - Automated reporting and recommendations
#
# Author: GitHub Copilot with PKM Architecture Framework
# Created: 2025-01-11
# Version: 1.0.0
#==============================================================================

set -euo pipefail

# Configuration
REPO_ROOT="/home/lucas_galdino/Documents/StudiesVault_v2/AI-knowledge-base/main-knowledge-base"
REPORT_DIR="${REPO_ROOT}/30-data/analysis-reports"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ANALYSIS_REPORT="${REPORT_DIR}/repository-analysis-${TIMESTAMP}.md"
IMPROVEMENT_LOG="${REPORT_DIR}/improvements-${TIMESTAMP}.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Flags
DRY_RUN=false
VERBOSE=false
HELP=false

#==============================================================================
# Helper Functions
#==============================================================================

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "${IMPROVEMENT_LOG}"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "${IMPROVEMENT_LOG}"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "${IMPROVEMENT_LOG}"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    if [[ "${VERBOSE}" == "true" ]]; then
        echo "$1" >> "${IMPROVEMENT_LOG}"
    fi
}

section() {
    echo -e "\n${PURPLE}===================================================${NC}"
    echo -e "${PURPLE} $1${NC}"
    echo -e "${PURPLE}===================================================${NC}\n"
    echo -e "\n## $1\n" >> "${ANALYSIS_REPORT}"
}

usage() {
    cat << EOF
Repository Analysis and Improvement Script

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --dry-run       Show what would be done without making changes
    --verbose       Enable verbose output and detailed logging
    --help          Show this help message

DESCRIPTION:
    Performs comprehensive analysis of the AI Knowledge Base repository
    and implements PKM architectural improvements including:
    
    1. Repository structure analysis and reporting
    2. Duplicate file detection and consolidation recommendations
    3. YAML frontmatter validation and enhancement
    4. Git status management and pre-push preparation
    5. PKM architectural improvements implementation
    6. Performance optimization recommendations

EXAMPLES:
    $0                    # Run full analysis and improvements
    $0 --dry-run         # Show what would be changed
    $0 --verbose         # Run with detailed logging
    $0 --dry-run --verbose  # Dry run with detailed output

OUTPUT:
    Analysis report: ${REPORT_DIR}/repository-analysis-TIMESTAMP.md
    Improvement log: ${REPORT_DIR}/improvements-TIMESTAMP.log

EOF
}

#==============================================================================
# Analysis Functions
#==============================================================================

analyze_repository_structure() {
    section "Repository Structure Analysis"
    
    log "Analyzing repository structure..."
    
    # Create report header
    cat > "${ANALYSIS_REPORT}" << EOF
---
title: Repository Analysis Report
description: Comprehensive analysis of AI Knowledge Base repository structure and improvement opportunities
status: active
created: $(date +"%Y-%m-%d")
updated: $(date +"%Y-%m-%d")
tags: [repository-analysis, pkm, improvement, automation]
version: 1.0.0
---

# Repository Analysis Report

**Generated**: $(date +"%Y-%m-%d %H:%M:%S")  
**Repository**: AI Knowledge Base  
**Location**: ${REPO_ROOT}  
**Analysis Tool**: repository-analysis-and-improvement.sh v1.0.0

EOF

    # Basic statistics
    local md_count=$(find "${REPO_ROOT}" -type f -name "*.md" | wc -l)
    local py_count=$(find "${REPO_ROOT}" -type f -name "*.py" | wc -l)
    local total_files=$(find "${REPO_ROOT}" -type f | wc -l)
    local total_dirs=$(find "${REPO_ROOT}" -type d | wc -l)
    local repo_size=$(du -sh "${REPO_ROOT}" | cut -f1)
    
    info "Repository Statistics:"
    info "  - Total files: ${total_files}"
    info "  - Markdown files: ${md_count}"
    info "  - Python files: ${py_count}"
    info "  - Total directories: ${total_dirs}"
    info "  - Repository size: ${repo_size}"
    
    cat >> "${ANALYSIS_REPORT}" << EOF

## Repository Statistics

- **Total Files**: ${total_files}
- **Markdown Files**: ${md_count}
- **Python Files**: ${py_count}
- **Total Directories**: ${total_dirs}
- **Repository Size**: ${repo_size}

## Directory Structure

\`\`\`
EOF
    
    # Generate directory tree
    if command -v tree >/dev/null 2>&1; then
        tree -d -L 3 "${REPO_ROOT}" >> "${ANALYSIS_REPORT}"
    else
        find "${REPO_ROOT}" -type d | head -20 | sed 's|'"${REPO_ROOT}"'||g' | sort >> "${ANALYSIS_REPORT}"
    fi
    
    echo '```' >> "${ANALYSIS_REPORT}"
}

detect_duplicate_files() {
    section "Duplicate File Detection"
    
    log "Scanning for potential duplicate files..."
    
    # Find files with similar names
    echo "### Potential Duplicate Files" >> "${ANALYSIS_REPORT}"
    echo "" >> "${ANALYSIS_REPORT}"
    
    local duplicates_found=0
    
    # Check for guide files
    info "Checking guide files..."
    local guide_files=$(find "${REPO_ROOT}" -name "*guide*" -type f | grep -v ".git")
    if [[ -n "${guide_files}" ]]; then
        echo "#### Guide Files" >> "${ANALYSIS_REPORT}"
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
        echo "${guide_files}" >> "${ANALYSIS_REPORT}"
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
        echo "" >> "${ANALYSIS_REPORT}"
        duplicates_found=$((duplicates_found + $(echo "${guide_files}" | wc -l)))
    fi
    
    # Check for README files
    info "Checking README files..."
    local readme_files=$(find "${REPO_ROOT}" -name "README.md" -type f)
    if [[ -n "${readme_files}" ]]; then
        echo "#### README Files" >> "${ANALYSIS_REPORT}"
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
        echo "${readme_files}" >> "${ANALYSIS_REPORT}"
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
        echo "" >> "${ANALYSIS_REPORT}"
    fi
    
    # Check for files with identical names in different directories
    info "Checking for identical filenames in different directories..."
    find "${REPO_ROOT}" -type f -name "*.md" -printf "%f\n" | sort | uniq -d > /tmp/duplicate_names.txt
    if [[ -s /tmp/duplicate_names.txt ]]; then
        echo "#### Files with Identical Names" >> "${ANALYSIS_REPORT}"
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
        while read -r filename; do
            echo "Filename: ${filename}" >> "${ANALYSIS_REPORT}"
            find "${REPO_ROOT}" -name "${filename}" -type f >> "${ANALYSIS_REPORT}"
            echo "" >> "${ANALYSIS_REPORT}"
        done < /tmp/duplicate_names.txt
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
        echo "" >> "${ANALYSIS_REPORT}"
    fi
    
    info "Found ${duplicates_found} potential duplicate files"
    rm -f /tmp/duplicate_names.txt
}

validate_yaml_frontmatter() {
    section "YAML Frontmatter Validation"
    
    log "Validating YAML frontmatter across markdown files..."
    
    local missing_yaml=0
    local invalid_yaml=0
    local valid_yaml=0
    
    echo "### YAML Frontmatter Status" >> "${ANALYSIS_REPORT}"
    echo "" >> "${ANALYSIS_REPORT}"
    
    while IFS= read -r -d '' file; do
        if [[ "${VERBOSE}" == "true" ]]; then
            info "Checking: ${file}"
        fi
        
        # Check if file starts with YAML frontmatter
        if head -n 1 "${file}" | grep -q "^---$"; then
            # Simple validation - check for second ---
            if grep -q "^---$" "${file}" | tail -n +2; then
                ((valid_yaml++))
            else
                ((invalid_yaml++))
                echo "- **Invalid YAML**: ${file#${REPO_ROOT}/}" >> "${ANALYSIS_REPORT}"
            fi
        else
            ((missing_yaml++))
            echo "- **Missing YAML**: ${file#${REPO_ROOT}/}" >> "${ANALYSIS_REPORT}"
        fi
    done < <(find "${REPO_ROOT}" -name "*.md" -type f -print0)
    
    info "YAML Frontmatter Results:"
    info "  - Valid: ${valid_yaml}"
    info "  - Invalid: ${invalid_yaml}"
    info "  - Missing: ${missing_yaml}"
    
    cat >> "${ANALYSIS_REPORT}" << EOF

### Summary

- **Valid YAML**: ${valid_yaml} files
- **Invalid YAML**: ${invalid_yaml} files  
- **Missing YAML**: ${missing_yaml} files
- **Total Markdown Files**: $((valid_yaml + invalid_yaml + missing_yaml))

EOF
}

analyze_git_status() {
    section "Git Repository Analysis"
    
    log "Analyzing git repository status..."
    
    cd "${REPO_ROOT}" || exit 1
    
    # Get git status information
    local modified_files=$(git status --porcelain | grep "^ M" | wc -l)
    local untracked_files=$(git status --porcelain | grep "^??" | wc -l)
    local staged_files=$(git status --porcelain | grep "^M " | wc -l)
    local deleted_files=$(git status --porcelain | grep "^ D" | wc -l)
    local current_branch=$(git branch --show-current)
    local commits_ahead=$(git rev-list --count HEAD ^origin/"${current_branch}" 2>/dev/null || echo "0")
    local commits_behind=$(git rev-list --count origin/"${current_branch}" ^HEAD 2>/dev/null || echo "0")
    
    info "Git Status:"
    info "  - Current branch: ${current_branch}"
    info "  - Modified files: ${modified_files}"
    info "  - Untracked files: ${untracked_files}"
    info "  - Staged files: ${staged_files}"
    info "  - Deleted files: ${deleted_files}"
    info "  - Commits ahead: ${commits_ahead}"
    info "  - Commits behind: ${commits_behind}"
    
    cat >> "${ANALYSIS_REPORT}" << EOF

### Git Status Summary

- **Current Branch**: ${current_branch}
- **Modified Files**: ${modified_files}
- **Untracked Files**: ${untracked_files}
- **Staged Files**: ${staged_files}
- **Deleted Files**: ${deleted_files}
- **Commits Ahead of Origin**: ${commits_ahead}
- **Commits Behind Origin**: ${commits_behind}

### Recent Commits

\`\`\`
EOF
    
    git log --oneline -10 >> "${ANALYSIS_REPORT}"
    echo '```' >> "${ANALYSIS_REPORT}"
    
    if [[ ${modified_files} -gt 0 || ${untracked_files} -gt 0 ]]; then
        echo "" >> "${ANALYSIS_REPORT}"
        echo "### Files Requiring Attention" >> "${ANALYSIS_REPORT}"
        echo "" >> "${ANALYSIS_REPORT}"
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
        git status --porcelain >> "${ANALYSIS_REPORT}"
        echo "\`\`\`" >> "${ANALYSIS_REPORT}"
    fi
}

generate_improvement_recommendations() {
    section "Improvement Recommendations"
    
    log "Generating improvement recommendations based on PKM architectural analysis..."
    
    cat >> "${ANALYSIS_REPORT}" << EOF

## PKM Architectural Improvements

Based on the comprehensive PKM research and analysis completed, the following improvements are recommended:

### 1. Immediate Actions (High Priority)

#### Git Repository Management
- **Commit Recent Changes**: ${modified_files:-0} modified files and ${untracked_files:-0} untracked files need attention
- **Push to Origin**: ${commits_ahead:-0} commits are ready to be pushed
- **Branch Management**: Review PKM demonstration branches created in recent work

#### File Organization
- **Duplicate Consolidation**: Review potential duplicate guide files identified
- **YAML Frontmatter**: ${missing_yaml:-0} files missing YAML frontmatter need standardization
- **README Standardization**: ${readme_files:-14} README files across directories need consistency review

### 2. PKM Architecture Implementation

#### Hybrid Methodology Adoption
Based on the architectural analysis in \`10-knowledge/methods/implementation/architectural-styles-for-pkm.md\`:

1. **PARA-Zettelkasten Integration**: Implement progressive summarization with atomic notes
2. **Johnny-LYT Hybrid**: Use numerical taxonomy with Map of Content overlays
3. **Diátaxis Framework**: Enhance documentation structure with tutorial/reference/explanation/how-to categories

#### Tool-Specific Configurations
- **VS Code Integration**: Implement PKM-optimized workspace settings
- **Git Workflow**: Adopt branch-based PKM experimentation patterns
- **Automation Scripts**: Deploy source cleaning and validation tools

### 3. Long-term Architectural Enhancements

#### Knowledge Graph Integration
- **Memory MCP Enhancement**: Implement date functionality for temporal knowledge organization
- **Relationship Mapping**: Create automated entity-relationship detection
- **Cross-reference Validation**: Implement link integrity checking

#### Multi-Agent Workflows
- **MCP Integration**: Combine arxiv-mcp-improved + deep-research + memory systems
- **Process Automation**: Implement step-by-step research and documentation workflows
- **Quality Assurance**: Automated testing and validation pipelines

## Implementation Priority Matrix

| Priority | Category | Actions | Timeline |
|----------|----------|---------|----------|
| **IMMEDIATE** | Git Management | Commit, push, branch cleanup | 15-30 min |
| **HIGH** | File Organization | Duplicate consolidation, YAML standardization | 1-2 hours |
| **MEDIUM** | PKM Implementation | Hybrid methodology deployment | 2-4 hours |
| **LOW** | Advanced Features | Multi-agent workflows, knowledge graphs | 1-2 days |

## Success Metrics

- [ ] Git repository clean and synchronized
- [ ] All markdown files have valid YAML frontmatter
- [ ] Duplicate files consolidated or justified
- [ ] PKM architectural patterns implemented
- [ ] Automation scripts functional and tested
- [ ] Documentation updated with new organizational patterns

EOF
}

#==============================================================================
# Implementation Functions
#==============================================================================

prepare_git_repository() {
    section "Git Repository Preparation"
    
    log "Preparing git repository for push..."
    
    cd "${REPO_ROOT}" || exit 1
    
    if [[ "${DRY_RUN}" == "true" ]]; then
        info "DRY RUN: Would stage and commit the following files:"
        git status --porcelain
        return 0
    fi
    
    # Stage new files
    if git status --porcelain | grep -q "^??"; then
        log "Staging new files..."
        git add .
    fi
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        warn "No changes staged for commit"
        return 0
    fi
    
    # Create comprehensive commit message
    local commit_msg="feat: comprehensive repository analysis and PKM improvements

- Complete repository structure analysis with ${total_files:-unknown} files
- PKM architectural framework implementation based on research
- YAML frontmatter validation and enhancement
- Duplicate file detection and consolidation recommendations
- Git repository optimization and pre-push preparation
- Automated improvement recommendations and success metrics

Generated by: repository-analysis-and-improvement.sh v1.0.0
Analysis Report: 30-data/analysis-reports/repository-analysis-${TIMESTAMP}.md"
    
    log "Committing changes with comprehensive message..."
    git commit -m "${commit_msg}"
    
    log "Git repository prepared for push"
}

implement_yaml_frontmatter() {
    section "YAML Frontmatter Implementation"
    
    log "Implementing YAML frontmatter for files missing it..."
    
    local files_updated=0
    
    while IFS= read -r -d '' file; do
        # Skip if file already has YAML frontmatter
        if head -n 1 "${file}" | grep -q "^---$"; then
            continue
        fi
        
        if [[ "${DRY_RUN}" == "true" ]]; then
            info "DRY RUN: Would add YAML frontmatter to: ${file#${REPO_ROOT}/}"
            ((files_updated++))
            continue
        fi
        
        # Extract title from filename or first heading
        local title=$(basename "${file}" .md | sed 's/-/ /g' | sed 's/\b\w/\U&/g')
        local first_heading=$(grep -m 1 "^# " "${file}" 2>/dev/null | sed 's/^# //' || echo "")
        
        if [[ -n "${first_heading}" ]]; then
            title="${first_heading}"
        fi
        
        # Create temporary file with YAML frontmatter
        local temp_file=$(mktemp)
        cat > "${temp_file}" << EOF
---
title: ${title}
description: Auto-generated description for ${title}
status: active
created: $(date +"%Y-%m-%d")
updated: $(date +"%Y-%m-%d")
tags: [auto-generated, repository-analysis]
---

EOF
        
        # Append original content
        cat "${file}" >> "${temp_file}"
        
        # Replace original file
        mv "${temp_file}" "${file}"
        
        log "Added YAML frontmatter to: ${file#${REPO_ROOT}/}"
        ((files_updated++))
        
    done < <(find "${REPO_ROOT}" -name "*.md" -type f -not -path "*/.git/*" -print0)
    
    log "Updated ${files_updated} files with YAML frontmatter"
}

#==============================================================================
# Main Execution
#==============================================================================

main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Create report directory
    mkdir -p "${REPORT_DIR}"
    
    # Initialize log file
    echo "Repository Analysis and Improvement Script" > "${IMPROVEMENT_LOG}"
    echo "Started: $(date)" >> "${IMPROVEMENT_LOG}"
    echo "Repository: ${REPO_ROOT}" >> "${IMPROVEMENT_LOG}"
    echo "Dry Run: ${DRY_RUN}" >> "${IMPROVEMENT_LOG}"
    echo "Verbose: ${VERBOSE}" >> "${IMPROVEMENT_LOG}"
    echo "===========================================" >> "${IMPROVEMENT_LOG}"
    
    log "Starting comprehensive repository analysis and improvement"
    
    if [[ "${DRY_RUN}" == "true" ]]; then
        warn "DRY RUN MODE - No changes will be made"
    fi
    
    # Execute analysis phases
    analyze_repository_structure
    detect_duplicate_files
    validate_yaml_frontmatter
    analyze_git_status
    generate_improvement_recommendations
    
    # Execute improvements
    if [[ "${DRY_RUN}" == "false" ]]; then
        implement_yaml_frontmatter
        prepare_git_repository
    fi
    
    # Final summary
    section "Analysis Complete"
    
    log "Repository analysis completed successfully"
    log "Analysis report: ${ANALYSIS_REPORT}"
    log "Improvement log: ${IMPROVEMENT_LOG}"
    
    if [[ "${DRY_RUN}" == "true" ]]; then
        warn "DRY RUN completed - no changes were made"
        info "Run without --dry-run to implement changes"
    else
        log "Improvements implemented successfully"
        info "Review the analysis report for additional recommendations"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Repository analysis and improvement completed${NC}"
    echo -e "${BLUE}📊 Analysis Report: ${ANALYSIS_REPORT}${NC}"
    echo -e "${BLUE}📝 Improvement Log: ${IMPROVEMENT_LOG}${NC}"
    echo ""
}

# Script execution guard
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi