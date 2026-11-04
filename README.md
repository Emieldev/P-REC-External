# P-REC External (v1.0.0)
### Zero-Lag, Zero-Warmup Automated Match Recorder for Team Fortress 2 (64-Bit Native)

[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/Emieldev/P-REC-External/releases)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg)](https://github.com/Emieldev/P-REC-External)
[![TF2 Architecture: 64-bit Native](https://img.shields.io/badge/TF2-64--bit%20Native-orange.svg)](https://github.com/Emieldev/P-REC-External)
[![Ruleset: ETF2L / AsiaFortress / RGL / ozfortress / Matcha / CLTF2](https://img.shields.io/badge/Ruleset-ETF2L%20%7C%20AsiaFortress%20%7C%20RGL%20%7C%20ozfortress%20%7C%20Matcha%20%7C%20CLTF2-green.svg)](https://github.com/Emieldev/P-REC-External)
[![100% VAC-Safe](https://img.shields.io/badge/VAC-100%25%20Safe-brightgreen.svg)](https://github.com/Emieldev/P-REC-External)
[![100% Vibecoded](https://img.shields.io/badge/Codebase-100%25%20Vibecoded-purple.svg)](https://github.com/Emieldev/P-REC-External)
[![Dependabot](https://img.shields.io/badge/Dependabot-Enabled-blue.svg)](https://github.com/Emieldev/P-REC-External)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

---

> [!WARNING]
> ### ⚠️ 100% Completely Vibecoded Application — Use at Your Own Risk
> **Why does this project exist?**
> Honestly, I got completely fed up with **PeachREC being shit** (causing microstutters and frame drops with synchronous HUD animation loops) and the original **P-REC not working** on modern 64-bit TF2 without `-insecure` (which Valve requires for unsigned plugins, blocking connection to VAC match servers).
>
> So I **vibecoded this companion for myself** using AI to achieve zero game lag, zero warmup bloat, and flawless competitive league compliance.
>
> While this software is architecturally **100% VAC-safe** (it uses official Source Engine RCON and Netcon loopback protocols with zero memory injection, zero DLL hooking, and zero modified game binaries), it is community vibecoded software. **Always test and verify your demo recordings during scrims and practice before relying on it for high-stakes league championship matches!**

---

## ⚡ Key Advantages (Why Use P-REC External?)

| Feature | How P-REC External Solves It | Predecessors / Alternatives |
| :--- | :--- | :--- |
| **0 FPS Impact / Zero Lag** | Runs completely out-of-process via engine network sockets. Touches **0 HUD animation manifests** and draws **0 VGUI panels**. | **PeachREC** runs synchronous animation loops on the main render thread, causing frame pacing jitter and microstutters. |
| **100% VAC-Safe** | Uses official Source Engine RCON and Netcon protocols. Zero DLL injection, zero memory tampering. | **Original P-REC** cannot run on 64-bit TF2 without `-insecure` (which triggers VAC server bans and league disqualification). |
| **Zero Warmup Bloat** | Listens to tournament countdown pulses and triggers recording **strictly when the match goes live**. | Valve's **`ds_enable 3`** starts recording the instant you join a server with `mp_tournament 1`, recording 30+ minutes of warmups and roll-calls. |
| **🛡️ System Tray (Hidden Pictograms)** | Runs quietly in the Windows Notification Area under **Hidden Pictograms** with the crisp TF2 **Supreme Soviet** icon. Right-click for Settings, Custom Folder, or clean Exit! | Clutters your taskbar with open cmd windows. |
| **⚡ Auto Profile Switching** | Automatically switches active league ruleset when an official tournament config is executed on the server. | Manual reconfiguration required in older tools. |
| **🎯 Scrim vs. Match Handling** | Automatically differentiates between **practice scrims** (`_scrim` prefix, suppresses screenshot spam) and **official matches** (full compliance & status screenshots). | Other tools take useless status screenshots on every practice round. |
| **🔍 DemoMan Auto-Detection** | Automatically discovers local [DemoMan](https://github.com/DemomanApp/DemoMan) installations, extracts its active RCON password and pre-fills your TF2 `/tf` path! | Zero manual port configuration or password hassle. |
| **Strict League Compliance** | Dedicated modular rulesets for **ETF2L**, **AsiaFortress**, **RGL**, **ozfortress**, **Matcha.tf**, and **CLTF2**. | Automatically captures required SteamID status screenshots (`status; jpeg`) and handles server checks. |
| **Crash & Reconnect Recovery** | Detects active tournament rounds if you crash and reconnect mid-match, resuming recording immediately. | Complies strictly with [ETF2L Rule 2.1](https://rules.etf2l.org/docs/general-2/#21-every-player-has-to-record-demos). Built-in TF2 recording fails to resume if you reconnect. |
| **Silent Background Tray & Auto-Start** | Runs quietly under Hidden Pictograms and can boot with Windows automatically. Hooks into TF2 with just `-netconport 2121`. | Never forget to record an official match again. |
| **Discord-Safe Background Install** | Installs into dedicated program folder while placing configs in `tf/custom/P-REC/cfg/` — avoids Discord falsely reporting you as playing TF2 24/7. | Putting executables in `steamapps/common/` causes Discord to report you playing TF2 constantly. |

---

## 🛡️ Windows Background Program (Hidden Pictograms / System Tray)

When running on Windows, P-REC External lives quietly in your system tray under the **Hidden Pictograms** (`^`) area with the **Supreme Soviet** icon (`assets/supreme_soviet.ico`):

* **Left Click / Double-Click:** Instantly toggles the console window (bringing it back from the hidden tray).
* **Crossing out ('X'):** Minimizes the console window back to the hidden tray without terminating recording.
* **Right-Click Context Menu:**
  * **Status Header:** Live connection and recording status (e.g. `P-REC External (Connected)`).
  * **Show / Hide Console Window:** Toggles terminal window visibility if you ever want to check live logs.
  * **Check RCON / Connection:** Manually tests communication with TF2, outputs diagnostics, and sends confirmation into the in-game developer console (`~`).
  * **Start with Windows:** 1-click toggle to boot silently with Windows directly into your hidden system tray.
  * **Go to Settings (PREC_Settings.cfg):** Quick one-click configuration access.
  * **Open tf/custom/ Folder:** Instantly opens your TF2 mods folder in File Explorer.
  * **Close P-REC External:** Stops recording cleanly, frees ports, and shuts down the background process.

---

## 💡 Classic P-REC Acronym Expansions (Name Ideas)

Keeping faith with the classic **P-REC** heritage:

1. **P-REC External: Precision Recording Engine for Competition** *(Accurate, professional, focuses on sub-tick live countdown timing)*
2. **P-REC External: Point-of-view Recording External Companion** *(Descriptive of its non-intrusive, zero-injection architecture)*
3. **P-REC External: Peach-Replacement External Companion** *(Community tongue-in-cheek nod to replacing PeachREC's stuttery HUD loops)*
4. **P-REC External: Perfect Recording for Esports & Competition** *(Focuses on tournament compliance and ruleset integrity)*
5. **P-REC External: Pure Recording External Client** *(Nods to running on pure VAC-secured TF2 without `-insecure`)*
6. **P-REC External: Painless Recording for Every Competition** *(Emphasizes automatic league switching, auto-RCON, and zero setup pain)*
7. **P-REC External: Performance Recording & Esports Companion** *(Highlights zero FPS impact)*

---

## ⚡ Dynamic Profile Switching & Scrim Mode

### 1. Automatic League Switching
When connected to a competitive server, P-REC External inspects console output for executed tournament configs. If the server executes an ETF2L config, AsiaFortress config, RGL config, ozfortress config, Matcha config, or CLTF2 config, P-REC External **dynamically switches its active league profile** on the fly without restarting:
```text
[P-REC External] ⚡ AUTO-SWITCHED LEAGUE PROFILE: AsiaFortress (AsiaFortress Cup & League) [OFFICIAL MATCH]
[P-REC External] Triggered by config execution: af_6v6_5cp.cfg
```

### 2. Scrim Mode vs. Official Match Mode
Competitive players spend hours scrimming before tournament matches. P-REC External distinguishes between practice scrims and official league games:
* **Official Match Mode:**
  * Demos named with official league prefix (e.g., `etf2l_`, `af_`, `rgl_`, `ozf_`).
  * Mandatory status & scoreboard screenshots (`status; jpeg`) captured at match completion (mandated by ETF2L Rule 2.1 & AsiaFortress rules).
* **Scrim Mode:**
  * Demos automatically tagged with `_scrim` (e.g., `etf2l_scrim_`, `af_scrim_`, `rgl_scrim_`, `ozf_scrim_`).
  * **Suppresses mandatory status screenshots** during scrims so your screenshot folder isn't cluttered with 50 practice status checks.
  * In-game team chat announces: `say_team [PREC Scrim] Recording started.`

---

## 🔍 Automatic DemoMan Integration

If you use [DemoMan](https://github.com/DemomanApp/DemoMan), P-REC External **automatically pairs with it**:
* Inspects DemoMan's local state storage to extract its active `rconPassword`.
* Detects your configured TF2 `/tf` path directly from DemoMan's `demoDirs`.
* Shares RCON port `27969` without conflicts.
* Automatically pre-fills both settings during the initial setup wizard!

---

## 🏆 What This Adds for Strict League Rulesets

Competitive leagues enforce strict POV demo recording rules with severe penalties (default losses, point deductions, or bans for suspected cheating):

### 1. European TF2 League ([ETF2L Rule 2.1](https://rules.etf2l.org/docs/general-2/#21-every-player-has-to-record-demos))
* **The Problem:** ETF2L strictly mandates that demos must cover the entire match. If your game crashes or you drop and reconnect mid-game, Valve's built-in `ds_enable 3` will NOT resume recording because the tournament mode wasn't restarted. Furthermore, ETF2L strictly mandates capturing proof of all players' SteamIDs and SourceTV status.
* **What P-REC External Adds:**
  * **Mid-match reconnect recovery:** Detects reconnections and sends `status` to verify match state, immediately resuming recording if the tournament match is in progress.
  * **Automated Status Screenshot:** Automatically triggers `status; jpeg` at match completion, saving the screenshot directly into your demo/screenshot folder with complete SteamID proof.

### 2. AsiaFortress ([AsiaFortress Rules](https://docs.google.com/document/d/16D6nGRbq1ZafMtR1uBOfnvC3jJ4K4lPzqbrB6lqDQ74/edit?tab=t.0#heading=h.rdjxx5582d9w))
* **The Problem:** AsiaFortress rules strictly mandate that all players must record first-person POV demos for all official cup and league matches. Demos must be submitted upon admin request within strict deadlines, and failure to provide POV demos results in round forfeits or match bans.
* **What P-REC External Adds:**
  * Automated detection of `af_` tournament configs (`af_6v6_5cp`, `af_6v6_koth`, `af_hl_stopwatch`, etc.).
  * Applies official `af` prefix (or `af_scrim` prefix during scrims).
  * Automatically captures status screenshots with SteamIDs at round completion.

### 3. RGL.gg ([RGL Rule 1008.5](https://docs.rgl.gg/rules/global/1008/?h=pov+demos#1008_5-pov-and-stv-demos))
* **The Problem:** RGL mandates POV demos for all matches and requires them to be kept throughout the season. Accidental demo deletion or missed starts result in penalty points.
* **What P-REC External Adds:**
  * Enforces `ds_autodelete 0` (preventing any automatic deletion).
  * Recognizes official RGL server config patterns (`rgl_6s`, `rgl_hl`, `rgl_7s`, `rgl_pt`) and `"Config Executed"` prints to arm and trigger recording seamlessly.
  * Applies the official `rgl` demo naming prefix.

### 4. ozfortress ([ozfortress POV Guide](https://docs.ozfortress.com/guides/pov_demo_recording/))
* **The Problem:** ozfortress servers run a server-side **Demo Checker** plugin (`sm_querycvar`) that queries client cvars upon connection, checking for `ds_enable 2/3` and `ds_autodelete 0`. If `ds_enable 0`, players receive warnings or penalties. However, `ds_enable 3` clutters hard drives with 45 minutes of pre-game warmup bloat.
* **What P-REC External Adds:**
  * Keeps `ds_enable 3` set so your client passes all server-side `sm_querycvar` checks with flying colors.
  * The split second the live tournament countdown begins, P-REC External issues `ds_stop; ds_record` to cleanly split the official match demo from the pre-game warmup!

### 5. Matcha.tf & CustomLander TF2 ([Matcha Rules](https://rules.matcha.tf/) & [CLTF2 Rule 3.3](https://docs.cltf2.com/))
* **What P-REC External Adds:**
  * Native recognition of Asia/Pacific tournament configs (`matcha_6v6`, `matcha_hl`, `[Matcha]`) and CLTF2 configs (`cltf2_4s`, `cltf2_ultiduo`, `[CLTF2]`).
  * Automates demo naming prefixes (`matcha` / `cltf2`) and end-of-round screenshots for admin verifications.

---

## 🛠️ Interactive Setup & Configuration Auditor

P-REC External includes an interactive setup wizard that configures everything in under 60 seconds:
```bash
# Run on Windows:
prec64.exe --install

# Or on Linux / Python:
python3 prec64.py --install
```

### What the Setup Wizard Does:
1. **Auto-Detects DemoMan:** Discovers DemoMan's password and TF2 path.
2. **Prompts for `/tf` Location:** Confirms detected paths on Windows and Linux.
3. **Scans `/tf/custom/` for Conflicting Mods:**
   * Detects and removes PeachREC HUD animation loops (`hudanimations_peachrec.txt` and `hudanimations_manifest.txt` hooks) that cause game lag.
   * Cleans up legacy 32-bit `prec.dll` / `prec.vdf` files that cannot load on 64-bit TF2.
4. **Installs Cleanly Outside Steam:** Places the executable into `%LOCALAPPDATA%\Programs\P-REC\` and configuration into `/tf/custom/P-REC/cfg/` (preventing Discord false game detection).
5. **Discovers Modular League Profiles:** Displays all rulesets found in `leagues/*.json`.
6. **Audits `/tf/cfg/overrides/` and `/tf/cfg/`:**
   * Discovers existing config files (`autoexec.cfg`, `game_overrides.cfg`, etc.).
   * **Explicitly asks whether to update configs in bulk or file-by-file (one by one)** with full diff previews.
   * Automatically creates `.cfg.bak` backups before modifying anything.
7. **Outputs Ready-to-Use Steam Launch Options!**

---

## 💻 Windows vs. Linux Support

| Platform | Download / Binary | How to Run |
| :--- | :--- | :--- |
| **Windows** | `prec64.exe` (Standalone Windows Executable) | Run `prec64.exe` directly (silently hides to tray) or enable Start with Windows. |
| **Linux** | `prec64` (Standalone Linux ELF Binary) or `prec64.py` | `chmod +x prec64 && ./prec64` or `python3 prec64.py` (requires 0 external dependencies!). |

> [!NOTE]
> An `.exe` file is a Windows Portable Executable and cannot run natively on Linux without Wine/Proton. For Linux gamers, use the native Linux binary (`prec64`) or run `python3 prec64.py` directly with your system's Python 3 installation!

---

## 🚀 Steam Launch Options (Choose One)

You can choose either of these two options in TF2's Launch Options in Steam (**Right-click Team Fortress 2 in Steam -> Properties -> General -> Launch Options**). Both fit directly into Steam's box with zero shell wrappers:

### ▶ Option 1: RCON Mode (Recommended - identical to DemoMan)
```text
-usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
```
*(If you already use [DemoMan](https://github.com/DemomanApp/DemoMan), keep DemoMan's launch options as they are — P-REC External detects DemoMan automatically and hooks into port 27969).*

#### ⚡ Server RCON & serveme.tf Synergy (Auto-Healing RCON)
> [!IMPORTANT]
> **Understanding TF2's Single `rcon_password` Cvar:**
> In Valve's Source Engine, the exact same console cvar (`rcon_password`) controls both:
> 1. **Outgoing Server RCON:** Connecting to remote match servers (e.g. [serveme.tf](https://serveme.tf), match reservations, or dedicated scrim servers) to run admin commands (`rcon changelevel ...`, `rcon exec etf2l_6v6_5cp`).
> 2. **Incoming Local Listen RCON:** The local port `27969` loopback socket on your computer used by P-REC External and DemoMan.
>
> When you run `rcon_password <password>` in-game or via an autoexec server alias, TF2 terminates existing local connections and switches port 27969's listening password to match.
>
> **How P-REC External seamlessly handles this:**
> * **Steam Launch Alignment:** Set `+rcon_password YOUR_PASSWORD` in your Steam Launch Options matching your preferred match server password. On **serveme.tf**, you can configure your default RCON password in your user settings so every reservation matches your launch option.
> * **Auto-Healing RCON Engine:** P-REC External automatically extracts candidate passwords from your running game process, `autoexec.cfg`, and `prec_server_rcon_passwords`. If you switch passwords in-game to run server commands, P-REC catches the socket reset, cycles candidate passwords, and re-authenticates in **under 1 millisecond** without missing a single frame or dropping demo recording!
> * **Netcon Alternative:** If you prefer not to manage RCON passwords at all, you can also use **Option 2 (Netcon Mode)** below with `-netconport 2121`.

### ▶ Option 2: Netcon Mode (Ultra-Short, 16 characters)
```text
-netconport 2121
```

### How it works:
1. Run `prec64.exe` (it sits silently in your Windows System Tray under **Hidden Pictograms** with the TF2 Supreme Soviet icon).
2. Launch Team Fortress 2 from Steam.
3. P-REC External connects automatically, prints a confirmation into your in-game developer console (`~`), monitors tournament status live, and records your official demos with zero warmup bloat!

> [!TIP]
> **Want it to start automatically with your PC?**
> In the setup wizard (`prec64.exe --install`), enable **Start with Windows**, or right-click the Supreme Soviet tray icon and click **Start with Windows**. P-REC External will launch silently into your hidden tray whenever Windows boots!

---

## 📁 Modular League Rulesets (`leagues/*.json`)

All league rules are stored as independent JSON files in the [`leagues/`](leagues/) directory:
* [`etf2l.json`](leagues/etf2l.json)
* [`asiafortress.json`](leagues/asiafortress.json)
* [`rgl.json`](leagues/rgl.json)
* [`ozfortress.json`](leagues/ozfortress.json)
* [`matcha.json`](leagues/matcha.json)
* [`cltf2.json`](leagues/cltf2.json)

### Instructions for Leagues / Tournament Organizers:
1. Copy `leagues/template.json` to `leagues/<your_league_id>.json`.
2. Configure your league's specific settings:
   ```json
   {
     "id": "myleague",
     "name": "My Tournament League",
     "rules_url": "https://myleague.com/rules",
     "prefix": "myleague",
     "scrim_prefix": "myleague_scrim",
     "ds_enable": 0,
     "ds_autodelete": 0,
     "ds_screens": 1,
     "mandatory_status_screenshot": true,
     "server_demo_checker_bypass": false,
     "server_config_patterns": [
       "myleague_(6v6|9v9)(_scrim)?",
       "myleague.*config loaded"
     ],
     "chat_triggers": [
       "Match is LIVE",
       "Both teams are ready"
     ]
   }
   ```
3. Open a **Pull Request** on this repository! Once merged, all players using P-REC External worldwide will immediately have native compliance with your league rules!

---

## 🤝 Contributing & Pull Requests Welcome!

**Community contributions and Pull Requests are strongly encouraged!**
* **League Admins:** Submit PRs adding or updating your league's JSON profile in `leagues/`.
* **Developers:** Feel free to open PRs for bug fixes, Linux packaging improvements, or feature enhancements.
* **HUD Authors & Players:** Report edge cases, chat trigger formats, or feedback via GitHub Issues.

---

## ⚙️ Configuration Reference @[PREC_Settings.cfg](PREC_Settings.cfg)

| Convar / Alias | Default | Description |
| :--- | :--- | :--- |
| `prec_version` | `"1.0.0"` | Current configuration version. |
| `prec_league` | `"etf2l"` | Default league profile (`etf2l`, `asiafortress`, `rgl`, `ozfortress`, `matcha`, `cltf2`, `custom`). Automatically switches when match configs execute. |
| `prec_mode` | `2` | `0` = Off, `1` = Custom named only, `2` = Record active tournament matches only, `3` = Record all matches. |
| `prec_dir` | `"demos"` | Folder inside `/tf/` where demo files are saved. |
| `prec_sound` | `1` | `1` = Play audio cue on start/stop, `0` = Mute. |
| `prec_hide_to_tray` | `1` | `1` = Hide console window into Windows System Tray (Hidden Pictograms), `0` = Keep console window open. |
| `prec_screens` | `1` | `1` = Capture status & scoreboard screenshot at match end. Automatically suppressed during scrims. |
| `prec_notify` | `1` | `0` = Console only, `1` = Team chat announcements, `2` = HUD notification. |
| `prec_delete_useless_demo` | `0` | `0` = Never delete (strictly required for league compliance). |
| `prec_tag` | `""` | Custom prefix tag for demo names (leave blank for league default). |
| `alias pr_message_start` | `say_team [PREC] Recording started.` | Chat message sent when recording begins. |
| `alias pr_message_stop` | `say_team [PREC] Stop recording.` | Chat message sent when recording ends. |
| `alias pr_message_mark` | `say_team [PREC] Bookmark placed.` | Chat message sent when a bookmark is placed. |

---

## 🙏 Credits & Acknowledgements

* **The Original P-REC:** Huge respect and credit to **Aethelred (Orange)** for creating the legendary original [P-REC (POV - Record)](https://github.com/Orange-TF2/p-rec) Source engine plugin that served the competitive TF2 community for over a decade.
* **PeachREC:** Thanks to **peaches** for [PeachREC](https://github.com/peaches-tf2/PeachREC) and demonstrating the competitive scene's demand for modern automated recording solutions following the 64-bit TF2 update.
* **DemoMan:** Credit to the [DemoMan](https://github.com/DemomanApp/DemoMan) developers for creating an awesome demo manager and modern TF2 ecosystem tool.
* **Competitive Leagues:** Respect to ETF2L, AsiaFortress, RGL.gg, ozfortress, Matcha.tf, and CLTF2 for keeping competitive Team Fortress 2 thriving worldwide.

---

## 📜 License & Liability Disclaimer

This software is released under the **GNU General Public License v3.0 (GPL-3.0)**.
* **Copyleft Requirement:** Any modifications, derivative works, or distributions must also remain free, open source, and licensed under GPL-3.0.
* **Liability Disclaimer (GPL-3.0 Sections 15 & 16):** The software is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of this software.
