---
title: "VS Code Performance Troubleshooting Manual"
description: "Step-by-step manual for diagnosing and fixing VS Code performance issues on Linux with NVIDIA GPUs"
status: active
created: 2025-09-14
updated: 2025-09-14
tags:
- manual
- troubleshooting
- vscode
- nvidia
- linux
- performance
version: 1.0.0
---

# VS Code Performance Troubleshooting Manual

## Quick Diagnosis Checklist

### 🚨 Emergency Symptoms Recognition

**Immediate Action Required:**

- [ ] VS Code consuming >4GB RAM
- [ ] System swap usage >70%
- [ ] UI completely unresponsive
- [ ] GPU temperature >85°C
- [ ] Multiple zombie VS Code processes

**Quick Recovery:**

```bash
# Kill problematic processes
pkill -f "code.*zygote"

# Clear cache
rm -rf ~/.config/Code/CachedData/*

# Restart with minimal config
code --disable-extensions --disable-gpu
```

### 🔍 Systematic Diagnosis Steps

#### Step 1: Identify the Problem Type

**Memory Issues:**

```bash
# Check current memory usage
free -h
smem -t -k | grep code
```

**GPU Issues:**

```bash
# Monitor GPU
nvidia-smi dmon -s pucm

# Test without GPU
code --disable-gpu
```

**Extension Issues:**

```bash
# Check running extensions
# F1 > Developer: Show Running Extensions
# F1 > Extensions: Bisect
```

#### Step 2: Gather System Information

```bash
# Create diagnostic report
cat > vscode-diagnostic.txt << EOF
=== System Information ===
OS: $(lsb_release -d | cut -f2)
Kernel: $(uname -r)
VS Code Version: $(code --version | head -1)
NVIDIA Driver: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader)

=== Memory Status ===
$(free -h)

=== GPU Status ===
$(nvidia-smi)

=== VS Code Processes ===
$(ps aux | grep code | head -10)

=== Extension List ===
$(code --list-extensions)
EOF
```

#### Step 3: Apply Targeted Solutions

**For Memory Issues:**

1. Check swap usage: `free -h`
2. If swap >50%, restart VS Code
3. Implement memory settings (see configuration section)
4. Monitor with: `watch -n 5 'smem -t -k | grep code'`

**For GPU Issues:**

1. Test different GPU paths:
   ```bash
   # Wayland
   ELECTRON_OZONE_PLATFORM_HINT=wayland code

   # X11
   ELECTRON_OZONE_PLATFORM_HINT=x11 code

   # Different GL backends
   code --use-gl=desktop
   code --use-gl=egl
   ```

**For Extension Issues:**

1. Disable all extensions: `code --disable-extensions`
2. Enable one by one to identify culprit
3. Check Copilot Chat memory specifically

## Configuration Templates

### Essential VS Code Settings

Save to `~/.config/Code/User/settings.json`:

```json
{
  "terminal.integrated.gpuAcceleration": "off",
  "workbench.list.smoothScrolling": false,
  "window.titleBarStyle": "native",
  "editor.semanticHighlighting.enabled": false,
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/**": true,
    "**/dist/**": true,
    "**/build/**": true,
    "**/.venv/**": true,
    "**/venv/**": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.venv": true,
    "**/venv": true
  },
  "git.autofetch": false,
  "typescript.tsserver.maxTsServerMemory": 3072,
  "editor.quickSuggestions": {
    "other": false,
    "comments": false,
    "strings": false
  },
  "github.copilot.enable": {
    "*": true,
    "yaml": false,
    "plaintext": false
  }
}
```

### System Optimization Script

Create `~/bin/vscode-optimize.sh`:

```bash
#!/bin/bash
set -euo pipefail

echo "🔧 Optimizing VS Code environment..."

# Enable NVIDIA persistence mode
if command -v nvidia-smi &> /dev/null; then
    sudo nvidia-smi -pm 1
    echo "✅ NVIDIA persistence mode enabled"
fi

# Increase inotify watchers
if [[ $(sysctl -n fs.inotify.max_user_watches) -lt 524288 ]]; then
    sudo sysctl fs.inotify.max_user_watches=524288
    echo "✅ Increased inotify watchers"
fi

# Clear VS Code cache
if [[ -d ~/.config/Code/CachedData ]]; then
    rm -rf ~/.config/Code/CachedData/*
    echo "✅ Cleared VS Code cache"
fi

# Set Node.js options
export VSCODE_NODE_OPTIONS="--max-old-space-size=3072"
echo "✅ Set Node.js memory limit"

echo "🚀 Optimization complete. Launch VS Code with:"
echo "   ELECTRON_OZONE_PLATFORM_HINT=x11 code"
```

### Monitoring Script

Create `~/bin/vscode-monitor.sh`:

