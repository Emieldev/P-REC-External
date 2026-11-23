# P-REC External v1.0.1 — Release Notes

[![Version: 1.0.1](https://img.shields.io/badge/Version-1.0.1-blue.svg)](https://github.com/Emieldev/P-REC-External/releases)
[![TF2 Architecture: 64-bit Native](https://img.shields.io/badge/TF2-64--bit%20Native-orange.svg)](https://github.com/Emieldev/P-REC-External)
[![Platform: Windows & Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg)](https://github.com/Emieldev/P-REC-External)
[![100% VAC-Safe](https://img.shields.io/badge/VAC-100%25%20Safe-brightgreen.svg)](https://github.com/Emieldev/P-REC-External)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

---

### 🚀 What's New in v1.0.1

This update focuses on eliminating in-game microstutters, fixing alt-tabbing/window popups, perfecting KOTH and map swap handling, and delivering rock-solid competitive consistency:

* **⚡ Zero Game Lag on Match Start (<20ms):**
  - Removed synchronous queries (`query_tournament_teams`, `query_player_name`) that blocked the engine thread when the countdown ended. Metadata queries are now offloaded to an asynchronous background worker.
  - Combined `ds_prefix` and `record` into a single atomic transmission, and batched in-game console notifications asynchronously ~40ms later so gameplay remains at max frame rate.
* **🛡️ Eliminated Flashing CMD Windows & Alt-Tabbing:**
  - Cached TF2 process parameters by PID to eliminate repeated WMI/PowerShell process inspection loops.
  - Enforced `0x08000000` (`CREATE_NO_WINDOW`) and `STARTUPINFO(wShowWindow=SW_HIDE)` across all background process invocations on Windows.
* **🎯 Fixed KOTH Auto-Recording Consistency:**
  - Added support for all tournament countdown formats (`The match will begin in \d+ seconds`, `The game will begin in \d+ seconds`), point unlock alerts, and KOTH config executions.
  - Added auto-recording fallback on native `World triggered "Round_Start"` in tournament mode to guarantee recording even if countdown text was skipped.
* **🔄 Fixed Map Swap & Stuck Recording:**
  - Added log listeners for `Server changing map`, `(?:Completed|Stopped)\s+demo`, and server disconnect/connect transitions.
  - On map change, active demos are cleanly stopped and the engine resets recording flags so it immediately arms for the next map's match countdown.
* **💀 Zero-Disruption Status Screenshots:**
  - Mandatory competitive status screenshots (`status; jpeg`) are now scheduled to capture during the player's respawn time upon death, eliminating mid-fight screenshot freezes.
  - Includes a safety fallback (~5m 30s) if the player does not die during the round.
* **🛡️ Non-SOAP Comp Servers & Manual SOAP Unload Handling:**
  - Priority logic ensures native Source Engine match countdowns take precedence over pregame SOAP DM unload events.
  - Full native support for competitive servers running without SOAP DM.

---

### 📥 Release Downloads
* **Windows (64-bit Standalone Executable):** [`prec64.exe`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.1/prec64.exe)
* **Linux (64-bit Standalone ELF Binary):** [`prec64`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.1/prec64)
* **Configuration File:** [`PREC_Settings.cfg`](https://github.com/Emieldev/P-REC-External/releases/download/v1.0.1/PREC_Settings.cfg)

📖 **Full Documentation & Configuration Reference:** See [README.md](https://github.com/Emieldev/P-REC-External/blob/main/README.md).

---

### 🙏 Credits
* **Oleg Koshmeliuk (Orange)** for the legendary original [P-REC (Pov-Record)](https://github.com/olegKoshmeliuk/Pov-Record) plugin.
* **peaches** for [PeachREC](https://github.com/peaches-tf2/PeachREC).
* **DemoMan** developers for the [DemoMan](https://github.com/DemomanApp/DemoMan) ecosystem.
* ETF2L, AsiaFortress, RGL.gg, ozfortress, Matcha.tf, and CLTF2 communities.
