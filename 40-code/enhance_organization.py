#!/usr/bin/env python3
"""
Repository Organization Enhancement Script

Automatically addresses common organization issues identified by maintain_organization.py
and implements best practices for academic knowledge base management.

Features:
- Creates missing README.md files with appropriate templates
- Organizes misplaced files into proper directory structure
- Generates YAML frontmatter for files missing it
- Creates comprehensive directory documentation

Usage:
    enhance_organization.py [options]

Examples:
    enhance_organization.py --auto-fix
    enhance_organization.py --create-readmes --organize-files
    enhance_organization.py --preview
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Dict, Optional
import json
from datetime import datetime
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
)
logger = logging.getLogger('enhance-organization')

class RepositoryOrganizationEnhancer:
    """Enhances repository organization through automated fixes."""
    
    def __init__(self, base_path: Path, dry_run: bool = False):
        self.base_path = base_path
        self.dry_run = dry_run
        self.changes_made = []
        
        # README templates for different directory types
        self.readme_templates = {
            'knowledge': """---
title: Knowledge Base Directory
description: Comprehensive repository of structured knowledge, methodologies, and insights
status: active
created: '{date}'
updated: '{date}'
tags:
- knowledge-management
- documentation
- academic-research
---

# Knowledge Base

This directory contains the core knowledge repository organized into four main categories:

## Directory Structure

### 📚 Foundations
Core concepts, principles, and foundational knowledge that underpins our research and development activities.

### 🔬 Methods
Methodologies, processes, implementation guides, and systematic approaches to various aspects of our work.

### 🎯 Applications
Applied knowledge, practical use cases, real-world examples, and implementation stories.

### 🔄 Synthesis
Research synthesis, meta-analysis, cross-domain insights, and integrated perspectives.

## Navigation

- Browse by category to find relevant knowledge areas
- Use search functionality to locate specific topics
- Follow cross-references between related documents
- Check status tags to understand content maturity

## Contributing

When adding content to the knowledge base:

1. Choose the appropriate category based on content type
2. Follow established naming conventions
3. Include comprehensive YAML frontmatter
4. Cross-reference related knowledge areas
5. Maintain consistent formatting and structure

## Maintenance

This directory is actively maintained and regularly updated. Content is reviewed for accuracy, relevance, and organization according to our governance framework.
""",
            
            'projects': """---
title: Projects Directory
description: Organized collection of active, completed, and archived projects with comprehensive tracking
status: active
created: '{date}'
updated: '{date}'
tags:
- project-management
- tracking
- documentation
---

# Projects

This directory contains all project-related documentation and deliverables organized by project lifecycle stage.

## Directory Structure

### 🚀 Active
Currently active projects with ongoing development, research, or implementation activities.

- Real-time progress tracking
- Current status and milestones
- Active collaboration documents
- Live development artifacts

### ✅ Completed
Successfully completed projects with final deliverables and completion reports.

- Final project reports
- Lessons learned documentation
- Success metrics and outcomes
- Archival documentation

### 📦 Archived
Deprecated, cancelled, or legacy projects maintained for historical reference.

- Historical project records
- Legacy system documentation
- Cancelled project analysis
- Sunset procedures and outcomes

## Project Lifecycle

1. **Initiation**: Projects start in the `active` directory with planning documents
2. **Development**: Active work proceeds with regular status updates
3. **Completion**: Successful projects move to `completed` with final reports
4. **Archival**: Obsolete projects move to `archived` for historical reference

## Project Documentation Standards

Each project should maintain:

- Clear project charter and objectives
- Regular status updates and progress reports
- Comprehensive completion reports
- Lessons learned and best practices
- Technical documentation and artifacts

## Navigation

Use the project status tags and categories to find relevant projects. Completion reports provide excellent learning opportunities and reference materials.
""",
            
            'resources': """---
title: Resources Directory
description: Curated collection of external resources, tools, and reference materials
status: active
created: '{date}'
updated: '{date}'
tags:
- resources
- references
- tools
- external-content
---

# Resources

This directory contains curated external resources, tools, and reference materials that support our research and development activities.

## Directory Structure

### 📖 Literature
Academic papers, research articles, and scholarly references organized by topic and relevance.

- Peer-reviewed publications
- Research papers and preprints
- Academic conference proceedings
- Systematic reviews and meta-analyses

### 🛠️ Tools
Documentation for tools, utilities, and software systems used in our workflows.

- Tool documentation and guides
- Configuration references
- Best practices and usage patterns
- Integration examples

### 📊 Data
Datasets, data sources, and data-related documentation for research and analysis.

