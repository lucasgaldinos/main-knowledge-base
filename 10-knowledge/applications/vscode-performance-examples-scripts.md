---
title: "VS Code Performance Optimization Examples and Scripts"
description: "Practical examples, scripts, and automation tools for optimizing VS Code performance on Linux with NVIDIA GPUs"
status: active
created: 2025-09-14
updated: 2025-09-14
tags:
- examples
- scripts
- automation
- vscode
- nvidia
- performance
- linux
version: 1.0.0
---

# VS Code Performance Optimization Examples and Scripts

## Quick Start Scripts

### 1. System Diagnostic Script

```bash
#!/bin/bash
# vscode-diagnostics.sh - Comprehensive system and VS Code diagnostics

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Output file
OUTPUT_FILE="vscode-diagnostic-$(date +%Y%m%d_%H%M%S).txt"

echo -e "${BLUE}🔍 VS Code Performance Diagnostics${NC}"
echo "Output will be saved to: $OUTPUT_FILE"
echo ""

# Function to log with timestamp
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$OUTPUT_FILE"
}

# System Information
log "${BLUE}=== SYSTEM INFORMATION ===${NC}"
log "OS: $(lsb_release -d | cut -f2- || echo 'Unknown')"
log "Kernel: $(uname -r)"
log "Architecture: $(uname -m)"
log "CPU: $(lscpu | grep 'Model name' | cut -d':' -f2 | xargs)"
log "CPU Cores: $(nproc)"
log ""

# Memory Information
log "${BLUE}=== MEMORY INFORMATION ===${NC}"
free -h | tee -a "$OUTPUT_FILE"
log ""

# GPU Information
log "${BLUE}=== GPU INFORMATION ===${NC}"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi | tee -a "$OUTPUT_FILE"
    log ""
    log "GPU Memory Details:"
    nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUTPUT_FILE"
else
    log "${YELLOW}⚠️ NVIDIA drivers not installed or nvidia-smi not available${NC}"
fi
log ""

# VS Code Information
log "${BLUE}=== VS CODE INFORMATION ===${NC}"
if command -v code &> /dev/null; then
    log "VS Code Version: $(code --version | head -1)"
    log "Installation Path: $(which code)"

    # Check for running VS Code processes
    log ""
    log "Running VS Code Processes:"
    ps aux | grep -E "code.*--" | grep -v grep | tee -a "$OUTPUT_FILE" || log "No VS Code processes running"

    # Extension information
    log ""
    log "Installed Extensions (first 20):"
    code --list-extensions | head -20 | tee -a "$OUTPUT_FILE"

    # Check VS Code status if running
    if pgrep -f "code" > /dev/null; then
        log ""
        log "VS Code Status:"
        timeout 10s code --status 2>/dev/null | tee -a "$OUTPUT_FILE" || log "Could not retrieve VS Code status"
    fi
else
    log "${RED}❌ VS Code not found in PATH${NC}"
fi
log ""

# Memory usage by VS Code
log "${BLUE}=== VS CODE MEMORY USAGE ===${NC}"
if command -v smem &> /dev/null; then
    log "Detailed Memory Usage (PSS):"
    smem -t -k | grep -i code | tee -a "$OUTPUT_FILE" || log "No VS Code processes found"
else
    log "Basic Memory Usage (RSS):"
    ps aux | grep -E "code.*--" | grep -v grep | awk '{print $6/1024 " MB - " $11}' | tee -a "$OUTPUT_FILE" || log "No VS Code processes found"
fi
log ""

# Swap usage
log "${BLUE}=== SWAP USAGE ===${NC}"
swapon --show | tee -a "$OUTPUT_FILE"
log "Swap usage details:"
cat /proc/swaps | tee -a "$OUTPUT_FILE"
log ""

# Graphics configuration
log "${BLUE}=== GRAPHICS CONFIGURATION ===${NC}"
log "Display server: ${XDG_SESSION_TYPE:-unknown}"
log "Current display: ${DISPLAY:-not set}"
log "Wayland display: ${WAYLAND_DISPLAY:-not set}"

if command -v glxinfo &> /dev/null; then
    log ""
    log "OpenGL Information:"
    glxinfo | grep -E "(direct rendering|OpenGL vendor|OpenGL renderer|OpenGL version)" | tee -a "$OUTPUT_FILE"
fi

if command -v vainfo &> /dev/null; then
    log ""
    log "VAAPI Information:"
    vainfo 2>&1 | head -10 | tee -a "$OUTPUT_FILE"
fi
log ""

# System load and processes
log "${BLUE}=== SYSTEM LOAD ===${NC}"
uptime | tee -a "$OUTPUT_FILE"
log ""
log "Top memory consumers:"
ps aux --sort=-%mem | head -10 | tee -a "$OUTPUT_FILE"
log ""

# Disk usage
log "${BLUE}=== DISK USAGE ===${NC}"
df -h / | tee -a "$OUTPUT_FILE"
log ""
log "VS Code cache sizes:"
if [[ -d ~/.config/Code ]]; then
    du -sh ~/.config/Code/* 2>/dev/null | sort -hr | head -10 | tee -a "$OUTPUT_FILE"
fi
log ""

# Network and file limits
log "${BLUE}=== SYSTEM LIMITS ===${NC}"
log "File descriptor limits:"
ulimit -n | tee -a "$OUTPUT_FILE"
log "inotify limits:"
sysctl fs.inotify.max_user_watches | tee -a "$OUTPUT_FILE"
log ""

# Recent errors in system logs
log "${BLUE}=== RECENT SYSTEM ERRORS ===${NC}"
log "Recent GPU-related errors:"
journalctl --since "1 hour ago" -p err | grep -i nvidia | tail -5 | tee -a "$OUTPUT_FILE" || log "No recent NVIDIA errors"
log ""
log "Recent VS Code crashes:"
journalctl --since "1 hour ago" -p err | grep -i code | tail -5 | tee -a "$OUTPUT_FILE" || log "No recent VS Code errors"
log ""

# Configuration files
log "${BLUE}=== CONFIGURATION FILES ===${NC}"
if [[ -f ~/.config/Code/User/settings.json ]]; then
    log "VS Code settings.json exists ($(wc -l < ~/.config/Code/User/settings.json) lines)"
    log "Key performance settings:"
    grep -E "(gpu|memory|smooth|semantic|watcher)" ~/.config/Code/User/settings.json | tee -a "$OUTPUT_FILE" || log "No performance-related settings found"
fi
log ""

echo -e "${GREEN}✅ Diagnostics complete. Report saved to: $OUTPUT_FILE${NC}"
echo -e "${YELLOW}💡 Review the report and share it when seeking support${NC}"
```

