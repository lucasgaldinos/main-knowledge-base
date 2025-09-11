#!/usr/bin/env python3
"""
Knowledge Base Organization Maintenance Script

Maintains the academic directory structure and validates content organization
according to the established governance framework.

Usage:
    maintain_organization.py [options]

Examples:
    maintain_organization.py --verbose
    maintain_organization.py --dry-run --check-structure
    maintain_organization.py --validate-all
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Dict, Optional, Set
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
)
logger = logging.getLogger('maintain-organization')

class AcademicStructureValidator:
    """Validates and maintains academic directory structure."""
    
    def __init__(self, base_path: Path, dry_run: bool = False):
        self.base_path = base_path
        self.dry_run = dry_run
        self.issues_found = []
        
        # Academic directory structure
        self.required_dirs = {
            'knowledge': {
                'foundations': 'Core concepts and foundational knowledge',
                'methods': 'Methodologies, processes, and implementation guides',
                'applications': 'Applied knowledge, use cases, and examples',
                'synthesis': 'Research synthesis and meta-analysis'
            },
            'projects': {
                'active': 'Currently active projects',
                'completed': 'Finished projects with completion reports',
                'archived': 'Archived or deprecated projects'
            },
            'resources': {
                'literature': 'Research papers, articles, and academic references',
                'tools': 'Tool documentation and guides',
                'data': 'Datasets and data sources'
            },
            'infrastructure': {
                'scripts': 'Automation scripts and maintenance tools'
            },
            'outputs': {
                'artifacts': 'Generated content and build artifacts',
                'publications': 'Published content and releases'
            },
            'database': 'SQLite databases for persistent storage'
        }
        
        # Files that should have README.md
        self.readme_dirs = [
            'knowledge', 'knowledge/foundations', 'knowledge/methods',
            'knowledge/applications', 'knowledge/synthesis',
            'projects', 'projects/active', 'projects/completed', 'projects/archived',
            'resources', 'resources/literature', 'resources/tools', 'resources/data',
            'infrastructure', 'outputs'
        ]
        
        # Root-level files that should exist
        self.required_root_files = [
            'README.md', 'GOVERNANCE.md', 'CITATION.cff', 'CHANGELOG.md'
        ]

    def check_directory_structure(self) -> bool:
        """Check and create missing directories."""
        logger.info("📁 Checking academic directory structure...")
        structure_valid = True
        
        for main_dir, subdirs in self.required_dirs.items():
            main_path = self.base_path / main_dir
            
            if not main_path.exists():
                logger.error(f"❌ Missing directory: {main_dir}")
                self.issues_found.append(f"Missing directory: {main_dir}")
                if not self.dry_run:
                    main_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"✅ Created: {main_dir}")
                structure_valid = False
            else:
                logger.info(f"✅ Found: {main_dir}")
            
            # Check subdirectories if they're defined as dict
            if isinstance(subdirs, dict):
                for subdir, description in subdirs.items():
                    sub_path = main_path / subdir
                    if not sub_path.exists():
                        logger.warning(f"⚠️  Missing subdirectory: {main_dir}/{subdir}")
                        self.issues_found.append(f"Missing subdirectory: {main_dir}/{subdir}")
                        if not self.dry_run:
                            sub_path.mkdir(parents=True, exist_ok=True)
                            logger.info(f"✅ Created: {main_dir}/{subdir}")
                        structure_valid = False
                    else:
                        logger.debug(f"✅ Found: {main_dir}/{subdir}")
        
        return structure_valid

    def check_readme_files(self) -> bool:
        """Check for README.md files in required directories."""
        logger.info("📝 Checking README files...")
        readmes_valid = True
        
        for dir_path in self.readme_dirs:
            readme_path = self.base_path / dir_path / 'README.md'
            if not readme_path.exists():
                logger.warning(f"⚠️  Missing README.md in: {dir_path}")
                self.issues_found.append(f"Missing README.md in: {dir_path}")
                readmes_valid = False
            else:
                logger.debug(f"✅ Found README.md in: {dir_path}")
        
        return readmes_valid

    def check_root_files(self) -> bool:
        """Check for required root-level files."""
        logger.info("📄 Checking root-level files...")
        root_files_valid = True
        
        for filename in self.required_root_files:
            file_path = self.base_path / filename
            if not file_path.exists():
                logger.error(f"❌ Missing root file: {filename}")
                self.issues_found.append(f"Missing root file: {filename}")
                root_files_valid = False
            else:
                logger.info(f"✅ Found root file: {filename}")
        
        return root_files_valid

    def find_misplaced_files(self) -> List[Path]:
        """Find files that might be in wrong locations."""
        logger.info("🔍 Looking for potentially misplaced files...")
        misplaced_files = []
        
        # Check for markdown files in root that should be organized
        root_md_files = [
            f for f in self.base_path.glob("*.md")
            if f.name not in self.required_root_files + ['CONTRIBUTING.md']
        ]
        
        if root_md_files:
            logger.warning("📄 Found files that could be organized:")
            for file_path in root_md_files:
                logger.warning(f"  - {file_path.name}")
                misplaced_files.append(file_path)
                self.issues_found.append(f"Potentially misplaced file: {file_path.name}")
            logger.info("💡 Consider moving these to appropriate knowledge/ subdirectories")
        else:
            logger.info("✅ No misplaced files found in root")
        
        return misplaced_files

    def find_empty_files(self) -> List[Path]:
        """Find empty or nearly empty markdown files that need content."""
        logger.info("📝 Detecting empty markdown files...")
        empty_files = []
        small_files = []
        
        markdown_files = list(self.base_path.glob("**/*.md"))
        
        for md_file in markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8').strip()
                content_size = len(content)
                
                # Count lines excluding YAML frontmatter
                lines = content.split('\n')
                content_lines = []
                in_frontmatter = False
                frontmatter_count = 0
                
                for line in lines:
                    if line.strip() == '---':
                        frontmatter_count += 1
                        in_frontmatter = frontmatter_count == 1
                        continue
                    if not in_frontmatter and line.strip():
                        content_lines.append(line.strip())
                
                actual_content = '\n'.join(content_lines).strip()
                
                if content_size == 0:
                    empty_files.append(md_file)
                    logger.error(f"❌ Empty file: {md_file.relative_to(self.base_path)}")
                    self.issues_found.append(f"Empty file: {md_file.relative_to(self.base_path)}")
                elif len(actual_content) < 50:  # Less than 50 characters of actual content
                    small_files.append((md_file, len(actual_content)))
                    logger.warning(f"⚠️  Minimal content file ({len(actual_content)} chars): {md_file.relative_to(self.base_path)}")
                    self.issues_found.append(f"Minimal content file: {md_file.relative_to(self.base_path)}")
                    
            except Exception as e:
                logger.warning(f"Could not read {md_file}: {e}")
        
        if empty_files:
            logger.warning(f"Found {len(empty_files)} completely empty files")
        if small_files:
            logger.warning(f"Found {len(small_files)} files with minimal content")
        
        if not empty_files and not small_files:
            logger.info("✅ No empty or minimal content files found")
        
        return empty_files + [f[0] for f in small_files]

    def validate_yaml_frontmatter(self) -> bool:
        """Enhanced validation of YAML frontmatter with content analysis."""
        logger.info("🏷️  Validating YAML frontmatter...")
        
        markdown_files = list(self.base_path.glob("**/*.md"))
        files_without_frontmatter = []
        files_with_invalid_frontmatter = []
        files_with_incomplete_frontmatter = []
        
        required_fields = ['title', 'description', 'status', 'created', 'updated', 'tags']
        
        for md_file in markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                
                if not content.startswith('---'):
                    files_without_frontmatter.append(md_file)
                    continue
                
                # Extract frontmatter
                try:
                    parts = content.split('---', 2)
                    if len(parts) < 3:
                        files_with_invalid_frontmatter.append(md_file)
                        continue
                    
                    frontmatter_text = parts[1].strip()
                    
                    # Check for required fields
                    missing_fields = []
                    for field in required_fields:
                        if f"{field}:" not in frontmatter_text:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        files_with_incomplete_frontmatter.append((md_file, missing_fields))
                        
                except Exception:
                    files_with_invalid_frontmatter.append(md_file)
                    
            except Exception as e:
                logger.warning(f"Could not read {md_file}: {e}")
        
        # Report findings
        frontmatter_valid = True
        
        if files_without_frontmatter:
            logger.warning(f"⚠️  Found {len(files_without_frontmatter)} files without YAML frontmatter")
            for file_path in files_without_frontmatter[:5]:
                logger.warning(f"  - {file_path.relative_to(self.base_path)}")
            if len(files_without_frontmatter) > 5:
                logger.warning(f"  ... and {len(files_without_frontmatter) - 5} more")
            frontmatter_valid = False
        
        if files_with_invalid_frontmatter:
            logger.warning(f"⚠️  Found {len(files_with_invalid_frontmatter)} files with invalid YAML frontmatter")
            for file_path in files_with_invalid_frontmatter[:3]:
                logger.warning(f"  - {file_path.relative_to(self.base_path)}")
            frontmatter_valid = False
        
        if files_with_incomplete_frontmatter:
            logger.warning(f"⚠️  Found {len(files_with_incomplete_frontmatter)} files with incomplete frontmatter")
            for file_path, missing in files_with_incomplete_frontmatter[:3]:
                logger.warning(f"  - {file_path.relative_to(self.base_path)} missing: {', '.join(missing)}")
            frontmatter_valid = False
        
        if frontmatter_valid:
            logger.info("✅ All markdown files have valid YAML frontmatter")
        else:
            logger.info("💡 Run yaml-frontmatter-enforcer.py to fix these issues")
            self.issues_found.extend([f"Frontmatter issue in: {f.relative_to(self.base_path)}" for f in files_without_frontmatter])
            self.issues_found.extend([f"Invalid frontmatter in: {f.relative_to(self.base_path)}" for f in files_with_invalid_frontmatter])
            self.issues_found.extend([f"Incomplete frontmatter in: {f[0].relative_to(self.base_path)}" for f in files_with_incomplete_frontmatter])
        
        return frontmatter_valid

    def check_git_integrity(self) -> bool:
        """Check git repository integrity and common issues."""
        logger.info("� Checking git repository integrity...")
        
        git_dir = self.base_path / '.git'
        if not git_dir.exists():
            logger.warning("⚠️  Not a git repository")
            self.issues_found.append("Not a git repository")
            return False
        
        issues_found = []
        
        # Check for large files
        try:
            import subprocess
            result = subprocess.run(['git', 'ls-files'], 
                                  cwd=self.base_path, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            
            if result.returncode == 0:
                large_files = []
                for file_line in result.stdout.strip().split('\n'):
                    if file_line:
                        file_path = self.base_path / file_line
                        if file_path.exists() and file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
                            large_files.append((file_line, file_path.stat().st_size // (1024 * 1024)))
                
                if large_files:
                    logger.warning(f"⚠️  Found {len(large_files)} large files in git:")
                    for file_name, size_mb in large_files[:3]:
                        logger.warning(f"  - {file_name} ({size_mb}MB)")
                    issues_found.append(f"Large files in git: {len(large_files)} files")
                
                # Check git status
                status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                             cwd=self.base_path, 
                                             capture_output=True, 
                                             text=True, 
                                             timeout=30)
                
                if status_result.returncode == 0:
                    untracked_files = [line for line in status_result.stdout.strip().split('\n') 
                                     if line.startswith('??')]
                    modified_files = [line for line in status_result.stdout.strip().split('\n') 
                                    if line.startswith(' M') or line.startswith('M ')]
                    
                    if untracked_files:
                        logger.info(f"📁 Found {len(untracked_files)} untracked files")
                    if modified_files:
                        logger.info(f"📝 Found {len(modified_files)} modified files")
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.warning(f"Could not check git status: {e}")
            issues_found.append("Git status check failed")
        
        if issues_found:
            self.issues_found.extend(issues_found)
            return False
        else:
            logger.info("✅ Git repository integrity looks good")
            return True

    def check_vscode_configuration(self) -> bool:
        """Validate VS Code workspace configuration."""
        logger.info("🔧 Checking VS Code configuration...")
        
        vscode_dir = self.base_path / '.vscode'
        if not vscode_dir.exists():
            logger.warning("⚠️  No .vscode configuration directory found")
            self.issues_found.append("Missing .vscode configuration")
            return False
        
        # Check for important configuration files
        config_files = {
            'settings.json': 'Workspace settings',
            'prompts/custom_toolset.toolsets.jsonc': 'Custom toolsets configuration'
        }
        
        missing_configs = []
        for config_file, description in config_files.items():
            config_path = vscode_dir / config_file
            if not config_path.exists():
                missing_configs.append(f"{config_file} ({description})")
                logger.warning(f"⚠️  Missing: {config_file}")
        
        if missing_configs:
            self.issues_found.extend([f"Missing VS Code config: {config}" for config in missing_configs])
            return False
        else:
            logger.info("✅ VS Code configuration files found")
            
            # Validate toolset configuration
            try:
                import json
                toolset_path = vscode_dir / 'prompts/custom_toolset.toolsets.jsonc'
                content = toolset_path.read_text(encoding='utf-8')
                
                # Remove comments for JSON parsing
                lines = []
                for line in content.split('\n'):
                    if '//' in line:
                        line = line[:line.index('//')]
                    lines.append(line)
                clean_content = '\n'.join(lines)
                
                toolsets = json.loads(clean_content)
                logger.info(f"✅ Found {len(toolsets)} configured toolsets")
                
                # Check for empty toolsets
                empty_toolsets = [name for name, config in toolsets.items() 
                                if not config.get('tools', [])]
                if empty_toolsets:
                    logger.warning(f"⚠️  Found {len(empty_toolsets)} empty toolsets: {', '.join(empty_toolsets)}")
                    self.issues_found.extend([f"Empty toolset: {name}" for name in empty_toolsets])
                
            except Exception as e:
                logger.warning(f"Could not validate toolset configuration: {e}")
                self.issues_found.append("Invalid toolset configuration")
                return False
        
        return True

    def check_database_integrity(self) -> bool:
        """Check database files exist and are accessible."""
        logger.info("🗄️  Checking database integrity...")
        
        db_dir = self.base_path / 'database'
        required_dbs = ['knowledge.db', 'analytics.db', 'citations.db', 'workflows.db']
        
        if not db_dir.exists():
            logger.error("❌ Database directory missing")
            self.issues_found.append("Database directory missing")
            return False
        
        missing_dbs = []
        for db_name in required_dbs:
            db_path = db_dir / db_name
            if not db_path.exists():
                missing_dbs.append(db_name)
                logger.warning(f"⚠️  Missing database: {db_name}")
        
        if missing_dbs:
            self.issues_found.extend([f"Missing database: {db}" for db in missing_dbs])
            logger.info("💡 Run database/setup_databases.py to create missing databases")
            return False
        else:
            logger.info("✅ All required databases found")
            return True

    def generate_comprehensive_report(self) -> Dict:
        """Generate detailed validation report with metrics."""
        markdown_files = list(self.base_path.glob("**/*.md"))
        
        # Count files by directory
        dir_counts = {}
        total_size = 0
        
        for md_file in markdown_files:
            rel_path = md_file.relative_to(self.base_path)
            dir_name = str(rel_path.parent) if rel_path.parent != Path('.') else 'root'
            
            if dir_name not in dir_counts:
                dir_counts[dir_name] = {'count': 0, 'size': 0}
            
            dir_counts[dir_name]['count'] += 1
            file_size = md_file.stat().st_size
            dir_counts[dir_name]['size'] += file_size
            total_size += file_size
        
        report = {
            'timestamp': str(Path().cwd()),
            'base_path': str(self.base_path),
            'validation_summary': {
                'total_issues': len(self.issues_found),
                'validation_complete': len(self.issues_found) == 0,
                'issues_by_category': self._categorize_issues()
            },
            'content_metrics': {
                'total_markdown_files': len(markdown_files),
                'total_content_size': total_size,
                'average_file_size': total_size // len(markdown_files) if markdown_files else 0,
                'files_by_directory': dir_counts
            },
            'issues_found': self.issues_found,
            'recommendations': self._generate_recommendations()
        }
        
        return report

    def _categorize_issues(self) -> Dict[str, int]:
        """Categorize issues for better reporting."""
        categories = {
            'structure': 0,
            'content': 0,
            'frontmatter': 0,
            'configuration': 0,
            'git': 0,
            'other': 0
        }
        
        for issue in self.issues_found:
            if any(keyword in issue.lower() for keyword in ['directory', 'missing', 'structure']):
                categories['structure'] += 1
            elif any(keyword in issue.lower() for keyword in ['empty', 'minimal', 'content']):
                categories['content'] += 1
            elif any(keyword in issue.lower() for keyword in ['frontmatter', 'yaml']):
                categories['frontmatter'] += 1
            elif any(keyword in issue.lower() for keyword in ['vscode', 'toolset', 'config']):
                categories['configuration'] += 1
            elif any(keyword in issue.lower() for keyword in ['git', 'repository']):
                categories['git'] += 1
            else:
                categories['other'] += 1
        
        return categories

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on issues found."""
        recommendations = []
        
        issue_categories = self._categorize_issues()
        
        if issue_categories['content'] > 0:
            recommendations.append("Run content population workflow to address empty files")
        
        if issue_categories['frontmatter'] > 0:
            recommendations.append("Execute YAML frontmatter enforcement script")
        
        if issue_categories['structure'] > 0:
            recommendations.append("Create missing directories using --validate-all flag")
        
        if issue_categories['configuration'] > 0:
            recommendations.append("Review and update VS Code workspace configuration")
        
        if issue_categories['git'] > 0:
            recommendations.append("Address git repository integrity issues")
        
        if not recommendations:
            recommendations.append("Repository is well-organized and maintains good structure")
        
        return recommendations


