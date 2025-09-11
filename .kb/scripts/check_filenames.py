#!/usr/bin/env python3
"""
Filename Policy Checker

Validates filenames against organizational naming conventions and policies.
Used by pre-commit hooks to ensure consistent naming standards.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any


class FilenameChecker:
    def __init__(self, policy_path: str = '.kb/policy/kb-policy.yaml'):
        self.policy_path = policy_path
        self.policy = self._load_policy()
        
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
    
    def _should_skip_path(self, path: str) -> bool:
        """Check if path should be skipped from validation."""
        skip_patterns = [
            '/.git/',
            '/.venv/',
            '/__pycache__/',
            '/.mypy_cache/',
            '/node_modules/',
            '.git/',
            '.venv/',
            '__pycache__/',
            '.mypy_cache/',
            'node_modules/',
        ]
        
        normalized_path = path.replace('\\', '/')
        return any(pattern in normalized_path for pattern in skip_patterns)
    
    def _check_naming_conventions(self, filename: str, filepath: str) -> List[str]:
        """Check filename against global naming conventions."""
        errors = []
        naming_config = self.policy.get('naming', {})
        
        # Check for forbidden spaces
        if naming_config.get('forbid_spaces', True) and ' ' in filename:
            errors.append(f"Spaces not allowed in filename: {filepath}")
        
        # Check allowed characters
        allowed_chars = naming_config.get('allowed_chars')
        if allowed_chars:
            pattern = re.compile(allowed_chars)
            if not pattern.match(filename):
                # Be more lenient with common file extensions and patterns
                if not re.match(r'^[a-zA-Z0-9._\-]+$', filename):
                    errors.append(f"Invalid characters in filename: {filepath}")
        
        # Check case convention
        case_convention = naming_config.get('case', 'kebab')
        if case_convention == 'kebab':
            # Allow kebab-case for base filename (excluding extension)
            name_without_ext = Path(filename).stem
            if '_' in name_without_ext and not name_without_ext.replace('_', '-').islower():
                errors.append(f"Filename should use kebab-case: {filepath}")
        elif case_convention == 'snake':
            # Allow snake_case
            name_without_ext = Path(filename).stem
            if '-' in name_without_ext:
                errors.append(f"Filename should use snake_case: {filepath}")
        
        return errors
    
    def _check_path_specific_rules(self, filepath: str) -> List[str]:
        """Check filename against path-specific rules."""
        errors = []
        path_rules = self.policy.get('paths', [])
        
        for rule in path_rules:
            if 'filename' in rule:
                try:
                    path_pattern = re.compile(rule['path'])
                    filename_pattern = re.compile(rule['filename'])
                    
                    # Check if this file is in a directory matching this rule
                    dir_path = str(Path(filepath).parent)
                    if path_pattern.search(dir_path):
                        filename = Path(filepath).name
                        if not filename_pattern.match(filename):
                            errors.append(
                                f"Filename doesn't match pattern for {rule['path']}: {filepath}"
                            )
                except re.error as e:
                    errors.append(f"Invalid regex in policy: {e}")
        
        return errors
    
    def _check_file_extensions(self, filename: str, filepath: str) -> List[str]:
        """Check if file extension is allowed."""
        errors = []
        file_config = self.policy.get('files', {})
        allowed_extensions = file_config.get('allowed_extensions', {})
        
        if not allowed_extensions:
            return errors  # No restrictions defined
        
        file_ext = Path(filename).suffix.lower()
        if not file_ext:
            return errors  # No extension
        
        # Check if extension is in any category
        extension_found = False
        for category, extensions in allowed_extensions.items():
            if file_ext in extensions:
                extension_found = True
                break
        
        if not extension_found:
            # Be lenient - only warn for clearly problematic extensions
            problematic_extensions = ['.exe', '.bin', '.dmg', '.deb', '.rpm']
            if file_ext in problematic_extensions:
                errors.append(f"Potentially problematic file extension: {filepath}")
        
        return errors
    
    def _check_file_size(self, filepath: str) -> List[str]:
        """Check if file size exceeds policy limits."""
        errors = []
        file_config = self.policy.get('files', {})
        max_size_mb = file_config.get('max_file_size_mb', 50)
        
        try:
            if os.path.exists(filepath):
                size_bytes = os.path.getsize(filepath)
                size_mb = size_bytes / (1024 * 1024)
                
                if size_mb > max_size_mb:
                    errors.append(
                        f"File size ({size_mb:.1f}MB) exceeds limit ({max_size_mb}MB): {filepath}"
                    )
        except OSError:
            pass  # File might not exist or be accessible
        
        return errors
    
    def check_file(self, filepath: str) -> List[str]:
        """Check a single file against all filename policies."""
        if self._should_skip_path(filepath):
            return []
        
        filename = Path(filepath).name
        errors = []
        
        # Run all checks
        errors.extend(self._check_naming_conventions(filename, filepath))
        errors.extend(self._check_path_specific_rules(filepath))
        errors.extend(self._check_file_extensions(filename, filepath))
        errors.extend(self._check_file_size(filepath))
        
        return errors
    
    def check_files(self, filepaths: List[str]) -> bool:
        """Check multiple files and return success status."""
        all_errors = []
        
        for filepath in filepaths:
            errors = self.check_file(filepath)
            all_errors.extend(errors)
        
        if all_errors:
            enforcement_level = self.policy.get('enforcement', {}).get('level', 'error')
            
            for error in all_errors:
                if enforcement_level == 'warning':
                    print(f"WARNING: {error}")
                else:
                    print(f"ERROR: {error}")
            
            return enforcement_level == 'warning'
        
        return True


def main():
    """Main entry point for the filename checker."""
    if len(sys.argv) <= 1:
        print("✅ No files provided for filename validation")
        return
    
    filepaths = sys.argv[1:]
    checker = FilenameChecker()
    
    success = checker.check_files(filepaths)
    
    if not success:
        sys.exit(1)
    else:
        print(f"✅ Filename validation passed for {len(filepaths)} files")


if __name__ == '__main__':
    main()