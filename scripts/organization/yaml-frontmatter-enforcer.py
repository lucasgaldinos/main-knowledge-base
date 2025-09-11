#!/usr/bin/env python3
"""
YAML Frontmatter Enforcer
=========================

Automatically enforces YAML frontmatter compliance across all markdown files
in the academic knowledge base with intelligent content analysis and metadata
generation.

Features:
- Scans all .md files for YAML frontmatter
- Generates missing frontmatter with intelligent defaults
- Validates existing frontmatter against academic standards
- Integrates with database for metadata tracking
- Supports batch processing and validation

Usage:
    python3 yaml-frontmatter-enforcer.py [--validate-only] [--fix] [--path PATH]
"""

import os
import sys
import re
import yaml
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import sqlite3

# Add parent directory to path for database imports
sys.path.append(str(Path(__file__).parent.parent))

class YAMLFrontmatterEnforcer:
    """Enforces YAML frontmatter standards across the knowledge base."""
    
    def __init__(self, base_path: str, db_path: str = None):
        self.base_path = Path(base_path)
        self.db_path = db_path or self.base_path / "database" / "knowledge.db"
        self.violations = []
        self.fixes_applied = []
        
        # Required fields for different content types
        self.required_fields = {
            'basic': ['title', 'description', 'status', 'created', 'updated', 'tags'],
            'academic': ['title', 'description', 'status', 'created', 'updated', 'tags', 'authors', 'citations'],
            'technical': ['title', 'description', 'status', 'created', 'updated', 'tags', 'version'],
            'project': ['title', 'description', 'status', 'created', 'updated', 'tags', 'project_type', 'methodology']
        }
        
        # Valid values for controlled fields
        self.valid_values = {
            'status': ['draft', 'in-review', 'published', 'deprecated', 'archived'],
            'confidence_level': ['high', 'medium', 'low'],
            'project_status': ['active', 'completed', 'on-hold', 'archived']
        }
    
    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract YAML frontmatter from markdown content."""
        if not content.startswith('---'):
            return None, content
        
        try:
            # Find the end of frontmatter
            end_marker = content.find('\n---\n', 3)
            if end_marker == -1:
                return None, content
            
            yaml_content = content[3:end_marker]
            body_content = content[end_marker + 5:]
            
            frontmatter = yaml.safe_load(yaml_content)
            return frontmatter, body_content
            
        except yaml.YAMLError as e:
            self.violations.append(f"Invalid YAML frontmatter: {e}")
            return None, content
    
    def determine_content_type(self, file_path: Path, content: str) -> str:
        """Determine content type based on file path and content analysis."""
        path_str = str(file_path).lower()
        
        # Academic content indicators
        if any(keyword in path_str for keyword in ['research', 'literature', 'citation', 'academic']):
            return 'academic'
        
        # Technical documentation
        if any(keyword in path_str for keyword in ['tools', 'reference', 'api', 'technical']):
            return 'technical'
        
        # Project documentation
        if any(keyword in path_str for keyword in ['projects', 'workflow', 'methodology']):
            return 'project'
        
        # Content analysis for type detection
        content_lower = content.lower()
        
        # Look for academic indicators
        academic_indicators = ['citation', 'doi:', 'arxiv:', 'journal:', 'peer review', 'methodology']
        if any(indicator in content_lower for indicator in academic_indicators):
            return 'academic'
        
        # Look for technical indicators
        technical_indicators = ['api', 'function', 'parameter', 'usage example', 'tool name']
        if any(indicator in content_lower for indicator in technical_indicators):
            return 'technical'
        
        # Look for project indicators
        project_indicators = ['phase', 'milestone', 'workflow', 'completion', 'implementation']
        if any(indicator in content_lower for indicator in project_indicators):
            return 'project'
        
        return 'basic'
    
    def generate_intelligent_metadata(self, file_path: Path, content: str, content_type: str) -> Dict:
        """Generate intelligent metadata based on content analysis."""
        metadata = {}
        
        # Extract title from first heading or filename
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        else:
            # Generate from filename
            metadata['title'] = file_path.stem.replace('-', ' ').replace('_', ' ').title()
        
        # Generate description from first paragraph or summary
        desc_patterns = [
            r'(?:^|\n)(?:## )?(?:Description|Summary|Overview)[:\s]*\n(.+?)(?:\n\n|\n#|$)',
            r'(?:^|\n)(.+?)(?:\n\n|\n#|$)'  # First paragraph
        ]
        
        for pattern in desc_patterns:
            desc_match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
            if desc_match:
                desc = desc_match.group(1).strip()
                # Clean up description
                desc = re.sub(r'\n+', ' ', desc)
                desc = re.sub(r'\s+', ' ', desc)
                if len(desc) > 200:
                    desc = desc[:197] + '...'
                metadata['description'] = desc
                break
        
        if 'description' not in metadata:
            metadata['description'] = f"Documentation for {metadata['title']}"
        
        # Set status based on content indicators
        if any(indicator in content.lower() for indicator in ['work in progress', 'draft', 'todo']):
            metadata['status'] = 'draft'
        elif any(indicator in content.lower() for indicator in ['complete', 'final', 'published']):
            metadata['status'] = 'published'
        else:
            metadata['status'] = 'draft'  # Conservative default
        
        # Set timestamps
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        metadata['created'] = current_time
        metadata['updated'] = current_time
        
        # Generate tags based on content and path
        tags = set()
        
        # Tags from file path
        path_parts = file_path.parts
        for part in path_parts:
            if part not in ['.', '..', 'docs', 'md']:
                tags.add(part.replace('-', ' ').replace('_', ' '))
        
        # Tags from content analysis
        content_lower = content.lower()
        tag_indicators = {
            'ai': ['artificial intelligence', 'machine learning', 'ai', 'ml'],
            'research': ['research', 'study', 'analysis', 'methodology'],
            'tools': ['tool', 'software', 'application', 'utility'],
            'documentation': ['guide', 'manual', 'reference', 'documentation'],
            'academic': ['academic', 'scholarly', 'peer-reviewed', 'journal'],
            'technical': ['technical', 'api', 'programming', 'development']
        }
        
        for tag, indicators in tag_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                tags.add(tag)
        
        metadata['tags'] = sorted(list(tags))[:5]  # Limit to 5 most relevant tags
        
        # Content-type specific metadata
        if content_type == 'academic':
            metadata['authors'] = ['lucas_galdino']  # Default author
            metadata['citations'] = []
            metadata['confidence_level'] = 'medium'
            
            # Extract citations from content
            citation_patterns = [
                r'\[([^\]]+)\]\([^)]*(?:doi|arxiv|journal)[^)]*\)',
                r'(?:doi:|DOI:)\s*([^\s]+)',
                r'(?:arxiv:|arXiv:)\s*([^\s]+)'
            ]
            
            citations = []
            for pattern in citation_patterns:
                citations.extend(re.findall(pattern, content, re.IGNORECASE))
            
            if citations:
                metadata['citations'] = citations[:10]  # Limit citations
        
        elif content_type == 'technical':
            metadata['version'] = '1.0.0'
            
            # Extract version from content if available
            version_match = re.search(r'version[:\s]+([0-9]+\.[0-9]+\.[0-9]+)', content, re.IGNORECASE)
            if version_match:
                metadata['version'] = version_match.group(1)
        
        elif content_type == 'project':
            metadata['project_type'] = 'research'
            metadata['methodology'] = 'systematic-content-recreation'
            
            # Determine project type from content
            if 'implementation' in content.lower():
                metadata['project_type'] = 'implementation'
            elif 'analysis' in content.lower():
                metadata['project_type'] = 'analysis'
            elif 'completion' in content.lower():
                metadata['project_type'] = 'completion-report'
        
        return metadata
    
    def validate_frontmatter(self, frontmatter: Dict, content_type: str, file_path: Path) -> List[str]:
        """Validate frontmatter against academic standards."""
        violations = []
        required = self.required_fields[content_type]
        
        # Check required fields
        for field in required:
            if field not in frontmatter:
                violations.append(f"Missing required field: {field}")
        
        # Validate field values
        for field, valid_values in self.valid_values.items():
            if field in frontmatter and frontmatter[field] not in valid_values:
                violations.append(f"Invalid value for {field}: {frontmatter[field]}. Valid values: {valid_values}")
        
        # Validate date formats
        date_fields = ['created', 'updated']
        for field in date_fields:
            if field in frontmatter:
                try:
                    datetime.strptime(frontmatter[field], '%Y-%m-%d')
                except ValueError:
                    violations.append(f"Invalid date format for {field}: {frontmatter[field]}. Expected: YYYY-MM-DD")
        
        # Validate tags
        if 'tags' in frontmatter:
            if not isinstance(frontmatter['tags'], list):
                violations.append("Tags must be a list")
            elif len(frontmatter['tags']) > 10:
                violations.append("Too many tags (max 10)")
        
        return violations
    
    def fix_frontmatter(self, file_path: Path, content: str, dry_run: bool = False) -> bool:
        """Fix or add frontmatter to a file."""
        frontmatter, body = self.extract_frontmatter(content)
        content_type = self.determine_content_type(file_path, body)
        
        if frontmatter is None:
            # No frontmatter - generate from scratch
            frontmatter = self.generate_intelligent_metadata(file_path, body, content_type)
            action = "Added"
        else:
            # Existing frontmatter - validate and fix
            violations = self.validate_frontmatter(frontmatter, content_type, file_path)
            if not violations:
                return False  # No fixes needed
            
            # Generate missing fields
            generated = self.generate_intelligent_metadata(file_path, body, content_type)
            required = self.required_fields[content_type]
            
            for field in required:
                if field not in frontmatter:
                    frontmatter[field] = generated[field]
            
            # Update timestamp
            frontmatter['updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            action = "Fixed"
        
        if not dry_run:
            # Write the fixed content
            yaml_content = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
            new_content = f"---\n{yaml_content}---\n\n{body}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Log to database
            self.log_to_database(file_path, frontmatter, content_type)
        
        self.fixes_applied.append(f"{action} frontmatter for {file_path}")
        return True
    
    def log_to_database(self, file_path: Path, frontmatter: Dict, content_type: str):
        """Log frontmatter changes to the knowledge database."""
        if not self.db_path.exists():
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert or update research content record
            cursor.execute("""
                INSERT OR REPLACE INTO research_content 
                (title, content, methodology, confidence_level, status, created_date, updated_date, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                frontmatter.get('title', ''),
                frontmatter.get('description', ''),
                frontmatter.get('methodology', content_type),
                frontmatter.get('confidence_level', 'medium'),
                frontmatter.get('status', 'draft'),
                frontmatter.get('created', datetime.now().strftime('%Y-%m-%d')),
                frontmatter.get('updated', datetime.now().strftime('%Y-%m-%d')),
                str(file_path.relative_to(self.base_path))
            ))
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Database logging error: {e}")
    
    def scan_directory(self, directory: Path = None) -> List[Path]:
        """Scan directory for markdown files."""
        scan_dir = directory or self.base_path
        markdown_files = []
        
        for file_path in scan_dir.rglob("*.md"):
            # Skip certain directories
            skip_dirs = ['.git', 'node_modules', '.vscode', 'cache']
            if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                continue
            
            markdown_files.append(file_path)
        
        return markdown_files
    
    def run_validation(self, file_paths: List[Path] = None) -> Dict:
        """Run validation on specified files or all markdown files."""
        files_to_check = file_paths or self.scan_directory()
        
        results = {
            'total_files': len(files_to_check),
            'compliant_files': 0,
            'violation_files': 0,
            'missing_frontmatter': 0,
            'violations': []
        }
        
        for file_path in files_to_check:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                frontmatter, body = self.extract_frontmatter(content)
                
                if frontmatter is None:
                    results['missing_frontmatter'] += 1
                    results['violations'].append(f"{file_path}: Missing frontmatter")
                else:
                    content_type = self.determine_content_type(file_path, body)
                    violations = self.validate_frontmatter(frontmatter, content_type, file_path)
                    
                    if violations:
                        results['violation_files'] += 1
                        for violation in violations:
                            results['violations'].append(f"{file_path}: {violation}")
                    else:
                        results['compliant_files'] += 1
                        
            except Exception as e:
                results['violations'].append(f"{file_path}: Error reading file - {e}")
        
        return results
    
    def run_fixes(self, file_paths: List[Path] = None, dry_run: bool = False) -> Dict:
        """Run fixes on specified files or all markdown files."""
        files_to_fix = file_paths or self.scan_directory()
        
        results = {
            'total_files': len(files_to_fix),
            'files_fixed': 0,
            'files_skipped': 0,
            'errors': []
        }
        
        for file_path in files_to_fix:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if self.fix_frontmatter(file_path, content, dry_run):
                    results['files_fixed'] += 1
                else:
                    results['files_skipped'] += 1
                    
            except Exception as e:
                results['errors'].append(f"{file_path}: {e}")
        
        return results

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="YAML Frontmatter Enforcer for Academic Knowledge Base")
    parser.add_argument('--validate-only', action='store_true', help='Only validate, do not fix')
    parser.add_argument('--fix', action='store_true', help='Fix violations automatically')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without making changes')
    parser.add_argument('--path', type=str, help='Specific path to process (default: current directory)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Determine base path
    if args.path:
        base_path = Path(args.path).resolve()
    else:
        # Try to find the knowledge base root
        current = Path.cwd()
        while current.parent != current:
            if (current / 'GOVERNANCE.md').exists() or (current / 'database').exists():
                base_path = current
                break
            current = current.parent
        else:
            base_path = Path.cwd()
    
    print(f"🔧 YAML Frontmatter Enforcer")
    print(f"📁 Base path: {base_path}")
    print("=" * 50)
    
    enforcer = YAMLFrontmatterEnforcer(base_path)
    
    if args.validate_only or not args.fix:
        # Run validation
        print("🔍 Validating frontmatter compliance...")
        results = enforcer.run_validation()
        
        print(f"📊 Validation Results:")
        print(f"   Total files: {results['total_files']}")
        print(f"   Compliant files: {results['compliant_files']}")
        print(f"   Files with violations: {results['violation_files']}")
        print(f"   Files missing frontmatter: {results['missing_frontmatter']}")
        
        if args.verbose and results['violations']:
            print(f"\n❌ Violations found:")
            for violation in results['violations']:
                print(f"   {violation}")
        
        if results['violation_files'] > 0 or results['missing_frontmatter'] > 0:
            print(f"\n💡 Run with --fix to automatically resolve issues")
            sys.exit(1)
        else:
            print(f"\n✅ All files are compliant!")
            sys.exit(0)
    
    if args.fix:
        # Run fixes
        print("🔧 Fixing frontmatter issues...")
        results = enforcer.run_fixes(dry_run=args.dry_run)
        
        print(f"📊 Fix Results:")
        print(f"   Total files processed: {results['total_files']}")
        print(f"   Files fixed: {results['files_fixed']}")
        print(f"   Files skipped (no issues): {results['files_skipped']}")
        
        if results['errors']:
            print(f"   Errors: {len(results['errors'])}")
            if args.verbose:
                for error in results['errors']:
                    print(f"   ❌ {error}")
        
        if args.verbose and enforcer.fixes_applied:
            print(f"\n✅ Fixes applied:")
            for fix in enforcer.fixes_applied:
                print(f"   {fix}")
        
        if args.dry_run:
            print(f"\n💡 This was a dry run. Use --fix without --dry-run to apply changes.")
        else:
            print(f"\n✅ Frontmatter enforcement complete!")

if __name__ == "__main__":
    main()
