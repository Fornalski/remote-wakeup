# OpenWrt setup

Tested on OpenWrt 24.10.0, Netgear router.

---

## 1. Static DHCP lease for the PC

In LuCI (web interface):

```
Network → DHCP and DNS → Static Leases → Add
```

Fill in:
- **Hostname** — e.g. `Ubuntu-PC`
- **MAC address** — your PC's ethernet MAC (find it with `ip link` on the PC, shown in green)
- **IP address** — e.g. `10.10.10.2`

Save and apply. The PC will always receive the same IP after this.

---

## 2. Install and configure etherwake

SSH into the router:

```bash
ssh root@10.10.10.1
```

Install:

```bash
opkg update
opkg install etherwake
```

Configure — create `/etc/config/etherwake` with the content from [etherwake.conf.example](etherwake.conf.example), replacing the placeholders with your values.

Test (PC must be suspended):

```bash
/etc/init.d/etherwake start Ubuntu_PC
```

If the PC wakes, the hardware and router side are confirmed working.

---

## 3. SSH key authentication

On your laptop, generate a key if you don't have one:

```bash
ssh-keygen -t ed25519 -C "your_comment"
```

Add the public key to the router in LuCI:

```
System → Administration → SSH Keys → paste your public key
```

Disable password authentication on the router (also in LuCI):

```
System → Administration → SSH Access
```

Set `PasswordAuth` to `off` after confirming key login works.

---

## Verification checklist

- [ ] PC always gets the same IP after reboot
- [ ] `etherwake start Ubuntu_PC` wakes the PC from suspend
- [ ] `ssh root@10.10.10.1` succeeds without a password prompt