### 2. Performance Optimization Script

```bash
#!/bin/bash
# vscode-optimize.sh - Optimize VS Code for better performance

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo -e "${RED}❌ Do not run this script as root${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 VS Code Performance Optimizer${NC}"
echo ""

# Function to ask for confirmation
confirm() {
    while true; do
        read -p "$1 (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            return 0
        elif [[ $REPLY =~ ^[Nn]$ ]]; then
            return 1
        fi
    done
}

# 1. System optimizations
echo -e "${YELLOW}📊 System Optimizations${NC}"

if confirm "Increase inotify watchers limit?"; then
    echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.d/99-vscode.conf
    sudo sysctl fs.inotify.max_user_watches=524288
    echo -e "${GREEN}✅ Increased inotify watchers${NC}"
fi

if command -v nvidia-smi &> /dev/null; then
    if confirm "Enable NVIDIA persistence mode?"; then
        sudo nvidia-smi -pm 1
        echo -e "${GREEN}✅ NVIDIA persistence mode enabled${NC}"
    fi
fi

# 2. VS Code settings optimization
echo ""
echo -e "${YELLOW}⚙️  VS Code Settings Optimization${NC}"

VSCODE_SETTINGS="$HOME/.config/Code/User/settings.json"
BACKUP_SETTINGS="$HOME/.config/Code/User/settings.json.backup.$(date +%Y%m%d_%H%M%S)"

if [[ -f "$VSCODE_SETTINGS" ]]; then
    if confirm "Backup and optimize VS Code settings?"; then
        cp "$VSCODE_SETTINGS" "$BACKUP_SETTINGS"
        echo -e "${GREEN}✅ Settings backed up to: $BACKUP_SETTINGS${NC}"

        # Create optimized settings
        cat > "$VSCODE_SETTINGS" << 'EOF'
{
    "terminal.integrated.gpuAcceleration": "off",
    "workbench.list.smoothScrolling": false,
    "window.titleBarStyle": "native",
    "editor.semanticHighlighting.enabled": false,
    "editor.bracketPairColorization.enabled": false,
    "editor.guides.bracketPairs": false,
    "files.watcherExclude": {
        "**/node_modules/**": true,
        "**/.git/**": true,
        "**/dist/**": true,
        "**/build/**": true,
        "**/.venv/**": true,
        "**/venv/**": true,
        "**/target/**": true,
        "**/.next/**": true
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/dist": true,
        "**/build": true,
        "**/.venv": true,
        "**/venv": true,
        "**/target": true,
        "**/.next": true
    },
    "git.autofetch": false,
    "git.autoRepositoryDetection": false,
    "typescript.tsserver.maxTsServerMemory": 3072,
    "typescript.preferences.includePackageJsonAutoImports": "off",
    "editor.quickSuggestions": {
        "other": false,
        "comments": false,
        "strings": false
    },
    "editor.parameterHints.enabled": false,
    "editor.hover.delay": 1000,
    "editor.lightbulb.enabled": false,
    "breadcrumbs.enabled": false,
    "workbench.iconTheme": null,
    "workbench.productIconTheme": "Default",
    "extensions.autoUpdate": false,
    "update.mode": "manual",
    "telemetry.telemetryLevel": "off"
}
EOF
        echo -e "${GREEN}✅ Optimized settings applied${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ VS Code settings file not found. Run VS Code first.${NC}"
fi

# 3. Environment optimization
echo ""
echo -e "${YELLOW}🌍 Environment Optimization${NC}"

BASHRC="$HOME/.bashrc"
PROFILE="$HOME/.profile"

if confirm "Add VS Code environment optimizations to shell profile?"; then
    # Add to .bashrc
    cat >> "$BASHRC" << 'EOF'

# VS Code Performance Optimizations
export VSCODE_NODE_OPTIONS="--max-old-space-size=3072"
export ELECTRON_OZONE_PLATFORM_HINT=x11

# VS Code aliases
alias vscode-clean='pkill -f "code.*helper"; sleep 2; code'
alias vscode-monitor='watch -n 5 "free -h && echo && ps aux | grep code | head -5"'
alias vscode-status='code --status'
EOF
    echo -e "${GREEN}✅ Environment optimizations added to .bashrc${NC}"
fi

# 4. Create optimization scripts
echo ""
echo -e "${YELLOW}📝 Creating Utility Scripts${NC}"

SCRIPTS_DIR="$HOME/.local/bin"
mkdir -p "$SCRIPTS_DIR"

# Memory monitor script
cat > "$SCRIPTS_DIR/vscode-memory-monitor.sh" << 'EOF'
#!/bin/bash
# Monitor VS Code memory usage

THRESHOLD_MB=4096
LOGFILE="$HOME/vscode-memory.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    MEMORY_MB=$(ps -o pid,rss,comm -C code 2>/dev/null | awk 'NR>1 {sum+=$2} END {print sum/1024}')

    if [[ -n "$MEMORY_MB" ]]; then
        echo "$TIMESTAMP: VS Code Memory: ${MEMORY_MB}MB" >> "$LOGFILE"

        if (( $(echo "$MEMORY_MB > $THRESHOLD_MB" | bc -l 2>/dev/null || echo 0) )); then
            notify-send "VS Code Memory Alert" "Memory usage: ${MEMORY_MB}MB"
        fi
    fi

    sleep 300  # Check every 5 minutes
done
EOF

# GPU monitor script
cat > "$SCRIPTS_DIR/vscode-gpu-monitor.sh" << 'EOF'
#!/bin/bash
# Monitor GPU usage with VS Code

if ! command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA drivers not available"
    exit 1
fi

echo "Monitoring GPU usage. Press Ctrl+C to stop."
echo "Timestamp,GPU_Usage_%,Memory_Used_MB,Memory_Total_MB,Temperature_C"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    GPU_DATA=$(nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits)
    echo "$TIMESTAMP,$GPU_DATA"
    sleep 5
done
EOF

# Cleanup script
cat > "$SCRIPTS_DIR/vscode-cleanup.sh" << 'EOF'
#!/bin/bash
# Clean VS Code caches and temporary files

echo "🧹 Cleaning VS Code caches..."

# Kill VS Code processes
pkill -f code || true
sleep 2

# Clear caches
if [[ -d ~/.config/Code/CachedData ]]; then
    echo "Clearing cached data..."
    rm -rf ~/.config/Code/CachedData/*
fi

if [[ -d ~/.config/Code/logs ]]; then
    echo "Clearing logs..."
    find ~/.config/Code/logs -name "*.log" -mtime +7 -delete
fi

if [[ -d ~/.config/Code/User/workspaceStorage ]]; then
    echo "Clearing workspace storage..."
    find ~/.config/Code/User/workspaceStorage -name "*.vscdb" -exec sqlite3 {} "VACUUM;" \;
fi

echo "✅ Cleanup complete"
EOF

# Make scripts executable
chmod +x "$SCRIPTS_DIR"/{vscode-memory-monitor.sh,vscode-gpu-monitor.sh,vscode-cleanup.sh}
echo -e "${GREEN}✅ Utility scripts created in $SCRIPTS_DIR${NC}"

# 5. Create desktop launcher with optimizations
echo ""
if confirm "Create optimized VS Code desktop launcher?"; then
    DESKTOP_FILE="$HOME/.local/share/applications/code-optimized.desktop"

    cat > "$DESKTOP_FILE" << 'EOF'
[Desktop Entry]
Name=VS Code (Optimized)
Comment=Code Editing. Redefined. (Performance Optimized)
GenericName=Text Editor
Exec=env VSCODE_NODE_OPTIONS="--max-old-space-size=3072" ELECTRON_OZONE_PLATFORM_HINT=x11 code --use-gl=desktop
Icon=vscode
Type=Application
StartupNotify=true
StartupWMClass=Code
Categories=Utility;TextEditor;Development;IDE;
MimeType=text/plain;inode/directory;application/x-code-workspace;
Actions=new-empty-window;
Keywords=vscode;

[Desktop Action new-empty-window]
Name=New Empty Window
Exec=env VSCODE_NODE_OPTIONS="--max-old-space-size=3072" ELECTRON_OZONE_PLATFORM_HINT=x11 code --use-gl=desktop --new-window
Icon=vscode
EOF

    echo -e "${GREEN}✅ Optimized desktop launcher created${NC}"
fi

# 6. System service for monitoring (optional)
echo ""
if confirm "Create systemd user service for memory monitoring?"; then
    SYSTEMD_DIR="$HOME/.config/systemd/user"
    mkdir -p "$SYSTEMD_DIR"

    cat > "$SYSTEMD_DIR/vscode-monitor.service" << EOF
[Unit]
Description=VS Code Memory Monitor
After=graphical-session.target

[Service]
Type=simple
ExecStart=$SCRIPTS_DIR/vscode-memory-monitor.sh
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

    systemctl --user daemon-reload
    echo -e "${GREEN}✅ Systemd service created${NC}"
    echo -e "${YELLOW}💡 Enable with: systemctl --user enable --now vscode-monitor${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Optimization complete!${NC}"
echo ""
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "1. Restart your terminal to load new environment variables"
echo "2. Launch VS Code with: code (now optimized)"
echo "3. Monitor performance with: vscode-monitor"
echo "4. Clean caches when needed: vscode-cleanup.sh"
echo ""
echo -e "${BLUE}💡 Pro Tips:${NC}"
echo "• Clear Copilot Chat after long sessions"
echo "• Restart VS Code every 4-6 hours during heavy use"
echo "• Use vscode-memory-monitor.sh to track usage"
echo "• Check logs in ~/vscode-memory.log"
```

