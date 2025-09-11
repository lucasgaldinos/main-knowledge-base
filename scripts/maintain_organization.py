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

    def validate_yaml_frontmatter(self) -> bool:
        """Basic validation of YAML frontmatter presence."""
        logger.info("🏷️  Validating YAML frontmatter...")
        
        markdown_files = list(self.base_path.glob("**/*.md"))
        files_without_frontmatter = []
        
        for md_file in markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                if not content.startswith('---'):
                    files_without_frontmatter.append(md_file)
            except Exception as e:
                logger.warning(f"Could not read {md_file}: {e}")
        
        if files_without_frontmatter:
            logger.warning(f"⚠️  Found {len(files_without_frontmatter)} files without YAML frontmatter")
            for file_path in files_without_frontmatter[:5]:  # Show first 5
                logger.warning(f"  - {file_path.relative_to(self.base_path)}")
            if len(files_without_frontmatter) > 5:
                logger.warning(f"  ... and {len(files_without_frontmatter) - 5} more")
            logger.info("💡 Run yaml-frontmatter-enforcer.py to fix these issues")
            return False
        else:
            logger.info("✅ All markdown files have YAML frontmatter")
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

    def generate_report(self) -> Dict:
        """Generate comprehensive validation report."""
        return {
            'timestamp': str(Path().cwd()),
            'base_path': str(self.base_path),
            'issues_found': self.issues_found,
            'issue_count': len(self.issues_found),
            'validation_complete': len(self.issues_found) == 0
        }


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
            validation_results.append(validator.validate_yaml_frontmatter())
            validation_results.append(validator.check_database_integrity())
        elif not args.check_structure:
            # Default: run structure and basic checks
            validation_results.append(validator.check_directory_structure())
            validation_results.append(validator.check_readme_files())
            validator.find_misplaced_files()
        
        # Generate report
        report = validator.generate_report()
        
        if args.output_json:
            args.output_json.write_text(json.dumps(report, indent=2))
            logger.info(f"📊 Report saved to {args.output_json}")
        
        # Summary
        print()
        if report['issue_count'] == 0:
            print("🎉 Organization maintenance complete! No issues found.")
            return 0
        else:
            print(f"⚠️  Found {report['issue_count']} issues that need attention:")
            for issue in report['issues_found'][:10]:  # Show first 10
                print(f"  - {issue}")
            if report['issue_count'] > 10:
                print(f"  ... and {report['issue_count'] - 10} more issues")
            
            print()
            print("💡 Recommended actions:")
            print("  1. Run with --validate-all for complete analysis")
            print("  2. Run yaml-frontmatter-enforcer.py for YAML compliance")
            print("  3. Run database/setup_databases.py for missing databases")
            print("  4. Review and organize misplaced files")
            
            return 1
    
    except Exception as e:
        logger.error(f"Script failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
