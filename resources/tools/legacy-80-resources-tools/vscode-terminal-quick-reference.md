---
title: VS Code Terminal Configuration Quick Reference
description: Quick reference and practical examples for VS Code integrated terminal setup
status: active
created: 2025-09-11
updated: 2025-09-11
tags:
  - vscode
  - terminal
  - configuration
  - quick-reference
  - automation
version: 1.0.0
authors:
  - lucas_galdino
---

# VS Code Terminal Configuration Quick Reference

## Essential Settings Configuration

### Basic Terminal Setup

```json
{
  "terminal.integrated.enableShellIntegration": true,
  "terminal.integrated.scrollback": 20000,
  "terminal.integrated.enablePersistentSessions": true,
  "terminal.integrated.tabs.enabled": true
}
```

### Terminal Profiles for Different Contexts

```json
{
  "terminal.integrated.profiles.linux": {
    "Bash (interactive)": {
      "path": "/bin/bash",
      "args": ["-l"],
      "icon": "terminal-bash",
      "color": "terminal.ansiGreen"
    },
    "Bash (automation)": {
      "path": "/bin/bash",
      "args": ["--noprofile", "--norc"],
      "icon": "rocket",
      "color": "terminal.ansiMagenta",
      "env": {
        "CI": "1",
        "NO_COLOR": "1"
      }
    }
  }
}
```

### Automation Profile Configuration

```json
{
  "terminal.integrated.automationProfile.linux": {
    "path": "/bin/bash",
    "args": ["--noprofile", "--norc", "-c"],
    "env": {
      "CI": "1",
      "DEBIAN_FRONTEND": "noninteractive",
      "NO_COLOR": "1"
    }
  }
}
```

### Auto-Replies for Common Prompts

```json
{
  "terminal.integrated.autoReplies": {
    "Do you want to continue\\? \\[Y/n\\]": "Y",
    "Proceed\\? \\(y/N\\)": "y",
    "Continue\\? \\[y/N\\]": "y"
  }
}
```

## Quick Commands

### Terminal Management

- `Ctrl+`` - Toggle terminal
- `Ctrl+Shift+`` - Create new terminal
- `Alt+Up/Down` - Navigate command history
- `Ctrl+Shift+5` - Split terminal

### Useful Terminal Commands

```bash
# Set strict bash options for automation
set -euo pipefail

# Non-interactive package installation
sudo apt-get update && sudo apt-get install -y package-name

# Git operations without prompts
git fetch --prune
git push --set-upstream origin branch-name
```

## Common Use Cases

### Development Workflow

1. **Interactive terminal**: For general development work
2. **Automation terminal**: For running scripts and CI/CD tasks
3. **Container terminal**: For Docker/container operations

### Task Integration

- Use `tasks.json` to define repeatable commands
- Link problem matchers for compiler output
- Set up background watchers for development servers

### CI/CD Alignment

- Mirror local tasks with CI pipeline steps
- Use same environment variables and flags
- Validate locally before pushing to remote

## Troubleshooting

### Shell Integration Issues

- Verify `enableShellIntegration` is true
- Check for terminal startup errors
- Ensure bash compatibility

### Performance Problems

- Reduce dotfile complexity
- Use minimal automation profiles
- Disable colors in automation contexts

### Auto-Reply Failures

- Test regex patterns with actual prompts
- Use escape characters for special characters
- Fall back to expect scripts for complex cases

## Related Resources

- [Full Automation Guide](<../../10-knowledge/methods/vscode-integrated-terminal-automation-guide.md>)
- [VS Code Terminal Documentation](https://code.visualstudio.com/docs/terminal/)
- [Shell Integration Guide](https://code.visualstudio.com/docs/terminal/shell-integration)
