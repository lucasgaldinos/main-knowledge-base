#!/usr/bin/env python3
"""
Metadata Validator for Knowledge Base

Validates YAML front matter in Markdown files and standalone metadata files
against JSON schemas defined in the organizational policy.
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
try:
    from jsonschema import validate, Draft202012Validator, ValidationError
except ImportError:
    print("jsonschema package required. Install with: pip install jsonschema")
    sys.exit(1)


class MetadataValidator:
    def __init__(self, policy_path: str = '.kb/policy/kb-policy.yaml'):
        self.policy_path = policy_path
        self.policy = self._load_policy()
        self.schema_cache = {}
        
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
    
    def _load_schema(self, schema_path: str) -> Dict[str, Any]:
        """Load and cache JSON schema."""
        if schema_path in self.schema_cache:
            return self.schema_cache[schema_path]
            
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
                self.schema_cache[schema_path] = schema
                return schema
        except FileNotFoundError:
            print(f"Schema file not found: {schema_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing schema file {schema_path}: {e}")
            return None
    
    def _extract_yaml_frontmatter(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extract YAML front matter from Markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            return None
            
        # Check for YAML front matter
        if not content.startswith('---\n'):
            return None
            
        # Find the end of front matter
        try:
            end_marker = content.index('\n---\n', 4)
            frontmatter = content[4:end_marker]
            return yaml.safe_load(frontmatter) or {}
        except (ValueError, yaml.YAMLError):
            return None
    
    def _get_schema_for_path(self, file_path: str) -> Optional[str]:
        """Determine which schema applies to a given file path."""
        path_rules = self.policy.get('paths', [])
        
        for rule in path_rules:
            if 'schema' in rule:
                # Check if file path matches this rule
                try:
                    pattern = re.compile(rule['path'])
                    if pattern.search(file_path):
                        return rule['schema']
                except re.error:
                    continue
        
        return None
    
    def _validate_against_schema(self, data: Dict[str, Any], schema_path: str, file_path: str) -> List[str]:
        """Validate data against JSON schema."""
        schema = self._load_schema(schema_path)
        if not schema:
            return [f"Could not load schema {schema_path}"]
        
        errors = []
        try:
            validator = Draft202012Validator(schema)
            validation_errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
            
            for error in validation_errors:
                path_str = " -> ".join(str(p) for p in error.path) if error.path else "root"
                errors.append(f"{file_path}: {error.message} at {path_str}")
                
        except Exception as e:
            errors.append(f"{file_path}: Schema validation error: {e}")
        
        return errors
    
    def _validate_controlled_vocabularies(self, data: Dict[str, Any], file_path: str) -> List[str]:
        """Validate values against controlled vocabularies."""
        errors = []
        controlled_vocabs = self.policy.get('metadata', {}).get('controlled_vocabs', {})
        
        for field, allowed_values in controlled_vocabs.items():
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    if value not in allowed_values:
                        errors.append(
                            f"{file_path}: Invalid value '{value}' for field '{field}'. "
                            f"Allowed values: {', '.join(allowed_values)}"
                        )
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str) and item not in allowed_values:
                            errors.append(
                                f"{file_path}: Invalid value '{item}' in field '{field}'. "
                                f"Allowed values: {', '.join(allowed_values)}"
                            )
        
        return errors
    
    def validate_file(self, file_path: str) -> List[str]:
        """Validate a single file's metadata."""
        errors = []
        
        if file_path.endswith('.md'):
            # Extract and validate YAML front matter
            frontmatter = self._extract_yaml_frontmatter(file_path)
            if frontmatter is None:
                # Check if front matter is required for this path
                schema_path = self._get_schema_for_path(file_path)
                if schema_path:
                    errors.append(f"{file_path}: Missing required YAML front matter")
                return errors
                
            # Validate against schema
            schema_path = self._get_schema_for_path(file_path)
            if schema_path:
                errors.extend(self._validate_against_schema(frontmatter, schema_path, file_path))
            
            # Validate controlled vocabularies
            errors.extend(self._validate_controlled_vocabularies(frontmatter, file_path))
            
        elif file_path.endswith(('.yaml', '.yml')):
            # Validate standalone YAML files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                    
                schema_path = self._get_schema_for_path(file_path)
                if schema_path:
                    errors.extend(self._validate_against_schema(data, schema_path, file_path))
                
                errors.extend(self._validate_controlled_vocabularies(data, file_path))
                
            except yaml.YAMLError as e:
                errors.append(f"{file_path}: YAML parsing error: {e}")
            except UnicodeDecodeError:
                errors.append(f"{file_path}: File encoding error")
                
        elif file_path.endswith('.json'):
            # Validate JSON files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                schema_path = self._get_schema_for_path(file_path)
                if schema_path:
                    errors.extend(self._validate_against_schema(data, schema_path, file_path))
                
                errors.extend(self._validate_controlled_vocabularies(data, file_path))
                
            except json.JSONDecodeError as e:
                errors.append(f"{file_path}: JSON parsing error: {e}")
            except UnicodeDecodeError:
                errors.append(f"{file_path}: File encoding error")
        
        return errors
    
    def validate_files(self, file_paths: List[str]) -> bool:
        """Validate multiple files and return success status."""
        all_errors = []
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                errors = self.validate_file(file_path)
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
    """Main entry point for the metadata validator."""
    if len(sys.argv) <= 1:
        print("✅ No files provided for metadata validation")
        return
    
    file_paths = sys.argv[1:]
    validator = MetadataValidator()
    
    success = validator.validate_files(file_paths)
    
    if not success:
        sys.exit(1)
    else:
        print(f"✅ Metadata validation passed for {len(file_paths)} files")


if __name__ == '__main__':
    main()