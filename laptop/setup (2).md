# Laptop setup

---

## 1. SSH config

Create or edit `~/.ssh/config` (Linux/macOS) or `C:\Users\<you>\.ssh\config` (Windows):

See [ssh_config.example](ssh_config.example) — copy it and replace the placeholders with your values.

The `ProxyJump` directive means `ssh Ubuntu_PC` automatically bounces through the router. The Python script relies on this — do not skip it.

---

## 2. Python script

Copy `wake_pc.py` (Linux/macOS) or `wake_pc_windows.py` (Windows) to a convenient location, e.g. `~/.ssh/`.

Edit the configuration block at the top of the script:

```python
ROUTER_USER_IP = "root@<your_router_ip>"
TARGET_PC_IP   = "<your_pc_ip>"
TARGET_PC_NAME = "Ubuntu_PC"   # must match option 'name' in etherwake config
SSH_HOST_ALIAS = "Ubuntu_PC"   # must match Host entry in ~/.ssh/config
```

Run:

```bash
python wake_pc.py           # wake and connect
python wake_pc.py --check   # check if PC is awake
python wake_pc.py --wake-only  # wake without connecting
```

**Windows — add a PowerShell alias:**

Add to your PowerShell profile (`notepad $PROFILE`):

```powershell
function wakepc { python $HOME\.ssh\wake_pc.py @args }
```

Then `wakepc` works from any PowerShell window.

---

## Verification checklist

- [ ] `ssh router` connects without a password
- [ ] `ssh Ubuntu_PC` connects without a password (ProxyJump fires automatically)
- [ ] `python wake_pc.py --check` returns correct status
- [ ] Full flow: PC suspended → `python wake_pc.py` → PC wakes → SSH session opens
