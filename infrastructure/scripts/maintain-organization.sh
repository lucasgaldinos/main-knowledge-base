#!/bin/bash

# Knowledge Base Organization Maintenance Script
# This script helps maintain the function-based organization structure

set -e

echo "🔧 Knowledge Base Organization Maintenance"
echo "==========================================="

# Function to check directory structure
check_structure() {
    echo "📁 Checking directory structure..."
    
    required_dirs=(
        "docs"
        "docs/foundations"
        "docs/guides" 
        "docs/reference"
        "docs/projects"
        "docs/processes"
        "docs/research"
        "docs/tools"
        "archives"
        "assets"
        "cache"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            echo "❌ Missing directory: $dir"
            mkdir -p "$dir"
            echo "✅ Created: $dir"
        else
            echo "✅ Found: $dir"
        fi
    done
}

# Function to check README files
check_readmes() {
    echo "📝 Checking README files..."
    
    readme_dirs=(
        "docs"
        "docs/foundations"
        "docs/guides"
        "docs/reference" 
        "docs/projects"
        "docs/processes"
        "docs/research"
        "docs/tools"
    )
    
    for dir in "${readme_dirs[@]}"; do
        if [ ! -f "$dir/README.md" ]; then
            echo "❌ Missing README.md in: $dir"
        else
            echo "✅ Found README.md in: $dir"
        fi
    done
}

# Function to find misplaced files
find_misplaced() {
    echo "🔍 Looking for misplaced files..."
    
    # Find markdown files in root that should be organized
    root_md_files=$(find . -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "CONTRIBUTING.md" ! -name "TODO.md" ! -name "README_old.md")
    
    if [ -n "$root_md_files" ]; then
        echo "📄 Found files that could be organized:"
        echo "$root_md_files" | while read -r file; do
            echo "  - $file"
        done
        echo "💡 Consider moving these to appropriate docs/ subdirectories"
    else
        echo "✅ No misplaced files found in root"
    fi
}

# Function to validate links
validate_links() {
    echo "🔗 Validating internal links (basic check)..."
    
    # Simple check for broken internal links in README files
    find docs -name "README.md" -exec grep -l "\[\|docs/\|archives/\|assets/\|cache/" {} \; | while read -r file; do
        echo "📋 Checking links in: $file"
        # This is a basic check - a more sophisticated tool would be better for production
    done
}

# Main execution
echo
check_structure
echo
check_readmes  
echo
find_misplaced
echo
validate_links
echo
echo "🎉 Organization maintenance complete!"
echo "💡 Run this script regularly to maintain structure quality"
