# P-REC External v1.0.2 — Zero-Lag Match Recorder for TF2 64-Bit (Windows & Linux)

[![TF2 Architecture: 64-bit Native](https://img.shields.io/badge/TF2-64--bit%20Native-orange.svg)](https://github.com/Emieldev/P-REC-External)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg)](https://github.com/Emieldev/P-REC-External)
[![100% VAC-Safe](https://img.shields.io/badge/VAC-100%25%20Safe-brightgreen.svg)](https://github.com/Emieldev/P-REC-External)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

---

### ⚡ What's New in v1.0.2
* **🔒 Strict Configuration Preservation:** On both first-time setup and subsequent self-updates, P-REC External strictly preserves all existing `.cfg` files (`PREC_Settings.cfg`, `Settings.cfg`, `autoexec.cfg`). It will never overwrite, edit, or inject changes into existing user configurations.
* **🛡️ Read-Only Runtime Config:** Runtime configuration parsing is now strictly read-only on existing files. DemoMan tokens or session passwords are held safely in memory without modifying the config file on disk.
* **🖥️ Desktop Shortcut Support:** Automatically creates or restores a desktop shortcut with the TF2 **Supreme Soviet** icon. Includes `prec_desktop_shortcut` config option and a System Tray shortcut button.
* **🛡️ Antivirus False Positive Resolution:** Autostart persistence uses standard Windows Registry keys (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`), full PE `VS_VERSION_INFO` metadata, and uncompressed `--noupx` binaries.
* **🔍 Tray Diagnostics & In-Game Announce:** "Check RCON / Connection" tray button with live confirmations sent directly into your TF2 developer console (`~`).
* **⚔️ Mid-Match Join Detection:** Instantly detects active match configs and tournament states (`mp_tournament 1`) even when joining mid-scrim.

---

### 🚀 Steam Launch Options (Choose One)
* **Option 1: RCON Mode (Recommended - identical to DemoMan):**
  ```text
  -usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
  ```
* **Option 2: Netcon Mode (Ultra-Short, 16 characters):**
  ```text
  -netconport 2121
  ```

---

### 📥 Release Downloads
* **Windows (64-bit Standalone Executable):** [`prec64.exe`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.2/prec64.exe)
* **Linux (64-bit Standalone ELF Binary):** [`prec64`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.2/prec64)
* **Configuration File:** [`PREC_Settings.cfg`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.2/PREC_Settings.cfg)

📖 **Full Setup Guide, League Instructions, and Documentation:** See the [README.md](https://github.com/Emieldev/P-REC-External/blob/main/README.md).

---

### 🙏 Credits
* **Aethelred (Orange)** for the original [P-REC](https://github.com/Orange-TF2/p-rec).
* **peaches** for [PeachREC](https://github.com/peaches-tf2/PeachREC).
* **DemoMan** developers for the [DemoMan](https://github.com/DemomanApp/DemoMan) ecosystem.
* ETF2L, AsiaFortress, RGL.gg, ozfortress, Matcha.tf, and CLTF2.
