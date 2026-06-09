#!/usr/bin/env python3
"""
wake_pc.py — Wake your suspended Linux PC and connect via SSH.
Linux / macOS version. Uses os.execvp for clean terminal handoff.

Usage:
    python wake_pc.py               wake PC and connect
    python wake_pc.py --check       check if PC is awake
    python wake_pc.py --wake-only   wake without connecting
"""

import argparse
import os
import sys
import subprocess
import socket
import time

# --- Configuration ---
ROUTER_USER_IP = "root@10.10.10.1"   # router SSH address
TARGET_PC_IP   = "10.10.10.2"        # PC local IP (static DHCP lease)
TARGET_PC_NAME = "Ubuntu_PC"         # must match option 'name' in /etc/config/etherwake
SSH_HOST_ALIAS = "Ubuntu_PC"         # must match Host entry in ~/.ssh/config


def check_ssh_port(ip, port=22, timeout=1.0):
    """Return True if the SSH port is open and accepting connections."""
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False


def wake_pc():
    """Fire the WoL command via the router."""
    print("Sending Wake-on-LAN packet via router...")
    cmd = ["ssh", ROUTER_USER_IP, f"/etc/init.d/etherwake start {TARGET_PC_NAME}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error triggering wake command: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)


def wait_for_boot(ip, port=22, max_attempts=40, wait_seconds=1):
    """Poll the PC until SSH responds or the attempt limit is reached."""
    print(f"Waiting for {ip} to come online...", end="", flush=True)
    for _ in range(max_attempts):
        if check_ssh_port(ip, port):
            print("\nPC is awake and ready.")
            return True
        print(".", end="", flush=True)
        time.sleep(wait_seconds)
    print("\nTimeout: PC did not come online.", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Wake the home PC and connect via SSH."
    )
    parser.add_argument(
        "--wake-only", action="store_true",
        help="Wake the PC and exit without connecting."
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Check if the PC is currently awake and exit."
    )
    args = parser.parse_args()

    if args.check:
        if check_ssh_port(TARGET_PC_IP):
            print("Status: AWAKE")
            sys.exit(0)
        else:
            print("Status: ASLEEP")
            sys.exit(1)

    if check_ssh_port(TARGET_PC_IP):
        print("PC is already awake.")
    else:
        wake_pc()
        if not wait_for_boot(TARGET_PC_IP):
            sys.exit(1)

    if args.wake_only:
        print("Done. (--wake-only, not connecting)")
        sys.exit(0)

    print(f"Connecting to {SSH_HOST_ALIAS}...")
    try:
        # Replace this process with SSH entirely — clean terminal handoff
        os.execvp("ssh", ["ssh", SSH_HOST_ALIAS])
    except FileNotFoundError:
        print("Error: 'ssh' not found on this system.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
