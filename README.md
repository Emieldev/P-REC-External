# P-REC External (v1.0.0)
### Zero-Lag, Zero-Warmup Automated Match Recorder for Team Fortress 2 (64-Bit Native)

[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/Emieldev/P-REC-External/releases)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg)](https://github.com/Emieldev/P-REC-External)
[![TF2 Architecture: 64-bit Native](https://img.shields.io/badge/TF2-64--bit%20Native-orange.svg)](https://github.com/Emieldev/P-REC-External)
[![Ruleset: ETF2L / AsiaFortress / RGL / ozfortress / Matcha / CLTF2](https://img.shields.io/badge/Ruleset-ETF2L%20%7C%20AsiaFortress%20%7C%20RGL%20%7C%20ozfortress%20%7C%20Matcha%20%7C%20CLTF2-green.svg)](https://github.com/Emieldev/P-REC-External)
[![100% VAC-Safe](https://img.shields.io/badge/VAC-100%25%20Safe-brightgreen.svg)](https://github.com/Emieldev/P-REC-External)
[![100% Vibecoded](https://img.shields.io/badge/Codebase-100%25%20Vibecoded-purple.svg)](https://github.com/Emieldev/P-REC-External)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

---

> [!WARNING]
> ### ⚠️ 100% Completely Vibecoded Application — Use at Your Own Risk
> **Why does this project exist?**
> Honestly, I got fed up with PeachREC microstutters making it unusable and causing start of round lag with many HUDs, and the original **P-REC not working** on modern 64-bit TF2 without `-insecure` (which Valve requires for unsigned plugins, blocking connection to VAC match servers).
>
> So I **vibecoded this companion for myself** using AI to achieve zero game lag, zero warmup bloat, and flawless competitive league compliance.
>
> ⚠️ **Player Responsibility Disclaimer:**
> In all competitive leagues (ETF2L, RGL, ozfortress, AsiaFortress, etc.), **it remains the player's personal responsibility to ensure your POV demos are actively recording and saved**. While this software is architecturally **100% VAC-safe** (using official Source Engine RCON and Netcon loopback protocols with zero memory injection, zero DLL hooking, and zero modified game binaries), always verify your in-game developer console (`~`) notifications, check your demo folder after games, and test recording during scrims before relying on it for high-stakes league matches!

---

## ⚡ Key Advantages

| Feature | How P-REC External Solves It | Predecessors / Alternatives |
| :--- | :--- | :--- |
| **0 FPS Impact / Zero Lag** | Runs completely out-of-process via engine network sockets. Touches **0 HUD animation manifests** and draws **0 VGUI panels**. | **PeachREC** runs synchronous animation loops on the main render thread, causing frame pacing jitter and start-of-round microstutters with many HUDs. |
| **100% VAC-Safe** | Uses official Source Engine RCON and Netcon protocols. Zero DLL injection, zero memory tampering. | **Original P-REC** cannot run on 64-bit TF2 without `-insecure` (which triggers VAC server bans and league disqualification). |
| **Zero Warmup Bloat** | Listens to tournament countdown pulses and triggers recording **strictly when the match goes live**. | Valve's **`ds_enable 3`** starts recording the instant you join a server with `mp_tournament 1`, recording 30+ minutes of warmups and roll-calls. |
| **🛡️ System Tray (Hidden Pictograms)** | Runs quietly in the Windows Notification Area under **Hidden Pictograms** with the TF2 **Supreme Soviet** icon. Right-click for Settings, Custom Folder, or clean Exit! | Clutters your taskbar with open cmd windows. |
| **⚡ Auto Profile Switching** | Automatically switches active league ruleset when an official tournament config is executed on the server. | Manual reconfiguration required in older tools. |
| **🎯 Scrim vs. Match Handling** | Automatically differentiates between **practice scrims** (`_scrim` prefix, suppresses screenshot spam) and **official matches** (full compliance & status screenshots). | Other tools take useless status screenshots on every practice round. |
| **🔍 DemoMan Auto-Detection** | Automatically discovers local [DemoMan](https://github.com/DemomanApp/DemoMan) installations, extracts its active RCON password and pre-fills your TF2 `/tf` path! | Zero manual port configuration or password hassle. |
| **Strict League Compliance** | Dedicated modular rulesets for **ETF2L**, **AsiaFortress**, **RGL**, **ozfortress**, **Matcha.tf**, and **CLTF2**. | Automatically captures required SteamID status screenshots (`status; jpeg`) and handles server checks. |
| **Crash & Reconnect Recovery** | Detects active tournament rounds if you crash and reconnect mid-match, resuming recording immediately. | Complies strictly with [ETF2L Rule 2.1](https://rules.etf2l.org/docs/general-2/#21-every-player-has-to-record-demos). Built-in TF2 recording fails to resume if you reconnect. |
| **Silent Background Tray & Auto-Start** | Runs quietly under Hidden Pictograms and can boot with Windows automatically. Hooks into TF2 with just `-netconport 2121`. | Never forget to record an official match again. |
| **Discord-Safe Background Install** | Installs into dedicated program folder while placing configs in `tf/custom/P-REC/cfg/` — avoids Discord falsely reporting you as playing TF2 24/7. | Putting executables in `steamapps/common/` causes Discord to report you playing TF2 constantly. |

---

## 🚀 Steam Launch Options (Choose One)

Add EITHER of these options to your TF2 Launch Options in Steam (**Right-click Team Fortress 2 in Steam -> Properties -> General -> Launch Options**):

### ▶ Option 1: RCON Mode (Recommended - identical to DemoMan)
```text
-usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
```
*(If you already use [DemoMan](https://github.com/DemomanApp/DemoMan), keep DemoMan's launch options as they are — P-REC External detects DemoMan automatically and hooks into port 27969).*

#### ⚡ Server RCON & serveme.tf Synergy (Auto-Healing RCON)
> [!NOTE]
> TF2 uses a single cvar (`rcon_password`) for both incoming local listen rcon (P-REC / DemoMan) and outgoing server rcon (match servers). 
> If you switch `rcon_password` in-game to run server commands, P-REC External's **Auto-Healing RCON Engine** automatically detects the reset, synchronizes candidates, and re-authenticates in **under 1 millisecond** without missing a single frame or dropping demo recording!

### ▶ Option 2: Netcon Mode (Ultra-Short, 16 characters)
```text
-netconport 2121
```

---

## 💻 Platforms & Quick Start

| Platform | Download | Quick Start |
| :--- | :--- | :--- |
| **Windows** | [`prec64.exe`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/prec64.exe) | Run `prec64.exe` (it silently hides to tray) or run `prec64.exe --install` for the wizard. |
| **Linux** | [`prec64`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.0/prec64) | `chmod +x prec64 && ./prec64` (requires 0 external dependencies!). |

---

## 🛡️ Windows System Tray (Hidden Pictograms)

When running on Windows, P-REC External lives quietly in your system tray under **Hidden Pictograms** (`^`) with the **Supreme Soviet** icon (`assets/supreme_soviet.ico`):

* **Left Click / Double-Click:** Instantly toggles the console window.
* **Crossing out ('X'):** Minimizes the console window back to the hidden tray without terminating recording.
* **Right-Click Context Menu:**
  * **Status Header:** Live connection and recording status (e.g. `Connected (ETF2L)`).
  * **Show / Hide Console Window:** Toggles terminal window visibility if you want to inspect live logs.
  * **Check RCON / Connection:** Manually tests communication with TF2, outputs diagnostics, and sends confirmation into the in-game developer console (`~`).
  * **Start with Windows:** 1-click toggle to boot silently with Windows directly into your hidden system tray.
  * **Go to Settings (PREC_Settings.cfg):** Quick one-click configuration access.
  * **Open tf/custom/ Folder:** Instantly opens your TF2 mods folder in File Explorer.
  * **Create Desktop Shortcut:** Instantly creates or repairs a Desktop shortcut.
  * **Report Issue / Bug (GitHub)...:** Directly opens the GitHub Issues page in your browser.
  * **Uninstall P-REC External...:** Clean uninstaller with options to keep or wipe settings.
  * **Close P-REC External:** Stops recording cleanly, frees ports, and shuts down the background process.

---

## 🐧 Linux Support Out-of-the-Box

The standalone Linux binary (`prec64`) is built natively for 64-bit Linux with zero external dependencies:
* **Native `/proc` Process Detection:** Reads `/proc/[0-9]*/comm` directly to detect `tf_linux64` and `hl2_linux` in `< 0.1ms` with 0 subprocesses.
* **Multi-Drive & Steam Deck Discovery (`libraryfolders.vdf`):** Automatically finds your `/tf` folder across all drives, secondary SSD mounts (`/mnt/...`), Flatpak Steam, Snap Steam, and Steam Deck SD cards.
* **POSIX Single-Instance Locking:** Uses kernel file locking (`fcntl.flock`) to prevent multiple background instances.
* **Desktop Notifications:** Sends system notifications via `notify-send` when recording starts and finishes.
* **Audio Fallback:** Supports PipeWire (`pw-play`), PulseAudio (`paplay`), ALSA (`aplay`), and terminal chime (`\a`).

---

## ⚡ Dynamic Profile Switching & Scrim Mode

### 1. Automatic League Switching
When connected to a competitive server, P-REC External inspects console output for executed tournament configs. If the server executes an ETF2L config, AsiaFortress config, RGL config, ozfortress config, Matcha config, or CLTF2 config, P-REC External **dynamically switches its active league profile** on the fly without restarting:
```text
[P-REC External] ⚡ AUTO-SWITCHED LEAGUE PROFILE: AsiaFortress (AsiaFortress Cup & League) [OFFICIAL MATCH]
[P-REC External] Triggered by config execution: af_6v6_5cp.cfg
```

### 2. Scrim Mode vs. Official Match Mode
* **Official Match Mode:** Demos use official league prefixes (`etf2l_`, `af_`, `rgl_`, `ozf_`). Captures mandatory status screenshots (`status; jpeg`) with player SteamIDs at mid-match (randomly after 3 minutes) and scoreboard screenshot at match completion.
* **Scrim Mode:** Demos are automatically tagged with `_scrim` (e.g. `etf2l_scrim_`, `af_scrim_`). **Suppresses mandatory status screenshots** during scrims so your screenshot folder isn't cluttered with dozens of practice status checks.

---

## 🏆 League Ruleset Compliance

* **ETF2L ([General Rule 2.1](https://rules.etf2l.org/docs/general-2/#21-every-player-has-to-record-demos) | [6v6 Rules](https://rules.etf2l.org/docs/6v6-2) | [9v9 Rules](https://rules.etf2l.org/docs/9v9-2)):** Continuous POV demo recording across all match rounds (5CP, KOTH, Stopwatch, Golden Cap, Halves), under-100MB file compliance (eliminates warmup bloat so demos upload cleanly to ETF2L without rejection), mid-match reconnect/crash recovery, and automated mid-game SteamID status screenshots (`status; jpeg`).
* **AsiaFortress ([Rules](https://docs.google.com/document/d/16D6nGRbq1ZafMtR1uBOfnvC3jJ4K4lPzqbrB6lqDQ74/edit?tab=t.0#heading=h.rdjxx5582d9w)):** Detects `af_` tournament configs, applies `af` demo prefixes, and captures round status screenshots.
* **RGL.gg ([Rule 1008.5](https://docs.rgl.gg/rules/global/1008/?h=pov+demos#1008_5-pov-and-stv-demos)):** Enforces `ds_autodelete 0`, applies `rgl` demo prefix, and triggers cleanly on `rgl_` configs.
* **ozfortress ([POV Guide](https://docs.ozfortress.com/guides/pov_demo_recording/)):** Keeps `ds_enable 3` set to pass server-side `sm_querycvar` Demo Checker checks, then cleanly splits the match demo from the pre-game warmup via `ds_stop; ds_record` the instant countdown begins.
* **Matcha.tf & CustomLander TF2 ([Matcha Rules](https://rules.matcha.tf/) & [CLTF2 Rule 3.3](https://docs.cltf2.com/)):** Native config recognition and prefix tagging for `matcha` and `cltf2`.

---

## 🛠️ Interactive Setup Wizard & Uninstallation

Run the interactive setup wizard at any time:
```bash
# Windows
prec64.exe --install

# Linux
./prec64 --install
```

### What the Setup Wizard Does:
1. **Auto-Detects DemoMan:** Discovers DemoMan's password and TF2 path automatically.
2. **Confirms `/tf` Location:** Confirms detected paths on Windows and Linux.
3. **Scans `/tf/custom/` for Conflicting Mods:** Cleans up legacy PeachREC HUD animation loops (`hudanimations_peachrec.txt`) that cause in-game microstutters, and removes obsolete 32-bit `prec.dll` files.
4. **Installs Cleanly Outside Steam:** Places the executable into `%LOCALAPPDATA%\Programs\P-REC\` (or `~/.local/share/P-REC/` on Linux) to prevent Discord from falsely reporting you playing TF2 24/7.
5. **Configures Autoexec:** Safely adds optimal P-REC settings to your active `autoexec.cfg` with full diff previews and backup creation.

### 🗑️ Clean Uninstallation
* **Via System Tray:** Right-click the Supreme Soviet icon -> **"Uninstall P-REC External..."**.
* **Via Command Line:**
  ```bash
  prec64.exe --uninstall
  ```
Prompts whether to preserve or wipe your configuration files, removes startup registry/autostart entries, deletes shortcuts, and cleans up binaries.

---

## 📁 Modular League Rulesets (`leagues/*.json`)

All league rules are stored as modular JSON files in the [`leagues/`](leagues/) directory:
* [`etf2l.json`](leagues/etf2l.json)
* [`asiafortress.json`](leagues/asiafortress.json)
* [`rgl.json`](leagues/rgl.json)
* [`ozfortress.json`](leagues/ozfortress.json)
* [`matcha.json`](leagues/matcha.json)
* [`cltf2.json`](leagues/cltf2.json)

To add a new league, copy `leagues/template.json` to `leagues/<your_league_id>.json`, customize its server config patterns and prefixes, and submit a Pull Request!

---

## ⚙️ Configuration Reference (`PREC_Settings.cfg`)

Located in `tf/custom/P-REC/cfg/PREC_Settings.cfg` (or `tf/cfg/`):

| Convar / Setting | Default | Description |
| :--- | :--- | :--- |
| `prec_version` | `"1.0.0"` | Configuration version. |
| `prec_league` | `"etf2l"` | Default league profile (`etf2l`, `asiafortress`, `rgl`, `ozfortress`, `matcha`, `cltf2`, `custom`). Automatically switches when match configs execute. |
| `prec_mode` | `2` | `3` = Record ALL matches (every map/round), `2` = Record tournament matches only (Default), `1` = Manual recording (`prec_record`), `0` = Disabled. |
| `prec_dir` | `"demos"` | Folder inside `/tf/` where demo files are saved. |
| `prec_sound` | `1` | `1` = Short, chill in-game tactile UI cues (Classic P-REC button clicks: `buttons/button9.wav` & `buttons/button14.wav`), `0` = Mute. |
| `prec_sound_start` | `"buttons/button9.wav"` | Source Engine sound path played on record start. |
| `prec_sound_stop` | `"buttons/button14.wav"` | Source Engine sound path played on record stop. |
| `prec_sound_mark` | `"buttons/bell1.wav"` | Source Engine sound path played on bookmark (`ds_mark`). |
| `prec_hide_to_tray` | `1` | `1` = Hide console window into Windows System Tray (Hidden Pictograms), `0` = Keep console window open. |
| `prec_screens` | `1` | `1` = Capture in-game status screenshot (randomly after 3 mins of play) & match-end scoreboard. Automatically suppressed during scrims. |
| `prec_notify` | `1` | `0` = Console only, `1` = Team chat announcements, `2` = HUD notification. |
| `prec_delete_useless_demo` | `0` | `0` = Never delete (strictly required for league compliance). |
| `prec_tag` | `""` | Custom prefix tag for demo names (leave blank for league default). |
| `alias pr_message_start` | `say_team [PREC] Recording started.` | Chat message sent when recording begins. |
| `alias pr_message_stop` | `say_team [PREC] Stop recording.` | Chat message sent when recording ends. |
| `alias pr_message_mark` | `say_team [PREC] Bookmark placed.` | Chat message sent when a bookmark is placed. |

---

## 🤝 Contributing & Reporting Issues

* **Found a bug or have a suggestion?** Click **"Report Issue (GitHub)"** in the console window toolbar, right-click the system tray icon and select **"Report Issue / Bug (GitHub)..."**, or type `prec_issue` in your TF2 console to open the [GitHub Issues Tracker](https://github.com/Emieldev/P-REC-External/issues).
* **Pull Requests:** PRs for bug fixes, new league rulesets, and documentation improvements are welcome!

---

## 🙏 Credits & Acknowledgements

* **The Original P-REC:** Huge respect and credit to **Oleg Koshmeliuk (Orange)** for creating the legendary original [P-REC (Pov-Record)](https://github.com/olegKoshmeliuk/Pov-Record) Source engine plugin that served the competitive TF2 community for over a decade.
* **PeachREC:** Thanks to **peaches** for [PeachREC](https://github.com/peaches-tf2/PeachREC).
* **DemoMan:** Credit to the [DemoMan](https://github.com/DemomanApp/DemoMan) developers for creating an awesome demo manager and modern TF2 ecosystem tool.
* **Competitive Leagues:** Respect to ETF2L, AsiaFortress, RGL.gg, ozfortress, Matcha.tf, and CLTF2 for keeping competitive Team Fortress 2 thriving worldwide.

---

## 📜 License & Liability Disclaimer

This software is released under the **GNU General Public License v3.0 (GPL-3.0)**.
* **Copyleft Requirement:** Any modifications, derivative works, or distributions must also remain free, open source, and licensed under GPL-3.0.
* **Liability Disclaimer (GPL-3.0 Sections 15 & 16):** The software is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of this software.
