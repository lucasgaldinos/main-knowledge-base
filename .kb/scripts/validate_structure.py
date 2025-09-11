#!/usr/bin/env python3
"""
Knowledge Base Structure Validator

Validates directory structure and required files against the organizational policy.
Used by pre-commit hooks to enforce organizational standards.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any


class StructureValidator:
    def __init__(self, policy_path: str = '.kb/policy/kb-policy.yaml'):
        self.policy_path = policy_path
        self.policy = self._load_policy()
        self.errors = []
        
    def _load_policy(self) -> Dict[str, Any]:
        """Load the organizational policy configuration."""
        try:
            with open(self.policy_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Policy file not found: {self.policy_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing policy file: {e}")
            sys.exit(1)
    
    def validate_required_files(self, repo_root: str) -> List[str]:
        """Check for required root-level files."""
        errors = []
        required = self.policy.get('require', [])
        
        for item in required:
            path = item['path'] if isinstance(item, dict) else item
            full_path = os.path.join(repo_root, path)
            
            if not os.path.exists(full_path):
                errors.append(f"Missing required file: {path}")
                
        return errors
    
    def validate_directory_structure(self, repo_root: str) -> List[str]:
        """Validate directory structure against policy rules."""
        errors = []
        path_rules = self.policy.get('paths', [])
        
        # Compile regex patterns for efficiency
        compiled_rules = []
        for rule in path_rules:
            try:
                compiled_rule = {
                    'path': re.compile(rule['path']),
                    'filename': re.compile(rule['filename']) if 'filename' in rule else None,
                    'required_files': rule.get('required_files', []),
                    'description': rule.get('description', ''),
                    'original_path': rule['path']
                }
                compiled_rules.append(compiled_rule)
            except re.error as e:
                errors.append(f"Invalid regex in policy for path '{rule['path']}': {e}")
        
        # Walk directory tree and validate
        for root, dirs, files in os.walk(repo_root):
            # Skip hidden directories and cache directories
            if any(part.startswith('.') for part in Path(root).parts):
                continue
                
            rel_path = os.path.relpath(root, repo_root)
            if rel_path == '.':
                continue
                
            # Check against path rules
            for rule in compiled_rules:
                if rule['path'].search(rel_path):
                    # Validate filenames in this directory
                    if rule['filename']:
                        for filename in files:
                            if not rule['filename'].match(filename):
                                errors.append(
                                    f"Filename policy violation in {rel_path}/: "
                                    f"'{filename}' doesn't match pattern for {rule['original_path']}"
                                )
                    
                    # Check for required files
                    for required_file in rule['required_files']:
                        required_path = os.path.join(root, required_file)
                        if not os.path.exists(required_path):
                            errors.append(
                                f"Missing required file in {rel_path}/: {required_file}"
                            )
        
        return errors
    
    def validate_naming_conventions(self, repo_root: str) -> List[str]:
        """Validate global naming conventions."""
        errors = []
        naming_config = self.policy.get('naming', {})
        
        forbid_spaces = naming_config.get('forbid_spaces', True)
        allowed_chars = naming_config.get('allowed_chars')
        
        if allowed_chars:
            pattern = re.compile(allowed_chars)
        else:
            pattern = None
        
        for root, dirs, files in os.walk(repo_root):
            # Skip system directories
            if any(part.startswith('.') for part in Path(root).parts if part not in ['.kb']):
                continue
                
            # Check directory names
            for dirname in dirs:
                if forbid_spaces and ' ' in dirname:
                    rel_path = os.path.relpath(os.path.join(root, dirname), repo_root)
                    errors.append(f"Spaces not allowed in directory name: {rel_path}")
                    
                if pattern and not pattern.match(dirname):
                    rel_path = os.path.relpath(os.path.join(root, dirname), repo_root)
                    errors.append(f"Invalid characters in directory name: {rel_path}")
            
            # Check file names
            for filename in files:
                if forbid_spaces and ' ' in filename:
                    rel_path = os.path.relpath(os.path.join(root, filename), repo_root)
                    errors.append(f"Spaces not allowed in filename: {rel_path}")
                    
                # Allow some flexibility for certain file types
                if filename.endswith(('.md', '.txt', '.py', '.yaml', '.yml', '.json')):
                    if pattern and not pattern.match(filename):
                        rel_path = os.path.relpath(os.path.join(root, filename), repo_root)
                        errors.append(f"Invalid characters in filename: {rel_path}")
        
        return errors
    
    def validate_all(self, repo_root: str = '.') -> bool:
        """Run all validations and return True if all pass."""
        repo_root = os.path.abspath(repo_root)
        
        self.errors.extend(self.validate_required_files(repo_root))
        self.errors.extend(self.validate_directory_structure(repo_root))
        self.errors.extend(self.validate_naming_conventions(repo_root))
        
        if self.errors:
            enforcement_level = self.policy.get('enforcement', {}).get('level', 'error')
            
            for error in self.errors:
                if enforcement_level == 'warning':
                    print(f"WARNING: {error}")
                else:
                    print(f"ERROR: {error}")
            
            return enforcement_level == 'warning'
        
        return True


def main():
    """Main entry point for the validator."""
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = '.'
    
    validator = StructureValidator()
    success = validator.validate_all(repo_root)
    
    if not success:
        sys.exit(1)
    else:
        if not validator.errors:
            print("✅ Knowledge base structure validation passed")


if __name__ == '__main__':
    main()