### 3. Real-time Monitoring Dashboard

```bash
#!/bin/bash
# vscode-dashboard.sh - Real-time performance dashboard

set -euo pipefail

# Check dependencies
for cmd in watch bc; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "❌ Required command '$cmd' not found"
        exit 1
    fi
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to get VS Code memory usage
get_vscode_memory() {
    ps -o pid,rss,comm -C code 2>/dev/null | awk 'NR>1 {sum+=$2} END {print sum/1024}' || echo 0
}

# Function to get system memory info
get_memory_info() {
    free -m | awk 'NR==2{printf "%.1f %.1f %.1f", $3*100/$2, $3/1024, $2/1024}'
}

# Function to get GPU info
get_gpu_info() {
    if command -v nvidia-smi &> /dev/null; then
        nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits | head -1
    else
        echo "N/A,N/A,N/A,N/A"
    fi
}

# Function to get VS Code process count
get_vscode_processes() {
    pgrep -f "code" | wc -l
}

# Function to get CPU usage
get_cpu_usage() {
    top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
}

# Function to format memory size
format_memory() {
    local mb=$1
    if (( $(echo "$mb >= 1024" | bc -l) )); then
        echo "$(echo "scale=1; $mb/1024" | bc)GB"
    else
        echo "${mb}MB"
    fi
}

# Function to get color based on value and threshold
get_color() {
    local value=$1
    local warning=$2
    local critical=$3

    if (( $(echo "$value >= $critical" | bc -l) )); then
        echo "$RED"
    elif (( $(echo "$value >= $warning" | bc -l) )); then
        echo "$YELLOW"
    else
        echo "$GREEN"
    fi
}

# Main dashboard function
dashboard() {
    clear

    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local vscode_memory=$(get_vscode_memory)
    local memory_info=$(get_memory_info)
    local gpu_info=$(get_gpu_info)
    local vscode_procs=$(get_vscode_processes)
    local cpu_usage=$(get_cpu_usage)

    # Parse memory info
    read mem_percent mem_used_gb mem_total_gb <<< "$memory_info"

    # Parse GPU info
    IFS=',' read gpu_util gpu_mem_used gpu_mem_total gpu_temp <<< "$gpu_info"

    # Calculate swap usage
    local swap_info=$(free -m | awk 'NR==3{if($2>0) printf "%.1f", $3*100/$2; else print "0"}')

    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                    VS CODE PERFORMANCE DASHBOARD             ║${NC}"
    echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${BLUE}║${NC} Last Update: $timestamp                    ${BLUE}║${NC}"
    echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"

    # VS Code Memory
    local vscode_color=$(get_color "$vscode_memory" 2048 4096)
    echo -e "${BLUE}║${NC} VS Code Memory: ${vscode_color}$(format_memory $vscode_memory)${NC} (Processes: $vscode_procs)             ${BLUE}║${NC}"

    # System Memory
    local mem_color=$(get_color "$mem_percent" 80 90)
    echo -e "${BLUE}║${NC} System Memory:  ${mem_color}${mem_percent}%${NC} (${mem_used_gb}GB / ${mem_total_gb}GB)                ${BLUE}║${NC}"

    # Swap Usage
    local swap_color=$(get_color "$swap_info" 50 80)
    echo -e "${BLUE}║${NC} Swap Usage:     ${swap_color}${swap_info}%${NC}                                     ${BLUE}║${NC}"

    # CPU Usage
    local cpu_color=$(get_color "$cpu_usage" 70 90)
    echo -e "${BLUE}║${NC} CPU Usage:      ${cpu_color}${cpu_usage}%${NC}                                      ${BLUE}║${NC}"

    echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"

    # GPU Information
    if [[ "$gpu_util" != "N/A" ]]; then
        local gpu_util_color=$(get_color "$gpu_util" 70 90)
        local gpu_temp_color=$(get_color "$gpu_temp" 75 85)
        echo -e "${BLUE}║${NC} GPU Utilization: ${gpu_util_color}${gpu_util}%${NC}                                   ${BLUE}║${NC}"
        echo -e "${BLUE}║${NC} GPU Memory:     ${gpu_mem_used}MB / ${gpu_mem_total}MB                           ${BLUE}║${NC}"
        echo -e "${BLUE}║${NC} GPU Temperature: ${gpu_temp_color}${gpu_temp}°C${NC}                                  ${BLUE}║${NC}"
    else
        echo -e "${BLUE}║${NC} GPU:            ${YELLOW}Not Available${NC}                              ${BLUE}║${NC}"
    fi

    echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"

    # VS Code Processes
    echo -e "${BLUE}║${NC} Top VS Code Processes:                                    ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}                                                           ${BLUE}║${NC}"

    local process_count=0
    while IFS= read -r line && [[ $process_count -lt 3 ]]; do
        if [[ -n "$line" ]]; then
            local pid=$(echo "$line" | awk '{print $2}')
            local memory=$(echo "$line" | awk '{print $6/1024}')
            local command=$(echo "$line" | awk '{print $11}' | cut -c1-20)
            printf "${BLUE}║${NC} %-6s %8.0fMB %-20s                    ${BLUE}║${NC}\n" "$pid" "$memory" "$command"
            ((process_count++))
        fi
    done < <(ps aux | grep -E "code.*--" | grep -v grep | sort -k6 -nr)

    # Fill remaining lines if less than 3 processes
    while [[ $process_count -lt 3 ]]; do
        echo -e "${BLUE}║${NC}                                                           ${BLUE}║${NC}"
        ((process_count++))
    done

    echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"

    # Alerts
    local alerts=()

    if (( $(echo "$vscode_memory > 4096" | bc -l) )); then
        alerts+=("🚨 VS Code memory critical (>4GB)")
    elif (( $(echo "$vscode_memory > 2048" | bc -l) )); then
        alerts+=("⚠️  VS Code memory high (>2GB)")
    fi

    if (( $(echo "$mem_percent > 90" | bc -l) )); then
        alerts+=("🚨 System memory critical (>90%)")
    elif (( $(echo "$mem_percent > 80" | bc -l) )); then
        alerts+=("⚠️  System memory high (>80%)")
    fi

    if [[ "$gpu_temp" != "N/A" ]] && (( $(echo "$gpu_temp > 85" | bc -l) )); then
        alerts+=("🌡️  GPU temperature high (${gpu_temp}°C)")
    fi

    if (( $(echo "$swap_info > 50" | bc -l) )); then
        alerts+=("💾 High swap usage (${swap_info}%)")
    fi

    if [[ ${#alerts[@]} -eq 0 ]]; then
        echo -e "${BLUE}║${NC} Status: ${GREEN}All systems normal${NC}                               ${BLUE}║${NC}"
    else
        echo -e "${BLUE}║${NC} Alerts:                                                   ${BLUE}║${NC}"
        for alert in "${alerts[@]}"; do
            printf "${BLUE}║${NC} %-55s ${BLUE}║${NC}\n" "$alert"
        done
    fi

    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}💡 Commands: 'q' to quit, 'c' to clear history, 'r' to reset VS Code${NC}"
}

# Handle user input
handle_input() {
    read -t 0.1 -n 1 key 2>/dev/null || true
    case "$key" in
        q|Q)
            echo -e "\n${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        c|C)
            clear
            ;;
        r|R)
            echo -e "\n${YELLOW}Restarting VS Code...${NC}"
            pkill -f code || true
            sleep 2
            code &
            ;;
    esac
}

# Main loop
echo -e "${BLUE}Starting VS Code Performance Dashboard...${NC}"
echo -e "${CYAN}Press 'q' to quit${NC}"
sleep 2

while true; do
    dashboard
    handle_input
    sleep 2
done
```

