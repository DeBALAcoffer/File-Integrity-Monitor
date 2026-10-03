#!/usr/bin/env python3
"""
File Integrity Monitor (FIM)
Monitors files for unauthorized changes using hash comparison
Built by DeBALA
"""

import os
import hashlib
import argparse
from datetime import datetime

# ANSI Color Codes
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[1;32m"
COLOR_YELLOW = "\033[1;33m"
COLOR_CYAN = "\033[1;36m"
COLOR_RED = "\033[1;31m"

BANNER = r"""

 ███████████    █████    ██████   ██████
░░███░░░░░░█   ░░███    ░░██████ ██████ 
 ░███   █ ░     ░███     ░███░█████░███ 
 ░███████       ░███     ░███░░███ ░███ 
 ░███░░░█       ░███     ░███ ░░░  ░███ 
 ░███  ░        ░███     ░███      ░███ 
 █████          █████    █████     █████
░░░░░          ░░░░░    ░░░░░     ░░░░░ 

        by DeBALA
"""


def calculate_hash(filepath):
    """Calculate SHA-256 hash of a file."""
    try:
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return None


def scan_directory(directory):
    """Scan directory and return dict of {filepath: hash}."""
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            if file_hash is not None:
                file_hashes[filepath] = file_hash
    return file_hashes


def save_baseline(directory, baseline_file):
    """Save current file hashes as baseline (plain text format)."""
    print(f"{COLOR_CYAN}[*] Scanning {directory}...{COLOR_RESET}")
    current_hashes = scan_directory(directory)

    with open(baseline_file, 'w') as f:
        for filepath, file_hash in current_hashes.items():
            f.write(f"{file_hash}  {filepath}\n")

    print(f"{COLOR_GREEN}[+] Baseline saved: {len(current_hashes)} files recorded{COLOR_RESET}")
    print(f"{COLOR_GREEN}[+] Baseline file: {baseline_file}{COLOR_RESET}")


def load_baseline(baseline_file):
    """Load baseline from plain text file."""
    baseline_hashes = {}
    with open(baseline_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('  ', 1)
            if len(parts) == 2:
                file_hash, filepath = parts
                baseline_hashes[filepath] = file_hash
    return baseline_hashes


def check_integrity(directory, baseline_file):
    """Compare current files against baseline."""
    if not os.path.exists(baseline_file):
        print(f"{COLOR_RED}[!] Error: Baseline file not found: {baseline_file}{COLOR_RESET}")
        print(f"{COLOR_YELLOW}[*] Run with --save-baseline first{COLOR_RESET}")
        return

    print(f"{COLOR_CYAN}[*] Loading baseline from {baseline_file}...{COLOR_RESET}")
    baseline_hashes = load_baseline(baseline_file)

    print(f"{COLOR_CYAN}[*] Scanning {directory}...{COLOR_RESET}")
    current_hashes = scan_directory(directory)

    modified_count = 0
    deleted_count = 0
    new_count = 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{'='*60}")
    print(f"{COLOR_YELLOW}Integrity Check Report - {timestamp}{COLOR_RESET}")
    print(f"{'='*60}\n")

    for filepath, old_hash in baseline_hashes.items():
        if filepath not in current_hashes:
            print(f"{COLOR_RED}[!] DELETED:  {filepath}{COLOR_RESET}")
            deleted_count += 1
        elif current_hashes[filepath] != old_hash:
            print(f"{COLOR_RED}[!] MODIFIED: {filepath}{COLOR_RESET}")
            print(f"    Old hash: {old_hash[:16]}...")
            print(f"    New hash: {current_hashes[filepath][:16]}...")
            modified_count += 1

    for filepath in current_hashes:
        if filepath not in baseline_hashes:
            print(f"{COLOR_GREEN}[+] NEW FILE: {filepath}{COLOR_RESET}")
            new_count += 1

    print(f"\n{'='*60}")
    print(f"{COLOR_YELLOW}Summary:{COLOR_RESET}")
    print(f"  Total files in baseline: {len(baseline_hashes)}")
    print(f"  Total files scanned:     {len(current_hashes)}")
    print(f"  Modified files:          {modified_count}")
    print(f"  Deleted files:           {deleted_count}")
    print(f"  New files:               {new_count}")
    print(f"{'='*60}")

    if modified_count == 0 and deleted_count == 0 and new_count == 0:
        print(f"{COLOR_GREEN}[✓] No changes detected. All files intact.{COLOR_RESET}")
    else:
        print(f"\n{COLOR_RED}[!] WARNING: Changes detected! Review above files.{COLOR_RESET}")


def main():
    print(f"{COLOR_CYAN}{BANNER}{COLOR_RESET}")
    
    parser = argparse.ArgumentParser(
        description="File Integrity Monitor - Detect unauthorized file changes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  1. Create baseline of a directory:
     python main.py --save-baseline C:/Users/YourName/Documents --output baseline.txt

  2. Check for changes:
     python main.py --check C:/Users/YourName/Documents --baseline baseline.txt

  3. Monitor current directory:
     python main.py --save-baseline . --output my_files.txt
     python main.py --check . --baseline my_files.txt
        """)

    parser.add_argument('--save-baseline', metavar='DIRECTORY',
                        help='Scan directory and save baseline')
    parser.add_argument('--check', metavar='DIRECTORY',
                        help='Check directory against baseline')
    parser.add_argument('--baseline', metavar='FILE',
                        help='Baseline file to use (default: baseline.txt)')
    parser.add_argument('--output', metavar='FILE',
                        help='Output file for baseline (default: baseline.txt)')

    args = parser.parse_args()

    if args.save_baseline:
        output_file = args.output or 'baseline.txt'
        save_baseline(args.save_baseline, output_file)
    elif args.check:
        baseline_file = args.baseline or 'baseline.txt'
        check_integrity(args.check, baseline_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()