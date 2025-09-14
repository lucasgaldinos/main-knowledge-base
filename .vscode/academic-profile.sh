#!/bin/bash
# Academic Workflow Terminal Profile Setup Script
# This script sets up the terminal environment for academic work

# Set academic environment variables
export PYTHONPATH="${WORKSPACEFOLDER:-$(pwd)}"
export ACADEMIC_MODE=1

# Activate virtual environment if available
if [ -f "./.venv/bin/activate" ]; then
    source ./.venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Set up academic aliases
alias acadcheck="uv run scripts/maintain_organization.py --verbose"
alias acadfix="uv run scripts/enhance_organization.py --auto-fix"
alias acadtest="uv run -m pytest scripts/ -v"
alias acadbackup="bash -c 'cd 30-data && find . -name \"*.db\" -exec cp {} backup/\$(date +%Y%m%d)_{} \;'"
alias acadtodos="grep -r \"TODO\\|FIXME\\|NOTE\\|RESEARCH\" --include=\"*.md\" --include=\"*.py\" ."

# Academic workflow functions
acadresearch() {
    echo "🔬 Starting academic research workflow..."
    echo "Available commands:"
    echo "  acadcheck  - Validate academic structure"
    echo "  acadfix    - Fix YAML frontmatter and organization"
    echo "  acadtest   - Run academic script tests"
    echo "  acadbackup - Backup academic databases"
    echo "  acadtodos  - Find all TODO items"
}

# Show welcome message
echo "📚 Academic Workflow Terminal Ready"
echo "Type 'acadresearch' for available commands"

# Set prompt to indicate academic mode
export PS1="[📚 Academic] \u@\h:\w\$ "
