# P-REC External v1.0.0 — Zero-Lag Match Recorder for TF2 64-Bit (Windows & Linux)

[![TF2 Architecture: 64-bit Native](https://img.shields.io/badge/TF2-64--bit%20Native-orange.svg)](https://github.com/Emieldev/P-REC-External)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg)](https://github.com/Emieldev/P-REC-External)
[![100% VAC-Safe](https://img.shields.io/badge/VAC-100%25%20Safe-brightgreen.svg)](https://github.com/Emieldev/P-REC-External)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

---

### 💡 Why This Exists (The Vibecoded Backstory)
> *"I got fed up with PeachREC microstutters making it unusable and causing start of round lag with many HUDs, and the original **P-REC not working** on modern 64-bit TF2 without `-insecure` (which Valve requires for unsigned plugins, blocking connection to VAC match servers). So I vibecoded this companion for myself to have zero game lag, zero warmup bloat, and total competitive league compliance."*

⚠️ **Player Responsibility Disclaimer:**
In all competitive leagues (ETF2L, RGL, ozfortress, AsiaFortress, etc.), **it remains the player's personal responsibility to ensure your POV demos are actively recording and saved**. While this software is architecturally **100% VAC-safe** (using official Source Engine RCON and Netcon loopback protocols with zero memory injection, zero DLL hooking, and zero modified game binaries), always verify your in-game developer console (`~`) confirmations, check your demo folder after matches, and test during scrims before major tournament fixtures!

---

### ⚡ Key Features
* **0 FPS Impact / Zero Lag:** Runs 100% externally out-of-process. Touches 0 HUD animations and 0 VGUI panels.
* **Zero Warmup Bloat:** Records strictly when the tournament countdown goes live.
* **100% VAC-Safe:** Connects via official engine loopback sockets. Zero DLL injection or memory hooks.
* **🛡️ Windows System Tray & Close-to-Tray:** Lives quietly in Hidden Pictograms with the TF2 **Supreme Soviet** icon. Crossing out ('X') the console minimizes to tray without interrupting recording. Single or double-click the tray icon to instantly toggle the console back.
* **📸 League Compliance Screenshots:** Takes mandatory in-game status screenshot randomly after 3 minutes of active tournament play (strict ETF2L Rule 2.1 compliance) plus scoreboard screenshot at match end.
* **🔄 Mid-Match Reconnect & Substitute Detection:** Automatically detects ongoing matches if you crash, rejoin, or substitute into a tournament server mid-game, resuming recording immediately.
* **🖥️ Desktop Shortcut & Startup:** Option to place a Desktop shortcut and auto-start silently on login.
* **🔍 Live Connection Diagnostics:** Click "Check Connection" in the tray at any time to verify communication.
* **Reassuring In-Game Console Messages:** Announces connection, active league, and recording start/stop in TF2 console (`~`).
* **Auto Profile Switching & Scrim Mode:** Auto-switches rulesets when match configs load; suppresses status screenshots and adds `_scrim` prefix during practice.
* **Multi-League Rulesets:** Dedicated compliance for **ETF2L** (Rule 2.1), **AsiaFortress**, **RGL** (1008.5), **ozfortress**, **Matcha.tf**, and **CLTF2** with intuitive 3-2-1-0 recording modes.
* **Auto-Healing RCON & serveme.tf Synergy:** Automatically synchronizes passwords and recovers instantly (<1ms) if you switch `rcon_password` in-game to execute server commands.
* **DemoMan Integration:** Automatically discovers DemoMan's active RCON password and TF2 path.
* **🎵 Authentic Tactile Audio Cues:** Uses classic original P-REC mechanical switch clicks directly in-game (`buttons/button9.wav` on start, `buttons/button14.wav` on stop, `buttons/bell1.wav` on bookmark) with zero annoying motherboard piezo buzzers and zero confusing player voice lines.
* **🐛 Report Issues Buttons & Commands:** Quick 1-click access to the GitHub issues tracker via console toolbar, system tray context menu, and in-game `prec_issue` command.
* **⚡ Ultra-Low CPU Engine:** Native Win32 Toolhelp snapshots inspect game state in < 0.5ms with zero background subprocess creation.

---

### 🚀 Steam Launch Options
Add this to the end of your Launch Options in Steam (TF2 Properties -> General):

```text
-usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
```
*(If you already run [DemoMan](https://github.com/DemomanApp/DemoMan), you already have this in Steam!)*

---

### 📥 Release Downloads
* **Windows (64-bit Standalone Executable):** [`prec64.exe`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/prec64.exe)
* **Linux (64-bit Standalone ELF Binary):** [`prec64`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/prec64)
* **Configuration File:** [`PREC_Settings.cfg`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/PREC_Settings.cfg)

📖 **Full Setup Guide & Documentation:** See [README.md](https://github.com/Emieldev/P-REC-External/blob/main/README.md).

---

### 🙏 Credits
* **Aethelred (Orange)** for the original [P-REC](https://github.com/Orange-TF2/p-rec).
* **peaches** for [PeachREC](https://github.com/peaches-tf2/PeachREC).
* **DemoMan** developers for the [DemoMan](https://github.com/DemomanApp/DemoMan) ecosystem.
* ETF2L, AsiaFortress, RGL.gg, ozfortress, Matcha.tf, and CLTF2.