- Research datasets
- Data source documentation
- Data processing scripts
- Analysis notebooks

## Resource Management

Resources are:

- **Curated**: Carefully selected for relevance and quality
- **Documented**: Include metadata and usage guidance
- **Maintained**: Regularly reviewed and updated
- **Accessible**: Organized for easy discovery and use

## Citation and Attribution

All resources include proper citation information and attribution. Follow academic standards for referencing and ensure compliance with usage rights and licensing terms.

## Contributing Resources

When adding new resources:

1. Verify quality and relevance
2. Include comprehensive metadata
3. Provide clear attribution and citation
4. Organize in appropriate subdirectory
5. Follow naming conventions

## Quality Standards

Resources are maintained according to academic standards with emphasis on:

- Credibility and authority
- Current relevance
- Proper documentation
- Clear organization
- Accessible formats
""",
            
            'outputs': """---
title: Outputs Directory
description: Generated content, build artifacts, and published materials
status: active
created: '{date}'
updated: '{date}'
tags:
- outputs
- generated-content
- artifacts
- publications
---

# Outputs

This directory contains generated content, build artifacts, and materials prepared for publication or distribution.

## Directory Structure

### 🏗️ Artifacts
Generated content and build artifacts from automated processes.

- Generated documentation
- Compiled reports
- Processed data outputs
- Automated analysis results

### 📚 Publications
Content prepared for external publication or distribution.

- Research papers
- Technical reports
- Presentation materials
- Public documentation

## Content Types

### Generated Artifacts
- Automatically generated from source materials
- Typically not manually edited
- Regenerated as source content changes
- Include generation metadata and timestamps

### Publication Materials
- Curated content for external audiences
- Manually reviewed and polished
- Version controlled for release management
- Include publication metadata and status

## Workflow Integration

This directory integrates with our automated workflows for:

- Continuous content generation
- Quality assurance processes
- Publication pipeline management
- Distribution and deployment

## Version Control

Generated content includes:

- Generation timestamps
- Source material references
- Version information
- Change tracking

Publication materials maintain:

- Release version control
- Publication status tracking
- Review and approval workflows
- Distribution records

## Maintenance

Generated artifacts are maintained automatically through our build processes. Publication materials undergo manual review and curation according to our quality standards.
""",
            
            'infrastructure': """---
title: Infrastructure Directory
description: Scripts, automation tools, and infrastructure management resources
status: active
created: '{date}'
updated: '{date}'
tags:
- infrastructure
- automation
- scripts
- maintenance
---

# Infrastructure

This directory contains scripts, automation tools, and infrastructure management resources that support the maintenance and operation of our knowledge base and research platform.

## Directory Structure

### 🤖 Scripts
Automation scripts for maintenance, organization, and workflow management.

- Repository maintenance scripts
- Content processing automation
- Quality assurance tools
- Workflow orchestration

## Infrastructure Components

### Maintenance Automation
- Repository organization validation
- Content quality assurance
- Automated testing and validation
- Performance monitoring

### Development Support
- Build and deployment scripts
- Development environment setup
- Testing frameworks
- Continuous integration tools

### Content Management
- Content processing pipelines
- Format conversion utilities
- Metadata management
- Search and indexing tools

## Usage Guidelines

Infrastructure tools are designed for:

- **Automated Execution**: Suitable for CI/CD pipelines
- **Manual Operation**: Direct execution for maintenance tasks
- **Development Support**: Tools for development workflows
- **Quality Assurance**: Validation and testing utilities

## Best Practices

When working with infrastructure tools:

1. Review documentation before execution
2. Use dry-run modes for testing
3. Backup important data before modifications
4. Follow security best practices
5. Monitor execution logs

## Security Considerations

Infrastructure scripts may have system-level access. Always:

- Review script contents before execution
- Run with minimal required permissions
- Use version-controlled scripts only
- Follow organizational security policies

## Contribution Guidelines

When adding infrastructure tools:

