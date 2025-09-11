#!/usr/bin/env python3
"""
Enhanced Knowledge Base Maintenance Tool

Provides comprehensive automation for knowledge base maintenance including:
- Automated content categorization
- Cross-reference validation and fixing
- Content quality assessment
- Lifecycle management
- Performance optimization

Usage:
    python3 maintain_kb_enhanced.py --scan
    python3 maintain_kb_enhanced.py --fix
    python3 maintain_kb_enhanced.py --optimize
"""

import os
import re
import yaml
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Optional

class KnowledgeBaseMaintainer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.issues = []
        self.stats = defaultdict(int)
        self.kb_policy = self._load_policy()
        
    def _load_policy(self) -> Dict:
        """Load knowledge base policy configuration"""
        policy_path = self.base_path / ".kb" / "policy" / "kb-policy.yaml"
        if policy_path.exists():
            with open(policy_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def scan_content(self) -> Dict:
        """Comprehensive content scanning and analysis"""
        print("🔍 Scanning knowledge base content...")
        
        results = {
            'structure_issues': self._check_structure(),
            'metadata_issues': self._check_metadata(),
            'content_quality': self._assess_content_quality(),
            'cross_references': self._validate_cross_references(),
            'lifecycle_status': self._check_lifecycle(),
            'performance_metrics': self._analyze_performance()
        }
        
        self._generate_scan_report(results)
        return results
    
    def _check_structure(self) -> List[Dict]:
        """Check directory structure compliance"""
        issues = []
        required_dirs = ['00-admin', '10-knowledge', '20-projects', '30-data', 
                        '40-code', '50-experiments', '60-manuscripts', 
                        '70-presentations', '80-resources', '90-archive']
        
        for req_dir in required_dirs:
            dir_path = self.base_path / req_dir
            if not dir_path.exists():
                issues.append({
                    'type': 'missing_directory',
                    'path': req_dir,
                    'severity': 'error',
                    'fix_suggestion': f'mkdir -p {req_dir}'
                })
        
        # Check for files in root that should be categorized
        for item in self.base_path.iterdir():
            if item.is_file() and item.suffix == '.md':
                if item.name not in ['README.md', 'TODO.md', 'TASKS.md', 
                                   'CHANGELOG.md', 'GOVERNANCE.md', 'CONTRIBUTING.md']:
                    issues.append({
                        'type': 'uncategorized_file',
                        'path': str(item),
                        'severity': 'warning',
                        'fix_suggestion': 'Move to appropriate academic category'
                    })
        
        return issues
    
    def _check_metadata(self) -> List[Dict]:
        """Validate YAML frontmatter across all markdown files"""
        issues = []
        md_files = list(self.base_path.rglob("*.md"))
        
        for md_file in md_files:
            if any(skip in str(md_file) for skip in ['.git', '.kb', '.venv']):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for frontmatter
                if not content.startswith('---'):
                    issues.append({
                        'type': 'missing_frontmatter',
                        'path': str(md_file),
                        'severity': 'warning',
                        'fix_suggestion': 'Add YAML frontmatter'
                    })
                    continue
                
                # Parse frontmatter
                try:
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end == -1:
                        raise ValueError("Malformed frontmatter")
                    
                    frontmatter = content[3:frontmatter_end].strip()
                    metadata = yaml.safe_load(frontmatter)
                    
                    # Validate required fields
                    required_fields = ['title', 'description', 'status', 'created', 'updated']
                    for field in required_fields:
                        if field not in metadata:
                            issues.append({
                                'type': 'missing_metadata_field',
                                'path': str(md_file),
                                'field': field,
                                'severity': 'warning',
                                'fix_suggestion': f'Add {field} to frontmatter'
                            })
                    
                    # Validate status values
                    valid_statuses = ['draft', 'active', 'completed', 'archived']
                    if 'status' in metadata and metadata['status'] not in valid_statuses:
                        issues.append({
                            'type': 'invalid_status',
                            'path': str(md_file),
                            'current_status': metadata['status'],
                            'severity': 'error',
                            'fix_suggestion': f'Use one of: {valid_statuses}'
                        })
                
                except yaml.YAMLError as e:
                    issues.append({
                        'type': 'yaml_parse_error',
                        'path': str(md_file),
                        'error': str(e),
                        'severity': 'error',
                        'fix_suggestion': 'Fix YAML syntax'
                    })
            
            except Exception as e:
                issues.append({
                    'type': 'file_read_error',
                    'path': str(md_file),
                    'error': str(e),
                    'severity': 'error'
                })
        
        return issues
    
    def _assess_content_quality(self) -> Dict:
        """Assess overall content quality metrics"""
        quality_metrics = {
            'total_files': 0,
            'files_with_metadata': 0,
            'avg_content_length': 0,
            'files_with_tags': 0,
            'files_with_links': 0,
            'outdated_files': 0,
            'draft_files': 0
        }
        
        md_files = list(self.base_path.rglob("*.md"))
        content_lengths = []
        cutoff_date = datetime.now() - timedelta(days=180)
        
        for md_file in md_files:
            if any(skip in str(md_file) for skip in ['.git', '.kb', '.venv']):
                continue
            
            quality_metrics['total_files'] += 1
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content_lengths.append(len(content))
                
                # Check for metadata
                if content.startswith('---'):
                    quality_metrics['files_with_metadata'] += 1
                    
                    # Parse metadata for additional checks
                    try:
                        frontmatter_end = content.find('---', 3)
                        if frontmatter_end != -1:
                            frontmatter = content[3:frontmatter_end].strip()
                            metadata = yaml.safe_load(frontmatter)
                            
                            if 'tags' in metadata and metadata['tags']:
                                quality_metrics['files_with_tags'] += 1
                            
                            if 'status' in metadata and metadata['status'] == 'draft':
                                quality_metrics['draft_files'] += 1
                            
                            if 'updated' in metadata:
                                updated_date = datetime.fromisoformat(str(metadata['updated']))
                                if updated_date < cutoff_date:
                                    quality_metrics['outdated_files'] += 1
                    except:
                        pass
                
                # Check for internal links
                if re.search(r'\[.*?\]\(.*?\.md\)', content):
                    quality_metrics['files_with_links'] += 1
            
            except Exception:
                continue
        
        if content_lengths:
            quality_metrics['avg_content_length'] = sum(content_lengths) // len(content_lengths)
        
        return quality_metrics
    
    def _validate_cross_references(self) -> List[Dict]:
        """Validate all cross-references and internal links"""
        issues = []
        md_files = list(self.base_path.rglob("*.md"))
        
        for md_file in md_files:
            if any(skip in str(md_file) for skip in ['.git', '.kb', '.venv']):
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find markdown links
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                
                for link_text, link_path in links:
                    # Skip external links
                    if link_path.startswith(('http://', 'https://', 'mailto:', '#')):
                        continue
                    
                    # Resolve relative path
                    if link_path.startswith('./'):
                        link_path = link_path[2:]
                    
                    full_link_path = md_file.parent / link_path
                    
                    if not full_link_path.exists():
                        issues.append({
                            'type': 'broken_link',
                            'source_file': str(md_file),
                            'link_text': link_text,
                            'link_path': link_path,
                            'severity': 'warning',
                            'fix_suggestion': 'Update link path or create target file'
                        })
            
            except Exception as e:
                issues.append({
                    'type': 'link_check_error',
                    'path': str(md_file),
                    'error': str(e),
                    'severity': 'error'
                })
        
        return issues
    
    def _check_lifecycle(self) -> Dict:
        """Check content lifecycle status and suggest actions"""
        lifecycle_stats = {
            'draft_files': [],
            'stale_files': [],
            'active_projects': [],
            'completed_projects': [],
            'archive_candidates': []
        }
        
        cutoff_date = datetime.now() - timedelta(days=365)
        stale_cutoff = datetime.now() - timedelta(days=90)
        
        md_files = list(self.base_path.rglob("*.md"))
        
        for md_file in md_files:
            if any(skip in str(md_file) for skip in ['.git', '.kb', '.venv']):
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.startswith('---'):
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end != -1:
                        frontmatter = content[3:frontmatter_end].strip()
                        metadata = yaml.safe_load(frontmatter)
                        
                        status = metadata.get('status', 'unknown')
                        updated = metadata.get('updated')
                        
                        if status == 'draft':
                            lifecycle_stats['draft_files'].append(str(md_file))
                        
                        if updated:
                            try:
                                updated_date = datetime.fromisoformat(str(updated))
                                if updated_date < stale_cutoff:
                                    lifecycle_stats['stale_files'].append(str(md_file))
                                if updated_date < cutoff_date and status == 'completed':
                                    lifecycle_stats['archive_candidates'].append(str(md_file))
                            except:
                                pass
                        
                        # Project-specific checks
                        if '20-projects/active' in str(md_file):
                            lifecycle_stats['active_projects'].append(str(md_file))
                        elif '20-projects/completed' in str(md_file):
                            lifecycle_stats['completed_projects'].append(str(md_file))
            
            except Exception:
                continue
        
        return lifecycle_stats
    
    def _analyze_performance(self) -> Dict:
        """Analyze performance metrics and optimization opportunities"""
        metrics = {
            'total_size_mb': 0,
            'largest_files': [],
            'deep_directories': [],
            'duplicate_names': [],
            'optimization_suggestions': []
        }
        
        # Calculate total size
        total_size = 0
        file_sizes = []
        file_names = Counter()
        
        for file_path in self.base_path.rglob("*"):
            if file_path.is_file() and not any(skip in str(file_path) for skip in ['.git', '.venv']):
                size = file_path.stat().st_size
                total_size += size
                
                if file_path.suffix == '.md':
                    file_sizes.append((size, str(file_path)))
                    file_names[file_path.name] += 1
        
        metrics['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        # Find largest files
        file_sizes.sort(reverse=True)
        metrics['largest_files'] = file_sizes[:10]
        
        # Find duplicate names
        metrics['duplicate_names'] = [(name, count) for name, count in file_names.items() if count > 1]
        
        # Find deep directories
        for dir_path in self.base_path.rglob("*"):
            if dir_path.is_dir():
                depth = len(dir_path.parts) - len(self.base_path.parts)
                if depth > 6:
                    metrics['deep_directories'].append((depth, str(dir_path)))
        
        # Generate optimization suggestions
        if metrics['total_size_mb'] > 100:
            metrics['optimization_suggestions'].append("Consider archiving old content")
        
        if len(metrics['duplicate_names']) > 5:
            metrics['optimization_suggestions'].append("Review duplicate filenames for confusion")
        
        if len(metrics['deep_directories']) > 0:
            metrics['optimization_suggestions'].append("Consider flattening deep directory structures")
        
        return metrics
    
    def _generate_scan_report(self, results: Dict):
        """Generate comprehensive scan report"""
        report_path = self.base_path / "00-admin" / f"maintenance-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        
        with open(report_path, 'w') as f:
            f.write(f"""---
title: Knowledge Base Maintenance Report
description: Automated maintenance scan results
status: active
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
tags: [maintenance, automation, report, scan]
version: 1.0.0
---

# Knowledge Base Maintenance Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Issues Found**: {len(results['structure_issues']) + len(results['metadata_issues']) + len(results['cross_references'])}
- **Structure Issues**: {len(results['structure_issues'])}
- **Metadata Issues**: {len(results['metadata_issues'])}
- **Broken Links**: {len(results['cross_references'])}
- **Total Files**: {results['content_quality']['total_files']}
- **Files with Metadata**: {results['content_quality']['files_with_metadata']}

## Content Quality Metrics

- **Average Content Length**: {results['content_quality']['avg_content_length']} characters
- **Files with Tags**: {results['content_quality']['files_with_tags']}
- **Files with Links**: {results['content_quality']['files_with_links']}
- **Outdated Files**: {results['content_quality']['outdated_files']}
- **Draft Files**: {results['content_quality']['draft_files']}

## Performance Metrics

- **Total Size**: {results['performance_metrics']['total_size_mb']} MB
- **Duplicate Names**: {len(results['performance_metrics']['duplicate_names'])}
- **Deep Directories**: {len(results['performance_metrics']['deep_directories'])}

## Issues Found

### Structure Issues
""")
            
            for issue in results['structure_issues']:
                f.write(f"- **{issue['type']}**: {issue['path']} ({issue['severity']})\n")
                if 'fix_suggestion' in issue:
                    f.write(f"  - Fix: {issue['fix_suggestion']}\n")
            
            f.write("\n### Metadata Issues\n")
            for issue in results['metadata_issues']:
                f.write(f"- **{issue['type']}**: {issue['path']} ({issue['severity']})\n")
                if 'fix_suggestion' in issue:
                    f.write(f"  - Fix: {issue['fix_suggestion']}\n")
            
            f.write("\n### Cross-Reference Issues\n")
            for issue in results['cross_references']:
                f.write(f"- **{issue['type']}**: {issue['source_file']} → {issue['link_path']} ({issue['severity']})\n")
                if 'fix_suggestion' in issue:
                    f.write(f"  - Fix: {issue['fix_suggestion']}\n")
            
            f.write(f"\n## Lifecycle Management\n")
            f.write(f"- **Draft Files**: {len(results['lifecycle_status']['draft_files'])}\n")
            f.write(f"- **Stale Files**: {len(results['lifecycle_status']['stale_files'])}\n")
            f.write(f"- **Archive Candidates**: {len(results['lifecycle_status']['archive_candidates'])}\n")
            
            f.write(f"\n## Optimization Suggestions\n")
            for suggestion in results['performance_metrics']['optimization_suggestions']:
                f.write(f"- {suggestion}\n")
            
            f.write(f"\n## Next Steps\n")
            f.write("1. Run `python3 maintain_kb_enhanced.py --fix` to auto-fix common issues\n")
            f.write("2. Review and address manual fixes needed\n")
            f.write("3. Consider archiving old content to improve performance\n")
            f.write("4. Update outdated metadata and content\n")
        
        print(f"📊 Maintenance report generated: {report_path}")
    
    def auto_fix(self) -> Dict:
        """Automatically fix common issues"""
        print("🔧 Running automatic fixes...")
        
        fixes_applied = {
            'frontmatter_added': 0,
            'metadata_updated': 0,
            'files_moved': 0,
            'links_fixed': 0
        }
        
        # Add missing frontmatter
        md_files = list(self.base_path.rglob("*.md"))
        
        for md_file in md_files:
            if any(skip in str(md_file) for skip in ['.git', '.kb', '.venv']):
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.startswith('---'):
                    # Add basic frontmatter
                    title = md_file.stem.replace('-', ' ').replace('_', ' ').title()
                    created_date = datetime.fromtimestamp(md_file.stat().st_ctime).strftime('%Y-%m-%d')
                    updated_date = datetime.fromtimestamp(md_file.stat().st_mtime).strftime('%Y-%m-%d')
                    
                    frontmatter = f"""---
title: {title}
description: Auto-generated description
status: draft
created: {created_date}
updated: {updated_date}
tags: [auto-generated]
version: 1.0.0
---

"""
                    
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(frontmatter + content)
                    
                    fixes_applied['frontmatter_added'] += 1
                    print(f"Added frontmatter to {md_file}")
            
            except Exception as e:
                print(f"Error fixing {md_file}: {e}")
        
        print(f"🎯 Auto-fix completed: {fixes_applied}")
        return fixes_applied
    
    def optimize(self) -> Dict:
        """Optimize knowledge base performance and organization"""
        print("⚡ Optimizing knowledge base...")
        
        optimizations = {
            'archived_files': 0,
            'reorganized_files': 0,
            'indexes_updated': 0,
            'duplicates_resolved': 0
        }
        
        # Archive old completed projects
        completed_dir = self.base_path / "20-projects" / "completed"
        archive_dir = self.base_path / "90-archive" / "old-projects"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        cutoff_date = datetime.now() - timedelta(days=365)
        
        if completed_dir.exists():
            for project_file in completed_dir.rglob("*.md"):
                if project_file.stat().st_mtime < cutoff_date.timestamp():
                    try:
                        new_path = archive_dir / project_file.name
                        project_file.rename(new_path)
                        optimizations['archived_files'] += 1
                        print(f"Archived {project_file} to {new_path}")
                    except Exception as e:
                        print(f"Error archiving {project_file}: {e}")
        
        # Update search indexes
        self._update_search_indexes()
        optimizations['indexes_updated'] = 1
        
        print(f"⚡ Optimization completed: {optimizations}")
        return optimizations
    
    def _update_search_indexes(self):
        """Update search indexes for better performance"""
        indexes_dir = self.base_path / "30-data" / "indexes"
        indexes_dir.mkdir(parents=True, exist_ok=True)
        
        # Create tag index
        tag_counter = Counter()
        category_counter = Counter()
        
        md_files = list(self.base_path.rglob("*.md"))
        
        for md_file in md_files:
            if any(skip in str(md_file) for skip in ['.git', '.kb', '.venv']):
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.startswith('---'):
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end != -1:
                        frontmatter = content[3:frontmatter_end].strip()
                        metadata = yaml.safe_load(frontmatter)
                        
                        if 'tags' in metadata and metadata['tags']:
                            for tag in metadata['tags']:
                                tag_counter[tag] += 1
                        
                        # Determine category from path
                        path_parts = md_file.parts
                        if len(path_parts) > 1:
                            category_counter[path_parts[1]] += 1
            
            except Exception:
                continue
        
        # Write tag index
        with open(indexes_dir / "tags.json", 'w') as f:
            json.dump(dict(tag_counter), f, indent=2)
        
        # Write category index
        with open(indexes_dir / "categories.json", 'w') as f:
            json.dump(dict(category_counter), f, indent=2)
        
        print(f"📊 Updated search indexes with {len(tag_counter)} tags and {len(category_counter)} categories")

def main():
    parser = argparse.ArgumentParser(description="Enhanced Knowledge Base Maintenance Tool")
    parser.add_argument("--scan", action="store_true", help="Scan for issues and generate report")
    parser.add_argument("--fix", action="store_true", help="Automatically fix common issues")
    parser.add_argument("--optimize", action="store_true", help="Optimize performance and organization")
    parser.add_argument("--all", action="store_true", help="Run scan, fix, and optimize")
    parser.add_argument("--path", default=".", help="Path to knowledge base root")
    
    args = parser.parse_args()
    
    if not any([args.scan, args.fix, args.optimize, args.all]):
        parser.print_help()
        return
    
    maintainer = KnowledgeBaseMaintainer(args.path)
    
    if args.scan or args.all:
        maintainer.scan_content()
    
    if args.fix or args.all:
        maintainer.auto_fix()
    
    if args.optimize or args.all:
        maintainer.optimize()
    
    print("✅ Knowledge base maintenance completed!")

if __name__ == "__main__":
    main()