## Configuration Examples

### 1. Optimized VS Code Settings

```json
{
  "// Performance Optimizations": "Core settings for better performance",
  "terminal.integrated.gpuAcceleration": "off",
  "workbench.list.smoothScrolling": false,
  "window.titleBarStyle": "native",
  "editor.semanticHighlighting.enabled": false,
  "editor.bracketPairColorization.enabled": false,
  "editor.guides.bracketPairs": false,
  "editor.minimap.enabled": false,
  "breadcrumbs.enabled": false,

  "// Memory Management": "Reduce memory consumption",
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/**": true,
    "**/dist/**": true,
    "**/build/**": true,
    "**/.venv/**": true,
    "**/venv/**": true,
    "**/target/**": true,
    "**/.next/**": true,
    "**/coverage/**": true,
    "**/.nyc_output/**": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.venv": true,
    "**/venv": true,
    "**/target": true,
    "**/.next": true,
    "**/coverage": true
  },

  "// Git Optimizations": "Reduce Git-related overhead",
  "git.autofetch": false,
  "git.autoRepositoryDetection": false,
  "scm.diffDecorations": "none",

  "// TypeScript Optimizations": "Improve TS performance",
  "typescript.tsserver.maxTsServerMemory": 3072,
  "typescript.preferences.includePackageJsonAutoImports": "off",
  "typescript.suggest.autoImports": false,
  "typescript.updateImportsOnFileMove.enabled": "never",

  "// Editor Optimizations": "Reduce editor overhead",
  "editor.quickSuggestions": {
    "other": false,
    "comments": false,
    "strings": false
  },
  "editor.parameterHints.enabled": false,
  "editor.hover.delay": 1000,
  "editor.lightbulb.enabled": false,
  "editor.codeLens": false,
  "editor.wordBasedSuggestions": false,

  "// Extension Management": "Control extension behavior",
  "extensions.autoUpdate": false,
  "extensions.autoCheckUpdates": false,

  "// Telemetry": "Disable telemetry for better performance",
  "telemetry.telemetryLevel": "off",
  "update.mode": "manual",

  "// GitHub Copilot Optimizations": "Optimize Copilot usage",
  "github.copilot.enable": {
    "*": true,
    "yaml": false,
    "plaintext": false,
    "markdown": false
  },

  "// Workbench Optimizations": "UI performance improvements",
  "workbench.iconTheme": null,
  "workbench.productIconTheme": "Default",
  "workbench.tree.indent": 8,
  "workbench.tree.renderIndentGuides": "none",

  "// Debug Console": "Limit debug output",
  "debug.console.fontSize": 12,
  "debug.console.lineHeight": 16
}
```