- Include comprehensive documentation
- Provide usage examples
- Implement proper error handling
- Follow coding standards
- Include security considerations
"""
        }
        
        # File organization mappings
        self.organization_mappings = {
            'system-design': 'knowledge/methods/',
            'architecture': 'knowledge/methods/',
            'completion-report': 'projects/completed/',
            'enhancement': 'knowledge/methods/',
            'research': 'knowledge/applications/',
            'guide': 'knowledge/methods/',
            'analysis': 'knowledge/applications/',
            'comparison': 'knowledge/applications/',
            'testing': 'knowledge/methods/',
            'workflow': 'knowledge/methods/',
            'platform': 'knowledge/methods/',
            'implementation': 'knowledge/methods/',
            'best-practices': 'knowledge/methods/',
        }

    def create_missing_readmes(self) -> int:
        """Create missing README.md files using appropriate templates."""
        logger.info("📝 Creating missing README.md files...")
        
        readmes_created = 0
        required_readmes = [
            ('knowledge', self.readme_templates['knowledge']),
            ('projects', self.readme_templates['projects']),
            ('resources', self.readme_templates['resources']),
            ('outputs', self.readme_templates['outputs']),
            ('infrastructure', self.readme_templates['infrastructure']),
        ]
        
        for dir_name, template in required_readmes:
            readme_path = self.base_path / dir_name / 'README.md'
            
            if not readme_path.exists():
                if not self.dry_run:
                    readme_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    content = template.format(
                        date=datetime.now().strftime('%Y-%m-%d')
                    )
                    
                    readme_path.write_text(content, encoding='utf-8')
                    logger.info(f"✅ Created README.md in: {dir_name}")
                else:
                    logger.info(f"📋 Would create README.md in: {dir_name}")
                
                self.changes_made.append(f"Created README.md in {dir_name}")
                readmes_created += 1
        
        if readmes_created == 0:
            logger.info("✅ All required README.md files already exist")
        else:
            logger.info(f"📝 Created {readmes_created} README.md files")
        
        return readmes_created

    def organize_misplaced_files(self) -> int:
        """Organize misplaced files into appropriate directory structure."""
        logger.info("📁 Organizing misplaced files...")
        
        files_moved = 0
        root_md_files = [
            f for f in self.base_path.glob("*.md")
            if f.name not in ['README.md', 'GOVERNANCE.md', 'CHANGELOG.md', 'CONTRIBUTING.md']
        ]
        
        for file_path in root_md_files:
            # Determine appropriate destination based on filename patterns
            filename = file_path.name.lower()
            destination_dir = None
            
            for pattern, target_dir in self.organization_mappings.items():
                if pattern in filename:
                    destination_dir = target_dir
                    break
            
            if not destination_dir:
                # Default organization based on content type
                if 'report' in filename:
                    destination_dir = 'projects/completed/'
                elif any(word in filename for word in ['guide', 'method', 'process']):
                    destination_dir = 'knowledge/methods/'
                else:
                    destination_dir = 'knowledge/applications/'
            
            destination_path = self.base_path / destination_dir / file_path.name
            
            if not self.dry_run:
                destination_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(destination_path))
                logger.info(f"📁 Moved {file_path.name} → {destination_dir}")
            else:
                logger.info(f"📋 Would move {file_path.name} → {destination_dir}")
            
            self.changes_made.append(f"Moved {file_path.name} to {destination_dir}")
            files_moved += 1
        
        if files_moved == 0:
            logger.info("✅ No misplaced files found in root directory")
        else:
            logger.info(f"📁 Organized {files_moved} misplaced files")
        
        return files_moved

    def fix_yaml_frontmatter(self) -> int:
        """Add missing YAML frontmatter to files that need it."""
        logger.info("🏷️  Adding missing YAML frontmatter...")
        
        files_fixed = 0
        markdown_files = list(self.base_path.glob("**/*.md"))
        
        for md_file in markdown_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                
                if not content.startswith('---'):
                    # Generate frontmatter based on file location and name
                    title = self._generate_title_from_filename(md_file.name)
                    description = f"Documentation for {title.lower()}"
                    
                    # Determine tags based on file location
                    rel_path = md_file.relative_to(self.base_path)
                    tags = self._generate_tags_from_path(rel_path)
                    
                    frontmatter = f"""---
title: {title}
description: {description}
status: draft
created: '{datetime.now().strftime('%Y-%m-%d')}'
updated: '{datetime.now().strftime('%Y-%m-%d')}'
tags:
{chr(10).join(f'- {tag}' for tag in tags)}
---

