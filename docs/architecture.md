# Architecture

## Network topology

```
Internet
    │
    ▼
OpenWrt router   10.10.10.1   (gateway, WoL relay, SSH bastion)
    │
    ├── Ubuntu PC   10.10.10.2   (target, suspended when idle)
    └── Raspberry Pi 10.10.10.3  (reserved — Stage 2, WireGuard VPN)
```

Subnet: `10.10.10.0/29` — 6 usable addresses, sufficient for this setup with room to grow.

## IP assignments

| Device | IP | How assigned |
|---|---|---|
| OpenWrt router | 10.10.10.1 | Static (router default) |
| Ubuntu PC | 10.10.10.2 | Static DHCP lease by MAC |
| Raspberry Pi | 10.10.10.3 | Reserved for Stage 2 |

## Connection flow

```
1. Laptop SSHes into router (bastion)
2. Router sends etherwake magic packet to PC's MAC on br-lan
3. Laptop polls PC's port 22 until it responds
4. Laptop SSHes into PC via ProxyJump through router
```

## Design decisions

**Router as relay, not Raspberry Pi**
The router is always-on by design and already sits between the internet and the LAN. Using it as the WoL relay eliminates the need for an extra always-on device and simplifies the network topology.

**etherwake broadcast mode enabled**
`broadcast on` in the etherwake config sends to `255.255.255.255`. More reliable than unicast in this subnet since no ARP entry exists for a sleeping machine.

**WoL persistence via nmcli, not systemd hook**
On Ubuntu with NetworkManager, `nmcli connection modify ... 802-3-ethernet.wake-on-lan magic` persists the WoL flag across reboots and resumes without a custom systemd sleep hook. Simpler and less fragile.

**ProxyJump in ~/.ssh/config**
The Python script calls `ssh Ubuntu_PC` — ProxyJump through the router is handled transparently by the SSH config. The script has no router-specific logic for the final connection step.

**os.execvp on Linux/macOS, subprocess.run on Windows**
`execvp` replaces the Python process entirely, giving SSH full control of the terminal (signals, resize events, etc.). Windows does not support `execvp` semantics, so the Windows variant uses `subprocess.run` with no output capture, which binds SSH directly to the calling terminal.