### 2. Environment Configuration

```bash
# ~/.bashrc additions for VS Code optimization

# Node.js memory optimization
export VSCODE_NODE_OPTIONS="--max-old-space-size=3072 --max-semi-space-size=128"

# Electron optimizations
export ELECTRON_OZONE_PLATFORM_HINT=x11
export ELECTRON_NO_ATTACH_CONSOLE=1
export ELECTRON_DISABLE_SECURITY_WARNINGS=true

# GPU configuration
export __GL_SYNC_TO_VBLANK=0
export __GL_THREADED_OPTIMIZATIONS=1

# VS Code aliases
alias code-clean='rm -rf ~/.config/Code/CachedData/* && rm -rf ~/.config/Code/logs/*'
alias code-reset='pkill -f code; sleep 2; code-clean; code'
alias code-monitor='watch -n 5 "ps aux | grep code | head -10"'
alias code-memory='smem -t -k | grep code'
alias code-gpu='watch -n 2 nvidia-smi'

# Functions for VS Code management
vscode-session-info() {
    echo "=== VS Code Session Information ==="
    echo "Processes: $(pgrep -f code | wc -l)"
    echo "Memory Usage: $(ps -o pid,rss,comm -C code 2>/dev/null | awk 'NR>1 {sum+=$2} END {print sum/1024}') MB"
    echo "Uptime: $(ps -o etime= -p $(pgrep -f "code.*--type=zygote" | head -1) 2>/dev/null | xargs)"
    echo "Extensions: $(code --list-extensions | wc -l)"
}

vscode-optimize-session() {
    echo "Optimizing VS Code session..."

    # Clear caches
    code-clean

    # Restart language servers
    code --command "typescript.restartTsServer"
    code --command "python.restartLanguageServer"

    echo "Optimization complete"
}
```

