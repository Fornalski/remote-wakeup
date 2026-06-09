# remote-wakeup

Wake your suspended Linux PC from anywhere and drop straight into an SSH session — one command, no manual steps.

Built on OpenWrt (router as relay), WoL via `etherwake`, and a small Python client script. No always-on middleman device required.

---

## How it works

```
Laptop ──SSH──▶ OpenWrt router ──WoL packet──▶ Suspended PC
Laptop ══SSH (ProxyJump through router) ══════▶ PC (now awake)
```

The Python script on your laptop handles the full sequence: fires WoL via the router, polls until SSH responds, then hands off the terminal.

---

## Requirements

| Component | What you need |
|---|---|
| Router | OpenWrt 24.10.0+ with `etherwake` installed |
| PC | Ubuntu (tested), any Linux with `nmcli` and `ethtool` |
| Laptop | Python 3.10+, OpenSSH client |
| Network | PC on a static DHCP lease; router reachable from outside |

---

## Setup

Follow the guides in order — each step is independently testable before moving on.

1. [OpenWrt setup](openwrt/setup.md) — static DHCP lease, etherwake, SSH key auth
2. [Ubuntu PC setup](ubuntu-pc/setup.md) — BIOS, WoL persistence via nmcli, SSH key
3. [Laptop setup](laptop/setup.md) — SSH config with ProxyJump, Python script

---

## Usage

```bash
python wake_pc.py            # wake PC and connect
python wake_pc.py --check    # check if PC is awake
python wake_pc.py --wake-only  # wake without connecting
```

On Windows, add to your PowerShell profile for a single command:

```powershell
function wakepc { python $HOME\.ssh\wake_pc.py @args }
```

---

## Repository structure

```
remote-wakeup/
├── docs/
│   └── architecture.md        network map, IP assignments
├── openwrt/
│   ├── setup.md               router configuration guide
│   └── etherwake.conf.example etherwake config template
├── ubuntu-pc/
│   └── setup.md               BIOS, ethtool, nmcli guide
└── laptop/
    ├── laptop_setup.md        Laptop confg
    ├── wake_pc.py             client script
    ├── wake_pc_windows.py     Windows-compatible variant
    └── ssh_config.example     ProxyJump config template
```

---

## Notes

- Tested on MSI B450 Gaming Plus with Realtek NIC — BIOS steps documented in [ubuntu-pc/setup.md](ubuntu-pc/setup.md)
- WoL flag persists across suspend via `nmcli` — no systemd hook required on Ubuntu with NetworkManager
- This is Stage 1 of a larger homelab project. Stage 2 adds a WireGuard VPN on a Raspberry Pi.