def main() -> int:
    """Main execution function."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--verbose', action='store_true', help='Detailed output')
    parser.add_argument('--dry-run', action='store_true', help='Preview mode without changes')
    parser.add_argument('--quiet', action='store_true', help='Minimal output for CI/CD')
    parser.add_argument('--check-structure', action='store_true', help='Only check directory structure')
    parser.add_argument('--validate-all', action='store_true', help='Run all validation checks')
    parser.add_argument('--base-path', type=Path, default=Path.cwd(), help='Base path to validate')
    parser.add_argument('--output-json', type=Path, help='Output report as JSON to file')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        print("🔧 Knowledge Base Organization Maintenance")
        print("===========================================")
        
        if args.dry_run:
            print("🔍 Running in DRY-RUN mode - no changes will be made")
        
        # Initialize validator
        validator = AcademicStructureValidator(args.base_path, args.dry_run)
        
        validation_results = []
        
        # Run validations based on arguments
        if args.check_structure or args.validate_all:
            validation_results.append(validator.check_directory_structure())
        
        if args.validate_all:
            validation_results.append(validator.check_readme_files())
            validation_results.append(validator.check_root_files())
            validator.find_misplaced_files()
            validator.find_empty_files()
            validation_results.append(validator.validate_yaml_frontmatter())
            validation_results.append(validator.check_database_integrity())
            validation_results.append(validator.check_git_integrity())
            validation_results.append(validator.check_vscode_configuration())
        elif not args.check_structure:
            # Default: run structure and basic checks
            validation_results.append(validator.check_directory_structure())
            validation_results.append(validator.check_readme_files())
            validator.find_misplaced_files()
            validator.find_empty_files()
        
        # Generate comprehensive report
        report = validator.generate_comprehensive_report()
        
        if args.output_json:
            args.output_json.write_text(json.dumps(report, indent=2))
            logger.info(f"📊 Report saved to {args.output_json}")
        
        # Summary
        print()
        if report['validation_summary']['total_issues'] == 0:
            print("🎉 Organization maintenance complete! No issues found.")
            print(f"📊 Repository contains {report['content_metrics']['total_markdown_files']} markdown files")
            print(f"📏 Total content size: {report['content_metrics']['total_content_size'] // 1024}KB")
            return 0
        else:
            print(f"⚠️  Found {report['validation_summary']['total_issues']} issues that need attention:")
            
            # Show issues by category
            categories = report['validation_summary']['issues_by_category']
            for category, count in categories.items():
                if count > 0:
                    print(f"  📋 {category.title()}: {count} issues")
            
            print()
            print("📋 Issue Details:")
            for issue in report['issues_found'][:10]:  # Show first 10
                print(f"  - {issue}")
            if report['validation_summary']['total_issues'] > 10:
                print(f"  ... and {report['validation_summary']['total_issues'] - 10} more issues")
            
            print()
            print("💡 Recommended actions:")
            for i, recommendation in enumerate(report['recommendations'], 1):
                print(f"  {i}. {recommendation}")
            
            return 1
    
    except Exception as e:
        logger.error(f"Script failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