```bash
#!/bin/bash

LOGFILE="$HOME/vscode-performance.log"
ALERT_THRESHOLD_MB=4096

monitor_performance() {
    while true; do
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

        # Get memory usage in MB
        MEMORY_MB=$(ps -o pid,rss,comm -C code | awk 'NR>1 {sum+=$2} END {print sum/1024}')

        # Check if above threshold
        if (( $(echo "$MEMORY_MB > $ALERT_THRESHOLD_MB" | bc -l) )); then
            notify-send "VS Code Memory Alert" "Memory usage: ${MEMORY_MB}MB"
        fi

        # Log details
        echo "=== $TIMESTAMP ===" >> "$LOGFILE"
        echo "Total VS Code Memory: ${MEMORY_MB}MB" >> "$LOGFILE"
        ps aux | grep -E "code.*--" >> "$LOGFILE"
        echo "" >> "$LOGFILE"

        sleep 60
    done
}

echo "Starting VS Code performance monitoring..."
echo "Alert threshold: ${ALERT_THRESHOLD_MB}MB"
echo "Log file: $LOGFILE"

monitor_performance &
MONITOR_PID=$!
echo "Monitor PID: $MONITOR_PID"
echo "To stop: kill $MONITOR_PID"
```

## Common Scenarios and Solutions

### Scenario 1: Long Copilot Chat Sessions

**Symptoms:**

- VS Code memory >3GB
- Chat UI becomes sluggish
- Extension Host high memory

**Solution:**

1. Clear current chat: Click "Clear Chat" button
2. Archive important responses to files
3. Restart window: `F1 > Developer: Reload Window`
4. Implement session rotation (every 20-30 prompts)

### Scenario 2: GPU Driver Conflicts

**Symptoms:**

- Graphical glitches
- Black screens
- Crash on startup

**Solution:**

1. Test without GPU: `code --disable-gpu`
2. If stable, try different GPU paths:
   ```bash
   code --use-gl=desktop
   code --use-gl=egl
   code --disable-features=VizDisplayCompositor
   ```
3. Update NVIDIA drivers
4. Consider X11 over Wayland

### Scenario 3: TypeScript Project Slowdowns

**Symptoms:**

- Slow autocomplete
- High tsserver memory
- File operations lag

**Solution:**

1. Limit tsserver memory:
   ```json
   "typescript.tsserver.maxTsServerMemory": 3072
   ```
2. Exclude unnecessary directories:
   ```json
   "typescript.preferences.exclude": [
     "**/node_modules",
     "**/dist",
     "**/.git"
   ]
   ```
3. Restart TypeScript server: `F1 > TypeScript: Restart TS Server`

### Scenario 4: System Memory Pressure

**Symptoms:**

- High swap usage
- System lag
- OOM killer activation

**Solution:**

1. Immediate relief:
   ```bash
   sudo sysctl vm.drop_caches=3
   pkill -f "code.*helper.*--type=utility"
   ```
2. Long-term:
   - Increase RAM if possible
   - Use zram for better swap performance
   - Implement memory limits with systemd

## Recovery Procedures

### Complete Reset

```bash
# Stop all VS Code processes
pkill -f code

# Clear all caches and logs
rm -rf ~/.config/Code/CachedData/*
rm -rf ~/.config/Code/logs/*
rm -rf ~/.config/Code/User/workspaceStorage/*

# Reset extensions (backup first)
cp -r ~/.vscode/extensions ~/.vscode/extensions.backup
rm -rf ~/.vscode/extensions/*

# Restart with clean profile
code --user-data-dir /tmp/vscode-clean
```

### Gradual Restoration

```bash
# Test baseline functionality
code --disable-extensions

# Enable essential extensions only
code --enable-extension ms-python.python
code --enable-extension ms-vscode.vscode-typescript-next

# Test Copilot separately
code --enable-extension github.copilot
code --enable-extension github.copilot-chat
```

## Prevention Strategies

### Daily Maintenance

1. **Morning Checklist:**
   ```bash
   # Check system resources
   free -h

   # Clear caches if needed
   [ $(du -sm ~/.config/Code/CachedData | cut -f1) -gt 500 ] && rm -rf ~/.config/Code/CachedData/*
   ```

2. **Session Hygiene:**
   - Restart VS Code every 4-6 hours during heavy use
   - Clear Copilot Chat after long sessions
   - Close unused workspaces

### Weekly Maintenance

1. **System Updates:**
   ```bash
   sudo apt update && sudo apt upgrade
   code --update-extensions
   ```

2. **Performance Review:**
   ```bash
   # Check performance logs
   tail -50 ~/vscode-performance.log

   # Review extension usage
   code --list-extensions --show-versions
   ```

### Monthly Maintenance

1. **Deep Cleaning:**
   ```bash
   # Clear all temporary files
   rm -rf ~/.config/Code/CachedData/*
   rm -rf ~/.config/Code/logs/*

   # Vacuum SQLite databases
   find ~/.config/Code -name "*.vscdb" -exec sqlite3 {} "VACUUM;" \;
   ```

2. **Configuration Review:**
   - Review and update settings.json
   - Audit installed extensions
   - Check for new optimization opportunities

## Emergency Contacts and Resources

### Log Locations

- VS Code logs: `~/.config/Code/logs/`
- System logs: `journalctl -u display-manager`
- NVIDIA logs: `journalctl | grep nvidia`

### Useful Commands Reference

```bash
# Quick status check
code --status

# Extension management
code --list-extensions
code --disable-extension <extension-id>
code --enable-extension <extension-id>

# Memory monitoring
smem -t -k | grep code
ps aux | grep code

# GPU monitoring
nvidia-smi dmon -s pucm
watch -n 1 nvidia-smi
```

### When to Escalate

- Multiple crashes per day
- Consistent >8GB memory usage
- GPU driver conflicts affecting other applications
- Data loss or corruption

Consider filing issues with:

- VS Code GitHub repository
- NVIDIA developer forums
- Distribution-specific forums