### 3. Systemd Service for Monitoring

```ini
# ~/.config/systemd/user/vscode-monitor.service
[Unit]
Description=VS Code Performance Monitor
After=graphical-session.target

[Service]
Type=simple
ExecStart=%h/.local/bin/vscode-memory-monitor.sh
Restart=always
RestartSec=30
Environment=DISPLAY=:0

[Install]
WantedBy=default.target
```

### 4. GPU-Specific Launch Scripts

```bash
#!/bin/bash
# ~/.local/bin/vscode-wayland
# Launch VS Code optimized for Wayland

export ELECTRON_OZONE_PLATFORM_HINT=wayland
export VSCODE_NODE_OPTIONS="--max-old-space-size=3072"

exec code \
    --enable-features=UseOzonePlatform,WaylandWindowDecorations \
    --ozone-platform=wayland \
    "$@"
```

```bash
#!/bin/bash
# ~/.local/bin/vscode-x11
# Launch VS Code optimized for X11

export ELECTRON_OZONE_PLATFORM_HINT=x11
export VSCODE_NODE_OPTIONS="--max-old-space-size=3072"

exec code \
    --use-gl=desktop \
    --disable-features=VizDisplayCompositor \
    "$@"
```

```bash
#!/bin/bash
# ~/.local/bin/vscode-nvidia-offload
# Launch VS Code with NVIDIA GPU offloading

export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia
export ELECTRON_OZONE_PLATFORM_HINT=x11
export VSCODE_NODE_OPTIONS="--max-old-space-size=4096"

exec code \
    --use-gl=desktop \
    --enable-gpu-rasterization \
    "$@"
```

