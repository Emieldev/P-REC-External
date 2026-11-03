# P-REC: Point-of-view Recording External Companion (v1.0.0)
### Zero-Lag, Zero-Warmup Automated Match Recorder for Team Fortress 2 (64-Bit Native)

[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg)](#)
[![TF2 Architecture: 64-bit Native](https://img.shields.io/badge/TF2-64--bit%20Native-orange.svg)](#)
[![Ruleset: ETF2L / RGL / ozfortress / Matcha / CLTF2](https://img.shields.io/badge/Ruleset-ETF2L%20%7C%20RGL%20%7C%20ozfortress%20%7C%20Matcha%20%7C%20CLTF2-green.svg)](#)
[![100% VAC-Safe](https://img.shields.io/badge/VAC-100%25%20Safe-brightgreen.svg)](#)
[![100% Vibecoded](https://img.shields.io/badge/Codebase-100%25%20Vibecoded-purple.svg)](#)
[![Dependabot](https://img.shields.io/badge/Dependabot-Enabled-blue.svg)](#)

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

## ⚡ Key Advantages (Why Use P-REC?)

| Feature | How P-REC Solves It | Predecessors / Alternatives |
| :--- | :--- | :--- |
| **0 FPS Impact / Zero Lag** | Runs completely out-of-process via engine network sockets. Touches **0 HUD animation manifests** and draws **0 VGUI panels**. | **PeachREC** runs synchronous animation loops on the main render thread, causing frame pacing jitter and microstutters. |
| **100% VAC-Safe** | Uses official Source Engine RCON and Netcon protocols. Zero DLL injection, zero memory tampering. | **Original P-REC** cannot run on 64-bit TF2 without `-insecure` (which triggers VAC server bans and league disqualification). |
| **Zero Warmup Bloat** | Listens to tournament countdown pulses and triggers recording **strictly when the match goes live**. | Valve's **`ds_enable 3`** starts recording the instant you join a server with `mp_tournament 1`, recording 30+ minutes of warmups and roll-calls. |
| **Strict League Compliance** | Dedicated modular rulesets for **ETF2L**, **RGL**, **ozfortress**, **Matcha.tf**, and **CLTF2**. | Automatically captures required SteamID status screenshots (`status; jpeg`) and handles server checks. |
| **Crash & Reconnect Recovery** | Detects active tournament rounds if you crash and reconnect mid-match, resuming recording immediately. | Complies strictly with [ETF2L Rule 2.1](https://rules.etf2l.org/docs/general-2/#21-every-player-has-to-record-demos). Built-in TF2 recording fails to resume if you reconnect. |
| **Auto-Booting with TF2** | Seamless Steam launch option wrapper launches the recorder automatically whenever you click "Play" in Steam. | Never forget to record an official match again. |
| **DemoMan & Auto-RCON** | Shares RCON port `27969` with [DemoMan](https://github.com/DemomanApp/DemoMan), or automatically generates a secure 12-char token if needed. | Zero port conflicts and zero manual security hassle. |
| **Centralized `tf/custom/` Install** | Installs cleanly into `tf/custom/P-REC/` for one-stop file management alongside your HUD and configs. | Keeps all your competitive files neatly organized in one folder. |

---

## 🏆 What This Adds for Strict League Rulesets

Competitive leagues enforce strict POV demo recording rules with severe penalties (default losses, point deductions, or bans for suspected cheating):

### 1. European TF2 League ([ETF2L Rule 2.1](https://rules.etf2l.org/docs/general-2/#21-every-player-has-to-record-demos))
* **The Problem:** ETF2L strictly mandates that demos must cover the entire match. If your game crashes or you drop and reconnect mid-game, Valve's built-in `ds_enable 3` will NOT resume recording because the tournament mode wasn't restarted. Furthermore, ETF2L strictly mandates capturing proof of all players' SteamIDs and SourceTV status.
* **What P-REC Adds:**
  * **Mid-match reconnect recovery:** Detects reconnections and sends `status` to verify match state, immediately resuming recording if the tournament match is in progress.
  * **Automated Status Screenshot:** Automatically triggers `status; jpeg` at match completion, saving the screenshot directly into your demo/screenshot folder with complete SteamID proof.

### 2. RGL.gg ([RGL Rule 1008.5](https://docs.rgl.gg/rules/global/1008/?h=pov+demos#1008_5-pov-and-stv-demos))
* **The Problem:** RGL mandates POV demos for all matches and requires them to be kept throughout the season. Accidental demo deletion or missed starts result in penalty points.
* **What P-REC Adds:**
  * Enforces `ds_autodelete 0` (preventing any automatic deletion).
  * Recognizes official RGL server config patterns (`rgl_6s`, `rgl_hl`, `rgl_7s`, `rgl_pt`) and `"Config Executed"` prints to arm and trigger recording seamlessly.
  * Applies the official `rgl` demo naming prefix.

### 3. ozfortress ([ozfortress POV Guide](https://docs.ozfortress.com/guides/pov_demo_recording/))
* **The Problem:** ozfortress servers run a server-side **Demo Checker** plugin (`sm_querycvar`) that queries client cvars upon connection, checking for `ds_enable 2/3` and `ds_autodelete 0`. If `ds_enable 0`, players receive warnings or penalties. However, `ds_enable 3` clutters hard drives with 45 minutes of pre-game warmup bloat.
* **What P-REC Adds:**
  * Keeps `ds_enable 3` set so your client passes all server-side `sm_querycvar` checks with flying colors.
  * The split second the live tournament countdown begins, P-REC issues `ds_stop; ds_record` to cleanly split the official match demo from the pre-game warmup!

### 4. Matcha.tf & CustomLander TF2 ([Matcha Rules](https://rules.matcha.tf/) & [CLTF2 Rule 3.3](https://docs.cltf2.com/))
* **What P-REC Adds:**
  * Native recognition of Asia/Pacific tournament configs (`matcha_6v6`, `matcha_hl`, `[Matcha]`) and CLTF2 configs (`cltf2_4s`, `cltf2_ultiduo`, `[CLTF2]`).
  * Automates demo naming prefixes (`matcha` / `cltf2`) and end-of-round screenshots for admin verifications.

---

## 🛠️ Interactive Setup & Configuration Auditor

P-REC includes an interactive setup wizard that configures everything in under 60 seconds:
```bash
# Run on Windows:
prec64.exe --install

# Or on Linux / Python:
python3 prec64.py --install
```

### What the Setup Wizard Does:
1. **Always Asks Where `/tf` Is Located:** Auto-detects common Steam directories across Windows and Linux, but always prompts you to confirm.
2. **Scans `/tf/custom/` for Conflicting Mods:**
   * Detects and removes PeachREC HUD animation loops (`hudanimations_peachrec.txt` and `hudanimations_manifest.txt` hooks) that cause game lag.
   * Cleans up legacy 32-bit `prec.dll` / `prec.vdf` files that cannot load on 64-bit TF2.
3. **Installs into `/tf/custom/P-REC/`:** Places the app, configs, and modular league rules in one tidy location.
4. **Discovers Modular League Profiles:** Displays all rulesets found in `leagues/*.json`.
5. **Auto-Generates Secure RCON Password:** If you don't already have DemoMan installed, it creates a secure random token.
6. **Audits `/tf/cfg/overrides/` and `/tf/cfg/` (Plus Subfolders):**
   * Discovers existing config files (`autoexec.cfg`, `game_overrides.cfg`, etc.).
   * **Explicitly asks whether to update configs in bulk or file-by-file (one by one)** with full diff previews.
   * Automatically creates `.cfg.bak` backups before modifying anything.
7. **Outputs Ready-to-Use Steam Launch Options!**

---

## 💻 Windows vs. Linux Support

| Platform | Download / Binary | How to Run |
| :--- | :--- | :--- |
| **Windows** | `prec64.exe` (Standalone Windows Executable) | Run `prec64.exe` directly or via Steam launch options wrapper. |
| **Linux** | `prec64` (Standalone Linux ELF Binary) or `prec64.py` | `chmod +x prec64 && ./prec64` or `python3 prec64.py` (requires 0 external dependencies!). |

> [!NOTE]
> An `.exe` file is a Windows Portable Executable and cannot run natively on Linux without Wine/Proton. For Linux gamers, use the native Linux binary (`prec64`) or run `python3 prec64.py` directly with your system's Python 3 installation!

---

## 🚀 Steam Launch Options & Auto-Boot

Add the following string to your TF2 Launch Options in Steam (**Right-click TF2 -> Properties -> General -> Launch Options**):

### Windows Launch Option:
```text
cmd /c start "" "H:\SteamLibrary\steamapps\common\Team Fortress 2\tf\custom\P-REC\prec64.exe" & %command% -condebug -usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
```

### Linux Launch Option:
```text
/home/user/.local/share/Steam/steamapps/common/Team\ Fortress\ 2/tf/custom/P-REC/prec64 & %command% -condebug -usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
```

---

## 📁 Modular League Rulesets (`leagues/*.json`)

All league rules are stored as independent JSON files in the [`leagues/`](file:///h:/prec/leagues/) directory:
* [`etf2l.json`](file:///h:/prec/leagues/etf2l.json)
* [`rgl.json`](file:///h:/prec/leagues/rgl.json)
* [`ozfortress.json`](file:///h:/prec/leagues/ozfortress.json)
* [`matcha.json`](file:///h:/prec/leagues/matcha.json)
* [`cltf2.json`](file:///h:/prec/leagues/cltf2.json)

### Instructions for Leagues / Tournament Organizers:
If you run a competitive TF2 league, tournament, or pug community (e.g. AsiaFortress, Pure League, Respawn League, United Gaming, etc.):

1. Copy `leagues/template.json` to `leagues/<your_league_id>.json`.
2. Configure your league's specific settings:
   ```json
   {
     "id": "myleague",
     "name": "My Tournament League",
     "rules_url": "https://myleague.com/rules",
     "prefix": "myleague",
     "ds_enable": 0,
     "ds_autodelete": 0,
     "ds_screens": 1,
     "mandatory_status_screenshot": true,
     "server_demo_checker_bypass": false,
     "server_config_patterns": [
       "myleague_(6v6|9v9)",
       "myleague.*config loaded"
     ],
     "chat_triggers": [
       "Match is LIVE",
       "Both teams are ready"
     ]
   }
   ```
3. Open a **Pull Request** on this repository!
   Once merged, all players using P-REC worldwide will immediately have native compliance with your league rules!

---

## 🤝 Contributing & Pull Requests Welcome!

**Community contributions and Pull Requests are strongly encouraged!**
* **League Admins:** Submit PRs adding or updating your league's JSON profile in `leagues/`.
* **Developers:** Feel free to open PRs for bug fixes, Linux packaging improvements, or feature enhancements.
* **HUD Authors & Players:** Report edge cases, chat trigger formats, or feedback via GitHub Issues.

---

## ⚙️ Configuration Reference @[PREC_Settings.cfg](file:///h:/prec/PREC_Settings.cfg)

| Convar / Alias | Default | Description |
| :--- | :--- | :--- |
| `prec_version` | `"1.0.0"` | Current configuration version. |
| `prec_league` | `"etf2l"` | Active league profile (`etf2l`, `rgl`, `ozfortress`, `matcha`, `cltf2`, `custom`). |
| `prec_mode` | `2` | `0` = Off, `1` = Custom named only, `2` = Record active tournament matches only, `3` = Record all matches. |
| `prec_dir` | `"demos"` | Folder inside `/tf/` where demo files are saved. |
| `prec_sound` | `1` | `1` = Audio cue on start/stop, `0` = Mute. |
| `prec_screens` | `1` | `1` = Capture status & scoreboard screenshot at match end (mandatory for ETF2L). |
| `prec_notify` | `1` | `0` = Console only, `1` = Team chat announcements, `2` = HUD notification. |
| `prec_delete_useless_demo` | `0` | `0` = Never delete (strictly required for league compliance). |
| `prec_tag` | `""` | Custom prefix tag for demo names (leave blank for league default). |
| `alias pr_message_start` | `say_team [P-REC] Recording started.` | Chat message sent when recording begins. |
| `alias pr_message_stop` | `say_team [P-REC] Stop recording.` | Chat message sent when recording ends. |
| `alias pr_message_mark` | `say_team [P-REC] Bookmark placed.` | Chat message sent when a bookmark is placed. |

---

## 🏗️ Building from Source

### Windows:
Run the provided build batch file:
```cmd
build_windows.bat
```
*(Uses PyInstaller to compile `prec64.exe` with bundled `leagues` profiles).*

### Linux:
Run the build shell script:
```bash
chmod +x build_linux.sh
./build_linux.sh
```
*(Uses PyInstaller to compile the standalone `prec64` ELF binary).*

### Automated CI/CD:
Every tagged commit (e.g. `v1.0.0`) automatically triggers [.github/workflows/build.yml](file:///h:/prec/.github/workflows/build.yml) on GitHub Actions to compile standalone binaries for both Windows and Linux!
