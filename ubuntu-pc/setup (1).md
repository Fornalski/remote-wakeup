# Ubuntu PC setup

---

## 1. BIOS configuration

Tested on MSI B450 Gaming Plus. Steps are the same across all B450 board variants.

Enter BIOS and switch to Advanced Mode.

**Disable ErP:**
```
Settings → Advanced → Power Management Setup → ErP Ready → Disabled
```
ErP cuts standby power to the NIC. It must be disabled or the NIC cannot receive the WoL packet.

**Enable resume by PCI-E device:**
```
Settings → Advanced → Wake Up Configuration → Resume By PCI-E Device → Enabled
```
This allows the Realtek NIC (connected via PCI-E) to wake the system.

Save and exit (F10).

**Verification:** after suspending the PC, check that the ethernet port indicator light on the back of the machine is still lit. If it is dark, the NIC has no standby power and WoL cannot work.

---

## 2. Enable WoL on the network adapter

Find your ethernet adapter name:

```bash
ip link
```

Look for the adapter with status `UP` — it will look something like `enp34s0`.

Enable WoL magic packet mode:

```bash
sudo ethtool -s <your_adapter_name> wol g
```

Verify:

```bash
sudo ethtool <your_adapter_name> | grep Wake
```

Expected output:

```
Supports Wake-on: pumbg
Wake-on: g
```

---

## 3. Persist WoL across reboots and resumes

The `ethtool` flag resets on reboot. Use `nmcli` to make it permanent via NetworkManager:

Find your connection name:

```bash
nmcli connection show
```

Look for your ethernet connection, e.g. `netplan-enp34s0`.

Apply persistent WoL setting:

```bash
sudo nmcli connection modify "netplan-enp34s0" 802-3-ethernet.wake-on-lan magic
```

Reboot and verify the flag survived:

```bash
sudo ethtool <your_adapter_name> | grep Wake
```

You should still see `Wake-on: g`.

---

## 4. SSH key setup

On your laptop, copy your public key to the PC:

```bash
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```

Set correct permissions (SSH will refuse keys with wrong permissions):

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## Verification checklist

- [ ] Ethernet port light is on when PC is suspended
- [ ] `ethtool | grep Wake` shows `Wake-on: g` after a reboot
- [ ] Router's `etherwake start Ubuntu_PC` wakes the PC from suspend
- [ ] SSH from laptop works without a password prompt