## Automation and Maintenance

### 1. Daily Maintenance Cron Job

```bash
#!/bin/bash
# ~/.local/bin/vscode-daily-maintenance.sh

# Run daily at 6 AM
# Add to crontab: 0 6 * * * ~/.local/bin/vscode-daily-maintenance.sh

LOG_FILE="$HOME/.local/share/vscode-maintenance.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" >> "$LOG_FILE"
}

log "Starting daily maintenance"

# Clear old logs (keep 30 days)
find ~/.config/Code/logs -name "*.log" -mtime +30 -delete
log "Cleared old logs"

# Vacuum SQLite databases
find ~/.config/Code -name "*.vscdb" -exec sqlite3 {} "VACUUM;" \;
log "Vacuumed SQLite databases"

# Clear excessive cache if over 1GB
CACHE_SIZE=$(du -sm ~/.config/Code/CachedData 2>/dev/null | cut -f1)
if [[ $CACHE_SIZE -gt 1024 ]]; then
    rm -rf ~/.config/Code/CachedData/*
    log "Cleared cache (was ${CACHE_SIZE}MB)"
fi

# Update extensions (if enabled)
if [[ -f ~/.config/Code/User/settings.json ]] && ! grep -q '"extensions.autoUpdate": false' ~/.config/Code/User/settings.json; then
    code --update-extensions 2>/dev/null
    log "Updated extensions"
fi

log "Daily maintenance completed"
```

