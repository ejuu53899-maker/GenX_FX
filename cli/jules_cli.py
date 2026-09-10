#!/usr/bin/env python3
"""
Jules CLI - Command line interface for Jules Agent & Workspace Orchestration.
Version: 1.0.0
"""

import sys
import os
import argparse
import subprocess

CLI_VERSION = "1.0.0"
WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR", "/app")
ATTACHMENTS_DIR = "/tmp/file_attachments/Workspace-Monorepo-main"

def check_status():
    print(f"=== Jules CLI v{CLI_VERSION} Status ===")
    print(f"Workspace Directory: {WORKSPACE_DIR}")
    print(f"Attachments Source: {ATTACHMENTS_DIR} (Exists: {os.path.exists(ATTACHMENTS_DIR)})")

    subdirs = ["AgentBrain", "DomainController", "MQL5-Google-Onedrive", "OS-Twin", "OS-Twin-setup", "scripts", "src"]
    print("\n--- Subproject Status ---")
    for d in subdirs:
        path = os.path.join(WORKSPACE_DIR, d)
        exists = os.path.exists(path)
        print(f"  [{'✓' if exists else '✗'}] {d}: {'Available' if exists else 'Missing'}")

    print("\n--- Git Remote Configuration ---")
    try:
        remotes = subprocess.check_output(["git", "remote", "-v"], cwd=WORKSPACE_DIR, text=True)
        print(remotes.strip())
    except Exception as e:
        print(f"Error fetching git remotes: {e}")

def run_sync():
    print("=== Continuous Workspace Syncing ===")
    sync_script = os.path.join(WORKSPACE_DIR, "scripts", "sync_workspace.sh")
    if not os.path.exists(sync_script):
        print(f"Error: Sync script not found at {sync_script}")
        sys.exit(1)

    try:
        res = subprocess.run(["bash", sync_script], cwd=WORKSPACE_DIR, check=True)
        print("Workspace sync completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Workspace sync failed: {e}")
        sys.exit(e.returncode)

def plugins_info():
    print("=== Jules Plugins & Integrations ===")
    print("Registered Plugins / IDE Links:")
    print("  - Git4Idea Plugin Repository: git@gitlab.com:genxfx/vscode-powershell.git")
    print("  - JetBrains Checkout Link: jetbrains://idea/checkout/git?idea.required.plugins.id=Git4Idea&checkout.repo=git%40gitlab.com%3Agenxfx%2Fvscode-powershell.git")
    print("  - VS Code Extensions: ms-vscode.powershell, Git4Idea, ms-python.python")

def main():
    parser = argparse.ArgumentParser(description="Jules CLI for Workspace Management and Agent Tools")
    parser.add_argument("--version", action="version", version=f"Jules CLI v{CLI_VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    status_parser = subparsers.add_parser("status", help="Show workspace and agent status")
    sync_parser = subparsers.add_parser("sync", help="Run workspace folder sync")
    plugins_parser = subparsers.add_parser("plugins", help="List registered plugins and links")

    args = parser.parse_args()

    if args.command == "status" or args.command is None:
        check_status()
    elif args.command == "sync":
        run_sync()
    elif args.command == "plugins":
        plugins_info()

if __name__ == "__main__":
    main()
