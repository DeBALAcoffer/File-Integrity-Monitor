# FIM - File Integrity Monitor

A Python-based security tool that monitors files and directories for unauthorized changes using SHA-256 hash comparison.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Library)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

FIM (File Integrity Monitor) is a command-line security tool that detects unauthorized modifications, deletions, or additions to files in a monitored directory. It works by creating a baseline of file hashes and comparing current file states against this baseline to identify tampering.

This type of tool is commonly used in enterprise security operations to detect malware infections, unauthorized system changes, and data integrity violations.

## Features

- **Hash-Based Detection**: Uses SHA-256 cryptographic hashing to detect even single-byte file modifications
- **Comprehensive Monitoring**: Detects modified, deleted, and newly added files
- **Baseline Management**: Save and load baselines for ongoing integrity checks
- **Detailed Reporting**: Generates timestamped reports with hash comparisons
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Zero Dependencies**: Uses only Python standard library (no `pip install` required)
- **Automation-Friendly**: Easily scriptable for scheduled security audits

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12+ |
| Hashing | `hashlib` (SHA-256) |
| File System | `os.walk()` |
| Storage | Plain text (sha256sum compatible format) |
| CLI | `argparse` |
| Timestamps | `datetime` |




Basic Examples
```bash
# Create a baseline of a directory
python main.py --save-baseline C:/Windows/System32 --output system32_baseline.txt

# Check for changes against the baseline
python main.py --check C:/Windows/System32 --baseline system32_baseline.txt

# Monitor current directory
python main.py --save-baseline . --output current_baseline.txt
python main.py --check . --baseline current_baseline.txt
```

Quick Test Commands
1)Windows PowerShell 
```bash
# Step 1: Create test environment
mkdir C:\FIM_Demo -Force
Set-Content C:\FIM_Demo\config.txt "server_port=8080"
Set-Content C:\FIM_Demo\passwords.txt "admin_credentials"
Set-Content C:\FIM_Demo\logs.txt "2026-10-04 system started"

# Step 2: Navigate to FIM folder and create baseline
cd E:\CyberSecurity\FIM
python main.py --save-baseline C:\FIM_Demo --output demo_baseline.txt

# Step 3: Simulate an attacker modifying a file
Set-Content C:\FIM_Demo\passwords.txt "HACKED_CREDENTIALS"

# Step 4: Simulate malware being dropped
Set-Content C:\FIM_Demo\backdoor.exe "malicious_payload"

# Step 5: Simulate log deletion (covering tracks)
Remove-Item C:\FIM_Demo\logs.txt

# Step 6: Run integrity check - tool detects all changes!
python main.py --check C:\FIM_Demo --baseline demo_baseline.txt
```

One-Liner Quick Test (Windows PowerShell)
```bash
# Complete test in a single command block
mkdir C:\FIM_Quick -Force; Set-Content C:\FIM_Quick\test.txt "original"; cd E:\CyberSecurity\FIM; python main.py --save-baseline C:\FIM_Quick --output quick.txt; Set-Content C:\FIM_Quick\test.txt "modified"; python main.py --check C:\FIM_Quick --baseline quick.txt
```

2)Linux
```bash
# Step 1: Create test environment
mkdir -p /tmp/FIM_Demo
echo "server_port=8080" > /tmp/FIM_Demo/config.txt
echo "admin_credentials" > /tmp/FIM_Demo/passwords.txt
echo "2026-10-04 system started" > /tmp/FIM_Demo/logs.txt

# Step 2: Navigate to FIM folder and create baseline
cd ~/FIM
python3 main.py --save-baseline /tmp/FIM_Demo --output demo_baseline.txt

# Step 3: Simulate an attacker modifying a file
echo "HACKED_CREDENTIALS" > /tmp/FIM_Demo/passwords.txt

# Step 4: Simulate malware being dropped
echo "malicious_payload" > /tmp/FIM_Demo/backdoor.exe

# Step 5: Simulate log deletion (covering tracks)
rm /tmp/FIM_Demo/logs.txt

# Step 6: Run integrity check - tool detects all changes!
python3 main.py --check /tmp/FIM_Demo --baseline demo_baseline.txt
```

One-Liner Quick Test (Linux)
```bash
# Complete test in a single command block
mkdir -p /tmp/FIM_Quick && echo "original" > /tmp/FIM_Quick/test.txt && python3 main.py --save-baseline /tmp/FIM_Quick --output quick.txt && echo "modified" > /tmp/FIM_Quick/test.txt && python3 main.py --check /tmp/FIM_Quick --baseline quick.txt
```


How It Works
Technical Flow
```
1. BASELINE CREATION (--save-baseline)
   ┌─────────────────────────────────────────┐
   │ Directory → os.walk() → List all files  │
   │ For each file:                          │
   │   - Read in 4KB chunks                  │
   │   - Compute SHA-256 hash                │
   │   - Store: hash + filepath              │
   └─────────────────────────────────────────┘
                    ↓
   Saved to baseline.txt (sha256sum format)

2. INTEGRITY CHECK (--check)
   ┌─────────────────────────────────────────┐
   │ Load baseline hashes                    │
   │ Scan current directory                  │
   │ Compare:                                │
   │   - Missing files → DELETED             │
   │   - Changed hash → MODIFIED             │
   │   - New file → NEW FILE                 │
   └─────────────────────────────────────────┘
                    ↓
   Generate timestamped report
```