"""
                    
                    new_content = frontmatter + content
                    
                    if not self.dry_run:
                        md_file.write_text(new_content, encoding='utf-8')
                        logger.info(f"🏷️  Added frontmatter to: {md_file.relative_to(self.base_path)}")
                    else:
                        logger.info(f"📋 Would add frontmatter to: {md_file.relative_to(self.base_path)}")
                    
                    self.changes_made.append(f"Added frontmatter to {md_file.relative_to(self.base_path)}")
                    files_fixed += 1
                    
            except Exception as e:
                logger.warning(f"Could not process {md_file}: {e}")
        
        if files_fixed == 0:
            logger.info("✅ All markdown files have YAML frontmatter")
        else:
            logger.info(f"🏷️  Added frontmatter to {files_fixed} files")
        
        return files_fixed

    def _generate_title_from_filename(self, filename: str) -> str:
        """Generate human-readable title from filename."""
        # Remove extension and replace hyphens/underscores with spaces
        title = filename.replace('.md', '').replace('-', ' ').replace('_', ' ')
        # Capitalize words
        return ' '.join(word.capitalize() for word in title.split())

    def _generate_tags_from_path(self, rel_path: Path) -> List[str]:
        """Generate appropriate tags based on file path."""
        tags = []
        
        path_parts = rel_path.parts
        
        # Add directory-based tags
        if 'knowledge' in path_parts:
            tags.append('knowledge-base')
            if 'methods' in path_parts:
                tags.append('methodology')
            elif 'applications' in path_parts:
                tags.append('applications')
            elif 'foundations' in path_parts:
                tags.append('foundations')
            elif 'synthesis' in path_parts:
                tags.append('synthesis')
        
        if 'projects' in path_parts:
            tags.append('project-documentation')
            if 'completed' in path_parts:
                tags.append('completion-report')
        
        if 'resources' in path_parts:
            tags.append('resources')
            if 'tools' in path_parts:
                tags.append('tools')
            elif 'literature' in path_parts:
                tags.append('literature')
        
        # Add filename-based tags
        filename = rel_path.name.lower()
        if 'test' in filename:
            tags.append('testing')
        if 'guide' in filename:
            tags.append('guide')
        if 'analysis' in filename:
            tags.append('analysis')
        if 'research' in filename:
            tags.append('research')
        if 'implementation' in filename:
            tags.append('implementation')
        
        return tags or ['documentation']

    def generate_enhancement_report(self) -> Dict:
        """Generate comprehensive enhancement report."""
        return {
            'timestamp': datetime.now().isoformat(),
            'base_path': str(self.base_path),
            'dry_run': self.dry_run,
            'changes_made': self.changes_made,
            'changes_count': len(self.changes_made),
            'enhancement_complete': True
        }


def main() -> int:
    """Main execution function."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix all identified issues')
    parser.add_argument('--create-readmes', action='store_true', help='Create missing README.md files only')
    parser.add_argument('--organize-files', action='store_true', help='Organize misplaced files only')
    parser.add_argument('--fix-frontmatter', action='store_true', help='Fix YAML frontmatter only')
    parser.add_argument('--preview', action='store_true', help='Preview changes without making them')
    parser.add_argument('--verbose', action='store_true', help='Detailed output')
    parser.add_argument('--base-path', type=Path, default=Path.cwd(), help='Base path to enhance')
    parser.add_argument('--output-json', type=Path, help='Output report as JSON to file')
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        print("🔧 Repository Organization Enhancement")
        print("=====================================")
        
        dry_run = args.preview
        if dry_run:
            print("🔍 Running in PREVIEW mode - no changes will be made")
        
        # Initialize enhancer
        enhancer = RepositoryOrganizationEnhancer(args.base_path, dry_run)
        
        total_changes = 0
        
        # Run enhancements based on arguments
        if args.auto_fix or args.create_readmes:
            total_changes += enhancer.create_missing_readmes()
        
        if args.auto_fix or args.organize_files:
            total_changes += enhancer.organize_misplaced_files()
        
        if args.auto_fix or args.fix_frontmatter:
            total_changes += enhancer.fix_yaml_frontmatter()
        
        if not any([args.auto_fix, args.create_readmes, args.organize_files, args.fix_frontmatter]):
            # Default: run all enhancements
            total_changes += enhancer.create_missing_readmes()
            total_changes += enhancer.organize_misplaced_files()
            total_changes += enhancer.fix_yaml_frontmatter()
        
        # Generate report
        report = enhancer.generate_enhancement_report()
        
        if args.output_json:
            args.output_json.write_text(json.dumps(report, indent=2))
            logger.info(f"📊 Report saved to {args.output_json}")
        
        # Summary
        print()
        if total_changes == 0:
            print("🎉 Repository organization is already optimal! No changes needed.")
        else:
            if dry_run:
                print(f"📋 Would make {total_changes} organizational improvements:")
            else:
                print(f"✅ Successfully made {total_changes} organizational improvements:")
            
            for change in report['changes_made']:
                print(f"  ✓ {change}")
            
            if not dry_run:
                print()
                print("💡 Recommended next steps:")
                print("  1. Run maintain_organization.py --validate-all to verify improvements")
                print("  2. Review and customize generated README.md files")
                print("  3. Update YAML frontmatter as needed")
                print("  4. Commit changes to version control")
        
        return 0
    
    except Exception as e:
        logger.error(f"Enhancement failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())