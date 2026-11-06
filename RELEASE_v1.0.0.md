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

### ⚡ Highlights & Key Features

* **Zero Game Lag / 0 FPS Impact:** Runs 100% externally out-of-process via engine loopback sockets. Touches 0 HUD animations and 0 VGUI panels.
* **100% VAC-Safe:** Connects via official Source engine RCON/Netcon. Zero memory injection, zero DLL hooking.
* **Zero Warmup Bloat:** Records strictly when the live tournament countdown begins.
* **🛡️ Windows System Tray & Close-to-Tray:** Sits quietly in Hidden Pictograms with the TF2 **Supreme Soviet** icon. Crossing out ('X') minimizes to tray without interrupting recording. Single or double-click toggles the console.
* **🐧 Linux Native Out-of-the-Box:** Includes a standalone 64-bit Linux ELF binary (`prec64`) with sub-millisecond `/proc` detection, multi-drive `libraryfolders.vdf` discovery, PipeWire/Pulse chimes, and `notify-send` desktop notifications.
* **📸 League Compliance Screenshots:** Automatically captures mandatory in-game status screenshots (`status; jpeg`) with player SteamIDs randomly after 3 minutes of play (ETF2L Rule 2.1 compliance) and snaps the match-end scoreboard.
* **🔄 Mid-Match Reconnect & Substitute Detection:** Automatically detects active tournament rounds if you crash, rejoin, or substitute into a match, resuming recording immediately.
* **⚡ Auto Profile Switching & Scrim Mode:** Auto-switches rulesets when match configs load; suppresses status screenshots and adds `_scrim` prefix during practice.
* **🏆 Multi-League Rulesets:** Dedicated compliance for **ETF2L** (Rule 2.1), **AsiaFortress**, **RGL** (1008.5), **ozfortress**, **Matcha.tf**, and **CLTF2**.
* **🔍 Auto-Healing RCON & DemoMan Synergy:** Automatically synchronizes passwords and recovers in <1ms if you switch `rcon_password` in-game for server commands. Automatically pairs with local [DemoMan](https://github.com/DemomanApp/DemoMan) setups.
* **🎵 Authentic Tactile Audio Cues:** Uses classic original P-REC mechanical switch clicks in-game (`buttons/button9.wav` on start, `buttons/button14.wav` on stop, `buttons/bell1.wav` on bookmark) with zero annoying piezo buzzers and zero confusing player voice lines.
* **🖥️ 1-Minute Setup & 1-Click Uninstaller:** Interactive setup wizard configures your active autoexec, creates optional Desktop shortcuts, and sets up silent startup.

---

### 🚀 Steam Launch Options
Add either option to your TF2 Launch Options in Steam (**Properties -> General -> Launch Options**):

* **Option 1 (RCON Mode - Recommended, identical to DemoMan):**
  ```text
  -usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
  ```
* **Option 2 (Netcon Mode - Ultra-short):**
  ```text
  -netconport 2121
  ```

---

### 📥 Release Downloads
* **Windows (64-bit Standalone Executable):** [`prec64.exe`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/prec64.exe)
* **Linux (64-bit Standalone ELF Binary):** [`prec64`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/prec64)
* **Configuration File:** [`PREC_Settings.cfg`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/PREC_Settings.cfg)

📖 **Full Documentation & Configuration Reference:** See [README.md](https://github.com/Emieldev/P-REC-External/blob/main/README.md).

---

### 🙏 Credits
* **Oleg Koshmeliuk (Orange)** for the legendary original [P-REC (Pov-Record)](https://github.com/olegKoshmeliuk/Pov-Record) plugin.
* **peaches** for [PeachREC](https://github.com/peaches-tf2/PeachREC).
* **DemoMan** developers for the [DemoMan](https://github.com/DemomanApp/DemoMan) ecosystem.
* ETF2L, AsiaFortress, RGL.gg, ozfortress, Matcha.tf, and CLTF2 communities.