### 2. Performance Alert Script

```bash
#!/bin/bash
# ~/.local/bin/vscode-performance-alert.sh

MEMORY_THRESHOLD=4096  # MB
CPU_THRESHOLD=80       # Percentage
TEMP_THRESHOLD=85      # Celsius

check_performance() {
    # Check VS Code memory
    VSCODE_MEMORY=$(ps -o pid,rss,comm -C code 2>/dev/null | awk 'NR>1 {sum+=$2} END {print sum/1024}')

    if [[ -n "$VSCODE_MEMORY" ]] && (( $(echo "$VSCODE_MEMORY > $MEMORY_THRESHOLD" | bc -l) )); then
        notify-send "VS Code Performance Alert" \
            "Memory usage critical: ${VSCODE_MEMORY}MB\nConsider restarting VS Code" \
            --urgency=critical
    fi

    # Check GPU temperature
    if command -v nvidia-smi &> /dev/null; then
        GPU_TEMP=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits)
        if [[ -n "$GPU_TEMP" ]] && (( $(echo "$GPU_TEMP > $TEMP_THRESHOLD" | bc -l) )); then
            notify-send "GPU Temperature Alert" \
                "GPU temperature: ${GPU_TEMP}°C\nConsider reducing workload" \
                --urgency=critical
        fi
    fi
}

# Run check
check_performance
```

These examples and scripts provide a comprehensive toolkit for optimizing and monitoring VS Code performance on Linux with NVIDIA GPUs. They can be customized based on specific hardware configurations and usage patterns.
