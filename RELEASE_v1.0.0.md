# GitHub Release v1.0.0 Template

**Release Tag:** `v1.0.0`  
**Release Title:** `P-REC External v1.0.0 — Zero-Lag Match Recorder for TF2 64-Bit (Windows & Linux)`

---

## 📦 Release Description (Copy & Paste below into GitHub Release Body)

```markdown
# P-REC External (v1.0.0)
### Zero-Lag, Zero-Warmup Automated Match Recorder for Team Fortress 2 (64-Bit Native)

---

### 💡 Why This Exists (The Vibecoded Backstory)
> *"I got completely fed up with **PeachREC being shit** (causing microstutters and frame drops with synchronous HUD animation loops) and the original **P-REC not working** on modern 64-bit TF2 without `-insecure` (which VAC bans match servers). So I vibecoded this companion for myself to have zero game lag, zero warmup bloat, and total competitive league compliance."*

⚠️ **Disclaimer:** This project is 100% completely vibecoded with AI. While it is architecturally **100% VAC-safe** (using official Source Engine RCON & Netcon loopback protocols without memory injection or DLL hooking), use at your own risk and test during scrims before major tournament matches!

---

## ⚡ Key Highlights in v1.0.0

* **0 FPS Drop / Zero Microstutters:** Runs 100% externally out-of-process. Zero HUD animation manifest hooks, zero VGUI modifications.
* **100% VAC-Safe:** Connects to TF2 via official engine sockets. Zero DLL injection or memory tampering.
* **Zero Warmup Bloat:** Listens to tournament countdown pulses and triggers recording strictly when the match goes live (no more 45-minute warmup demo files from `ds_enable 3`!).
* **🛡️ Windows System Tray (Hidden Pictograms):** Lives quietly in the notification area under Hidden Pictograms with the TF2 **Supreme Soviet** icon. Right-click to access Settings, Custom folder, toggle console visibility, or Close cleanly!
* **Zero Distracting Screen Pop-ups:** Zero desktop toast pop-ups, zero intrusive overlays, zero focus stealing. Clean alerts via team chat and audio cues.
* **⚡ Auto Profile Switching & Scrim Mode:** Auto-switches rulesets when match configs load; suppresses status screenshots and adds `_scrim` prefix during practice.
* **🔍 DemoMan Auto-Detection:** Automatically discovers local [DemoMan](https://github.com/DemomanApp/DemoMan) installations, extracts its active RCON password and pre-fills your TF2 `/tf` path!
* **Multi-League Strict Rule Compliance:**
  * **ETF2L (Rule 2.1):** Auto-captures mandatory player SteamID & SourceTV screenshots (`status; jpeg`) at match end; recovers from mid-match crashes and reconnects without losing demo coverage.
  * **AsiaFortress:** Full compliance with AsiaFortress Cup & League rules (`af_` tournament configs, mandatory POV demos, status screenshots).
  * **RGL (Rule 1008.5):** Mandatory POV demo recording, `rgl` prefixes, and `ds_autodelete 0` preservation.
  * **ozfortress:** Satisfies server-side `Demo Checker` plugin (`sm_querycvar` check for `ds_enable 3` & `ds_autodelete 0`), while cleanly splitting match demos from warmup on live countdown (`ds_stop; ds_record`).
  * **Matcha.tf & CLTF2:** Automated recording and league prefixes for Asia/Pacific and CustomLander competitions.
* **Interactive First-Time Setup Wizard:**
  * Prompts for your `/tf` folder with automatic path detection.
  * Scans `/tf/custom/` for interfering PeachREC animation files and legacy 32-bit plugins, cleaning them safely.
  * Installs directly into `tf/custom/P-REC/` for organized file management.
  * Audits `tf/cfg/overrides` and `tf/cfg/`, asking to apply settings file-by-file or in bulk.
  * Auto-generates cryptographically secure RCON passwords (or hooks into DemoMan port `27969`).
* **Modular League Profiles (`leagues/*.json`):** Third-party leagues can add their own rulesets simply by submitting a Pull Request!
* **Steam Launch Option Auto-Boot:** Launches seamlessly alongside TF2.
* **License:** Licensed under GNU General Public License v3.0 (GPL-3.0) — 100% free forever with complete liability disclaimer.

---

## 💻 Downloads & Platform Compatibility

| File | Platform | Notes |
| :--- | :--- | :--- |
| **`prec64.exe`** | **Windows** (64-bit) | Standalone Windows executable with embedded Supreme Soviet icon. Place in `tf/custom/P-REC/`. |
| **`prec64`** | **Linux** (64-bit) | Standalone Linux ELF binary (`chmod +x prec64`). |
| **`PREC_Settings.cfg`** | All | Configuration file with convars, tray settings, and chat message aliases. |
| **Source Code (`prec64.py`)** | All | Zero external dependencies; run with `python3 prec64.py`. |

> [!NOTE]
> **Windows vs. Linux:** An `.exe` file is a Windows executable and does not run natively on Linux. Linux players should download the native Linux binary `prec64` or run `python3 prec64.py` directly with Python 3.

---

## 🚀 Quick Installation

### Windows:
1. Download `prec64.exe` and `PREC_Settings.cfg`.
2. Run `prec64.exe --install` in a terminal/command prompt to run the 60-second setup wizard (or let it launch automatically on first run).
3. Add the outputted launch options to TF2 in Steam:
   ```text
   cmd /c start "" "C:\path\to\Team Fortress 2\tf\custom\P-REC\prec64.exe" & %command% -condebug -usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
   ```

### Linux:
1. Download `prec64` and `PREC_Settings.cfg`.
2. Make executable: `chmod +x prec64`
3. Run `./prec64 --install` to complete setup.
4. Add launch options to TF2 in Steam:
   ```text
   /path/to/tf/custom/P-REC/prec64 & %command% -condebug -usercon +rcon_password YOUR_PASSWORD +ip 0.0.0.0 +hostport 27969 +net_start
   ```

---

## 🤝 Calling All Leagues & Developers (Pull Requests Welcome!)

We encourage third-party leagues, tournament organizers, and community developers to contribute:
* **Add Your League:** Copy `leagues/template.json` to `leagues/<your_league>.json` and open a PR!
* **Bug Fixes & HUD Integrations:** Feel free to submit pull requests or report issues.

---

## 🙏 Credits & Acknowledgements

* **The Original P-REC:** Huge respect and credit to **Aethelred (Orange)** for creating the original [P-REC](https://github.com/Orange-TF2/p-rec) Source engine plugin that served the competitive TF2 community for over a decade.
* **PeachREC:** Thanks to **peaches** for [PeachREC](https://github.com/peaches-tf2/PeachREC) and demonstrating the competitive scene's demand for modern automated recording solutions following the 64-bit TF2 update.
* **DemoMan:** Credit to the [DemoMan](https://github.com/DemomanApp/DemoMan) developers for creating an awesome demo manager and modern TF2 ecosystem tool.
* **Competitive Leagues:** Respect to ETF2L, AsiaFortress, RGL.gg, ozfortress, Matcha.tf, and CLTF2 for keeping competitive Team Fortress 2 thriving worldwide.
```
