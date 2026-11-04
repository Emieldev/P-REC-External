#!/usr/bin/env python3
"""
P-REC: Point-of-view Recording External Companion
(Precision Recording Engine for Competition)
A high-performance, zero-lag automated match recorder for Team Fortress 2 (64-bit).
Cross-Platform (Windows & Linux).

================================================================================
⚠️ DISCLAIMER:
This application is 100% COMPLETELY VIBECODED. Use at your own risk.
While it is 100% VAC-safe (uses official engine RCON/Netcon without memory injection
or DLL tampering), test it during scrims/practice before using in championship matches.
================================================================================

Advantages:
- Zero Game FPS Drops: Runs 100% externally. Touches 0 HUD animations and 0 VGUI panels.
- 100% VAC-Safe: Official Source RCON / Netcon protocols. Zero DLL injection.
- Zero Warmup Bloat: Records strictly when the tournament countdown starts.
- Multi-League Rule Compliance: Profiles for ETF2L, RGL, ozfortress, Matcha.tf, and CLTF2.
- Smart Setup & Audit:
  * Scans tf/cfg/overrides and tf/cfg/ (plus subfolders) with bulk or one-by-one approval.
  * Scans tf/custom for interfering mods (PeachREC HUD loops, legacy 32-bit plugins).
  * Always asks where /tf folder is located before installing.
- Auto-RCON Security: Auto-generates cryptographically secure passwords.
- Auto-Boots with TF2: Seamless Steam launch options wrapper.
"""

import os
import sys
import io
import time
import socket
import struct
import re
import json
import shutil
import threading
import secrets
import subprocess
import random
import urllib.request
from pathlib import Path

# In PyInstaller windowed / GUI mode on Windows, standard streams are None
if sys.stdin is None:
    sys.stdin = io.StringIO()
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()


def is_interactive() -> bool:
    """Safely checks if running in an interactive terminal with a valid stdin."""
    try:
        return bool(sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty())
    except Exception:
        return False

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

APP_NAME = "P-REC External"
APP_VERSION = "1.0.0"
APP_FULL_TITLE = f"P-REC External v{APP_VERSION}"
GITHUB_REPO = "Emieldev/P-REC-External"
DEFAULT_CONFIG_FILES = ["PREC_Settings.cfg"]

# ====================================================================
# Modular League Profiles (Fallbacks + Dynamic JSON Loader)
# ====================================================================

DEFAULT_LEAGUE_PROFILES = {
    "etf2l": {
        "id": "etf2l",
        "name": "European TF2 League (ETF2L)",
        "rules_url": "https://rules.etf2l.org/docs/general-2/#21-every-player-has-to-record-demos",
        "config_repo": "https://github.com/ETF2L/gameserver-configs",
        "prefix": "etf2l",
        "scrim_prefix": "etf2l_scrim",
        "ds_enable": 0,
        "ds_autodelete": 0,
        "ds_screens": 1,
        "mandatory_status_screenshot": True,
        "server_demo_checker_bypass": False,
        "server_config_patterns": [
            r"etf2l_(6v6|9v9|golden_cap|ultiduo|bball|scrim)",
            r"ETF2L config",
            r"config has been loaded"
        ],
        "chat_triggers": [
            r"Both teams are ready",
            r"Match is LIVE",
            r"All players are ready",
            r"\[SOAP\] (Soap DM|Plugins) unloaded",
            r"\[ProperPregame\] Class limits restored"
        ]
    },
    "asiafortress": {
        "id": "asiafortress",
        "name": "AsiaFortress (AF)",
        "rules_url": "https://docs.google.com/document/d/16D6nGRbq1ZafMtR1uBOfnvC3jJ4K4lPzqbrB6lqDQ74/edit?tab=t.0#heading=h.rdjxx5582d9w",
        "prefix": "af",
        "scrim_prefix": "af_scrim",
        "ds_enable": 0,
        "ds_autodelete": 0,
        "ds_screens": 1,
        "mandatory_status_screenshot": True,
        "server_demo_checker_bypass": False,
        "server_config_patterns": [
            r"af_(6v6|5cp|koth|golden_cap|scrim)",
            r"asiafortress.*",
            r"AsiaFortress"
        ],
        "chat_triggers": [
            r"Both teams are ready",
            r"Match is LIVE",
            r"All players are ready",
            r"\[SOAP\] (Soap DM|Plugins) unloaded",
            r"\[ProperPregame\] Class limits restored"
        ]
    },
    "rgl": {
        "id": "rgl",
        "name": "RGL.gg (North America)",
        "rules_url": "https://docs.rgl.gg/rules/global/1008/?h=pov+demos#1008_5-pov-and-stv-demos",
        "config_repo": "https://github.com/RGLgg/server-resources-updater",
        "prefix": "rgl",
        "scrim_prefix": "rgl_scrim",
        "ds_enable": 0,
        "ds_autodelete": 0,
        "ds_screens": 1,
        "mandatory_status_screenshot": False,
        "server_demo_checker_bypass": False,
        "server_config_patterns": [
            r"rgl_(6s|hl|7s|pt|cast)(_scrim)?",
            r"RGL (6s|HL|7s|Prolander).*(Config Executed|scrim)"
        ],
        "chat_triggers": [
            r"Both teams are ready",
            r"Match is LIVE",
            r"Config Executed"
        ]
    },
    "ozfortress": {
        "id": "ozfortress",
        "name": "ozfortress (Oceania)",
        "rules_url": "https://docs.ozfortress.com/guides/pov_demo_recording/",
        "config_repo": "https://github.com/ozfortress/server-configs",
        "prefix": "ozf",
        "scrim_prefix": "ozf_scrim",
        "ds_enable": 3,
        "ds_autodelete": 0,
        "ds_screens": 1,
        "mandatory_status_screenshot": False,
        "server_demo_checker_bypass": True,
        "server_config_patterns": [
            r"ozfortress_(6v6|hl|ultiduo)(_scrim)?",
            r"ozf-(6s|hl|ud|scrim)",
            r"ozfortress.*(config loaded|scrim)"
        ],
        "chat_triggers": [
            r"Both teams are ready",
            r"Match is LIVE"
        ]
    },
    "matcha": {
        "id": "matcha",
        "name": "Matcha.tf (Asia/Pacific)",
        "rules_url": "https://rules.matcha.tf/",
        "prefix": "matcha",
        "scrim_prefix": "matcha_scrim",
        "ds_enable": 0,
        "ds_autodelete": 0,
        "ds_screens": 1,
        "mandatory_status_screenshot": True,
        "server_demo_checker_bypass": False,
        "server_config_patterns": [
            r"matcha_(6v6|hl|koth|5cp|scrim)",
            r"\[Matcha\]"
        ],
        "chat_triggers": [
            r"Both teams are ready",
            r"Match is LIVE",
            r"\[Matcha\] Match live"
        ]
    },
    "cltf2": {
        "id": "cltf2",
        "name": "CustomLander TF2 (CLTF2)",
        "rules_url": "https://docs.cltf2.com/",
        "prefix": "cltf2",
        "scrim_prefix": "cltf2_scrim",
        "ds_enable": 0,
        "ds_autodelete": 0,
        "ds_screens": 1,
        "mandatory_status_screenshot": False,
        "server_demo_checker_bypass": False,
        "server_config_patterns": [
            r"cltf2_(4s|ultiduo|hl|koth|3cp|scrim)",
            r"\[CLTF2\]"
        ],
        "chat_triggers": [
            r"Both teams are ready",
            r"Match is LIVE",
            r"\[CLTF2\] Match live"
        ]
    },
    "custom": {
        "id": "custom",
        "name": "Custom / Casual / Mixes",
        "rules_url": "",
        "prefix": "custom",
        "scrim_prefix": "custom_scrim",
        "ds_enable": 0,
        "ds_autodelete": 0,
        "ds_screens": 1,
        "mandatory_status_screenshot": False,
        "server_demo_checker_bypass": False,
        "server_config_patterns": [],
        "chat_triggers": [
            r"Both teams are ready",
            r"Match is LIVE",
            r"All players are ready",
            r"\[SOAP\] (Soap DM|Plugins) unloaded",
            r"\[ProperPregame\] Class limits restored"
        ]
    }
}

def get_league_directories(tf_path=None):
    """Finds all potential directories hosting leagues/*.json."""
    dirs = [
        get_app_dir() / "leagues",
        Path.cwd() / "leagues",
    ]
    if getattr(sys, '_MEIPASS', None):
        dirs.append(Path(sys._MEIPASS) / "leagues")
    if tf_path:
        dirs.append(Path(tf_path) / "custom" / APP_NAME / "leagues")
    return [d for d in dirs if d.exists()]

def load_league_profiles(tf_path=None):
    """Loads all modular league profiles from disk with fallback to defaults."""
    profiles = dict(DEFAULT_LEAGUE_PROFILES)
    for l_dir in get_league_directories(tf_path):
        for json_file in l_dir.glob("*.json"):
            if json_file.name == "template.json":
                continue
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                l_id = data.get("id", json_file.stem).lower()
                profiles[l_id] = data
            except Exception as e:
                print(f"[LEAGUE] Could not load profile {json_file.name}: {e}", flush=True)
    return profiles

# ====================================================================
# Configuration Parser & Password Generator
# ====================================================================

class PrecConfig:
    def __init__(self, cfg_path="PREC_Settings.cfg"):
        self.cfg_path = Path(cfg_path)
        # League Profile
        self.prec_league = "etf2l"        # "etf2l", "rgl", "ozfortress", "matcha", "cltf2", "custom"

        # Recording & Demo Settings
        self.prec_mode = 2                # 0=off, 1=custom, 2=tournament live, 3=all
        self.prec_dir = "demos"
        self.prec_sound = 1
        self.prec_hide_to_tray = 1        # 1=Hide to system tray (hidden pictograms), 0=keep console open
        self.prec_desktop_shortcut = 1    # 1=Ensure desktop shortcut exists, 0=off
        self.prec_screens = 1             # Status & scoreboard screenshot on round/match end
        self.prec_notify = 1
        self.prec_min_streak = 3
        self.prec_kill_delay = 15
        self.prec_log = 0
        self.prec_delete_useless_demo = 0 # 0=never delete (mandatory across all leagues)
        self.prec_stv_status = 1
        self.prec_tag = ""
        self.prec_demo_name = "%date%_%time%_%map%_%red%_%blu%"

        # Chat Aliases
        self.pr_message_start = "say_team [P-REC] Recording started."
        self.pr_message_stop = "say_team [P-REC] Stop recording."
        self.pr_message_mark = "say_team [P-REC] Bookmark placed."

        # Connection Settings
        self.prec_connection_mode = "auto" # "auto", "netcon", or "rcon"
        self.prec_rcon_port = 27969
        self.prec_rcon_password = ""
        self.prec_server_rcon_passwords = []
        self.candidate_passwords = []
        self.prec_netcon_port = 2121
        self.prec_tf_path = ""

        self.load()

    def load(self):
        if not self.cfg_path.exists():
            print(f"[CONFIG] '{self.cfg_path}' not found, generating default configuration...", flush=True)
            self._generate_default_cfg()

        with open(self.cfg_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for line in lines:
            line_str = line.strip()
            if not line_str or line_str.startswith("//") or line_str.startswith("#"):
                continue

            if "//" in line_str:
                line_str = line_str.split("//")[0].strip()

            alias_match = re.match(r'^alias\s+([A-Za-z0-9_]+)\s+"?([^"]*)"?', line_str, re.I)
            if alias_match:
                name, val = alias_match.group(1).lower(), alias_match.group(2).strip()
                if name in ("pr_message_start", "prec_message_start", "rec_message_start"):
                    self.pr_message_start = val
                elif name in ("pr_message_stop", "prec_message_stop", "rec_message_stop"):
                    self.pr_message_stop = val
                elif name in ("pr_message_mark", "prec_message_mark", "rec_message_mark"):
                    self.pr_message_mark = val
                continue

            parts = re.split(r'\s+', line_str, maxsplit=1)
            if len(parts) == 2:
                key = parts[0].strip().lower()
                val = parts[1].strip().strip('"').strip("'")

                if key in ("prec_league", "league"):
                    self.prec_league = val.lower()
                elif key in ("prec_mode", "mode"):
                    self.prec_mode = int(val)
                elif key in ("prec_dir", "dir", "ds_dir"):
                    self.prec_dir = val
                elif key in ("prec_sound", "sound", "ds_sound"):
                    self.prec_sound = int(val)
                elif key in ("prec_popup", "popup"):
                    self.prec_popup = int(val)
                elif key in ("prec_hide_to_tray", "hide_to_tray", "prec_tray"):
                    self.prec_hide_to_tray = int(val)
                elif key in ("prec_desktop_shortcut", "desktop_shortcut"):
                    self.prec_desktop_shortcut = int(val)
                elif key in ("prec_screens", "screens", "ds_screens"):
                    self.prec_screens = int(val)
                elif key in ("prec_notify", "notify", "ds_notify"):
                    self.prec_notify = int(val)
                elif key in ("prec_min_streak", "min_streak", "ds_min_streak"):
                    self.prec_min_streak = int(val)
                elif key in ("prec_kill_delay", "kill_delay", "ds_kill_delay"):
                    self.prec_kill_delay = int(val)
                elif key in ("prec_log", "log", "ds_log"):
                    self.prec_log = int(val)
                elif key in ("prec_delete_useless_demo", "delete_useless_demo", "ds_autodelete"):
                    self.prec_delete_useless_demo = int(val)
                elif key in ("prec_stv_status", "stv_status"):
                    self.prec_stv_status = int(val)
                elif key in ("prec_tag", "tag"):
                    self.prec_tag = val
                elif key in ("prec_demo_name", "demo_name", "prec_naming_scheme", "naming_scheme", "prec_format"):
                    self.prec_demo_name = val
                elif key in ("prec_connection_mode", "connection_mode"):
                    self.prec_connection_mode = val.lower()
                elif key in ("prec_rcon_port", "rcon_port"):
                    self.prec_rcon_port = int(val)
                elif key in ("prec_rcon_password", "rcon_password"):
                    self.prec_rcon_password = val
                elif key in ("prec_server_rcon_passwords", "server_rcon_passwords", "prec_server_passwords"):
                    raw_pws = re.split(r'[,;\s]+', val)
                    self.prec_server_rcon_passwords = [p.strip() for p in raw_pws if p.strip()]
                elif key in ("prec_netcon_port", "netcon_port"):
                    self.prec_netcon_port = int(val)
                elif key in ("prec_tf_path", "tf_path"):
                    self.prec_tf_path = val

        # Harvest candidate passwords for RCON auto-healing and synchronization
        candidates = []
        if self.prec_rcon_password and self.prec_rcon_password.lower() not in ("changeme", "generate", ""):
            candidates.append(self.prec_rcon_password)
        for sp in self.prec_server_rcon_passwords:
            if sp and sp not in candidates:
                candidates.append(sp)

        # 1. Detect from running TF2 process commandline (+rcon_password <pw>)
        proc_pws = detect_process_rcon_passwords()
        for pp in proc_pws:
            if pp and pp not in candidates:
                candidates.append(pp)

        # 2. Detect from DemoMan leveldb
        demoman = detect_demoman_config()
        if demoman.get("rcon_password"):
            dp = demoman["rcon_password"]
            if dp and dp not in candidates:
                candidates.append(dp)

        # 3. Detect from local TF2 config files (e.g. autoexec.cfg aliases, serveme configs)
        tf_dir_for_scan = self.prec_tf_path or (str(demoman["tf_path"].resolve()) if demoman.get("tf_path") else None) or (str(detect_tf2_directory().resolve()) if detect_tf2_directory() else None)
        if tf_dir_for_scan:
            local_cfg_pws = discover_local_rcon_passwords(tf_dir_for_scan)
            for lp in local_cfg_pws:
                if lp and lp not in candidates:
                    candidates.append(lp)

        self.candidate_passwords = candidates

        # Auto-adopt active password from environment if not explicitly set
        if not self.prec_rcon_password or self.prec_rcon_password.lower() in ("changeme", "generate", ""):
            if candidates:
                self.prec_rcon_password = candidates[0]
                print(f"[RCON AUTO-SYNC] Synchronized active RCON password from environment: {self.prec_rcon_password}", flush=True)
            else:
                generated_pw = secrets.token_hex(6)
                self.prec_rcon_password = generated_pw
                self.candidate_passwords.append(generated_pw)
                print(f"[SECURITY] Using temporary session RCON password in memory: {generated_pw}", flush=True)

        if not self.prec_tf_path and demoman.get("tf_path"):
            self.prec_tf_path = str(demoman["tf_path"].resolve())

        print(f"[CONFIG] Loaded configuration from {self.cfg_path.resolve()}", flush=True)
        print(f"         League Profile: {self.prec_league.upper()} | Mode: {self.prec_mode} | Connection: {self.prec_connection_mode}", flush=True)



    def _generate_default_cfg(self):
        default_content = """// ====================================================================
// P-REC External — Settings & Configuration
// ====================================================================
// High-performance automated match recorder for Team Fortress 2 (64-bit).
// Works seamlessly with mastercomfig, m0rehud, and DemoMan.
// ====================================================================

// --------------------------------------------------------------------
// Engine Compatibility Aliases (Suppresses console warnings in TF2)
// --------------------------------------------------------------------
alias prec_league                ""
alias prec_mode                  ""
alias prec_dir                   ""
alias prec_sound                 ""
alias prec_screens               ""
alias prec_notify                ""
alias prec_tag                   ""
alias prec_demo_name             ""
alias prec_min_streak            ""
alias prec_kill_delay            ""
alias prec_log                   ""
alias prec_server_rcon_passwords ""

// --------------------------------------------------------------------
// 1. League Ruleset Profile
// --------------------------------------------------------------------
// Available Profiles:
//   - "etf2l"        : European TF2 League (Strict Rule 2.1 compliance)
//   - "rgl"          : RGL.gg North American League (Rule 1008.5 compliance)
//   - "ozfortress"   : Oceanic TF2 League (Demo Checker compliance)
//   - "asiafortress" : AsiaFortress Cup & League (af_ configs)
//   - "matcha"       : Matcha.tf Asia/Pacific League
//   - "cltf2"        : CustomLander TF2 (4v4, Ultiduo, Highlander)
//   - "custom"       : Custom user triggers
prec_league                "etf2l"

// --------------------------------------------------------------------
// 2. Recording Mode
// --------------------------------------------------------------------
// Modes:
//   3 = Record ALL matches (every map, round, and server automatically)
//   2 = Record tournament matches only (Auto-records when match goes LIVE - Default)
//   1 = Manual recording only (records on custom triggers/manual start)
//   0 = Disabled (turns off all demo recording)
prec_mode                  2

// --------------------------------------------------------------------
// 3. Demo Storage & Alerts
// --------------------------------------------------------------------
prec_dir                   "demos"
prec_sound                 1
prec_screens               1
prec_notify                1

// --------------------------------------------------------------------
// 4. Demo Naming Pattern
// --------------------------------------------------------------------
prec_tag                   ""
prec_demo_name             "%date%_%time%_%map%_%red%_%blu%"

// --------------------------------------------------------------------
// 5. Team Chat Messages (Configurable)
// --------------------------------------------------------------------
alias pr_message_start "say_team [P-REC] Recording started."
alias pr_message_stop  "say_team [P-REC] Stop recording."
alias pr_message_mark  "say_team [P-REC] Bookmark placed."

// --------------------------------------------------------------------
// 6. Killstreaks & Bookmarks (Optional)
// --------------------------------------------------------------------
prec_min_streak            3
prec_kill_delay            15
prec_log                   0

// --------------------------------------------------------------------
// 7. Server RCON / serveme.tf Synergy (Optional)
// --------------------------------------------------------------------
prec_server_rcon_passwords ""

sv_rcon_whitelist_address "127.0.0.1"
removeip 127.0.0.1
"""
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            f.write(default_content)


# ====================================================================
# Directory & Process Helpers (with DemoMan Auto-Detection)
# ====================================================================

def is_tf2_running():
    """
    Checks if Team Fortress 2 is currently running.
    Returns (running_bool, process_name, pid).
    """
    target_names = {
        "tf_win64.exe", "tf.exe", "hl2.exe",
        "tf_linux64", "hl2_linux", "tf"
    }
    if sys.platform == "win32":
        try:
            out = subprocess.check_output("tasklist /NH /FO CSV", shell=True).decode("latin1", "ignore")
            for line in out.splitlines():
                if line.strip():
                    parts = line.split(",")
                    pname = parts[0].strip('"').lower()
                    if pname in target_names or "tf_win64" in pname:
                        pid = parts[1].strip('"') if len(parts) > 1 else "?"
                        return True, pname, pid
        except Exception:
            pass
    else:
        try:
            out = subprocess.check_output(["pgrep", "-a", "tf"], text=True)
            for line in out.splitlines():
                parts = line.split(None, 1)
                pid = parts[0]
                cmd = parts[1] if len(parts) > 1 else ""
                if any(t in cmd.lower() for t in target_names):
                    return True, Path(cmd.split()[0]).name, pid
        except Exception:
            pass
    return False, None, None


def detect_demoman_config():
    """
    Detects if DemoMan is installed and automatically extracts:
    - RCON password
    - TF2 /tf path (from demoDirs in DemoMan leveldb)
    """
    candidates = []
    if sys.platform == "win32":
        local_app = os.environ.get("LOCALAPPDATA", "")
        app_data = os.environ.get("APPDATA", "")
        if local_app:
            candidates.append(Path(local_app) / "com.demomanapp.demoman/EBWebView/Default/Local Storage/leveldb")
            candidates.append(Path(local_app) / "demoman")
        if app_data:
            candidates.append(Path(app_data) / "com.demomanapp.demoman/EBWebView/Default/Local Storage/leveldb")
    else:
        home = Path.home()
        candidates.extend([
            home / ".local/share/com.demomanapp.demoman/localstorage/leveldb",
            home / ".config/com.demomanapp.demoman/localstorage/leveldb",
            home / ".local/share/demoman",
            home / ".config/demoman",
        ])

    found_pw = None
    found_tf = None

    for c in candidates:
        if not c.exists():
            continue
        files = list(c.glob("*.log")) + list(c.glob("*.ldb"))
        if not files and c.is_dir():
            files = list(c.rglob("*.log")) + list(c.rglob("*.ldb"))

        for f in files:
            try:
                data = f.read_bytes().decode("latin1", "ignore")
                m_pw = re.findall(r'rconPassword[\s\x00-\x1f]*"([^"]+)"', data)
                if m_pw:
                    found_pw = m_pw[-1]
                m_tf = re.findall(r'"([A-Za-z]:\\\\[^"]*?\\\\tf(?:\\\\[^"]*?)?)"', data)
                if m_tf:
                    cand_tf = Path(m_tf[-1].replace("\\\\", "\\"))
                    while cand_tf and cand_tf.name.lower() != "tf" and len(cand_tf.parents) > 0:
                        cand_tf = cand_tf.parent
                    if cand_tf and cand_tf.exists() and cand_tf.name.lower() == "tf":
                        found_tf = cand_tf
                m_tf_linux = re.findall(r'"(/[^"]+/tf(?:/[^"]*)?)"', data)
                if m_tf_linux:
                    cand_tf = Path(m_tf_linux[-1])
                    while cand_tf and cand_tf.name.lower() != "tf" and len(cand_tf.parents) > 0:
                        cand_tf = cand_tf.parent
                    if cand_tf and cand_tf.exists() and cand_tf.name.lower() == "tf":
                        found_tf = cand_tf
            except Exception:
                pass

    return {
        "installed": bool(found_pw or found_tf),
        "rcon_password": found_pw,
        "tf_path": found_tf
    }


def detect_process_rcon_passwords():
    """
    Extracts any active +rcon_password parameters from running TF2 processes.
    Supports Windows (Win32_Process) and Linux (/proc/<pid>/cmdline).
    """
    passwords = []
    if sys.platform == "win32":
        try:
            cmd = [
                "powershell", "-NoProfile", "-NonInteractive", "-Command",
                "Get-CimInstance Win32_Process -Filter \"name like 'tf%.exe' or name like 'hl2%.exe'\" | Select-Object -ExpandProperty CommandLine"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            if res.returncode == 0 and res.stdout:
                matches = re.findall(r'\+rcon_password\s+([^\s]+)', res.stdout)
                for m in matches:
                    clean = m.strip().strip('"').strip("'")
                    if clean and clean not in passwords:
                        passwords.append(clean)
        except Exception:
            pass
    else:
        try:
            tf_running, _, pid = is_tf2_running()
            if tf_running and pid:
                p_cmd = Path(f"/proc/{pid}/cmdline")
                if p_cmd.exists():
                    raw = p_cmd.read_bytes().replace(b"\x00", b" ").decode("utf-8", "ignore")
                    matches = re.findall(r'\+rcon_password\s+([^\s]+)', raw)
                    for m in matches:
                        clean = m.strip().strip('"').strip("'")
                        if clean and clean not in passwords:
                            passwords.append(clean)
        except Exception:
            pass
    return passwords


def discover_local_rcon_passwords(tf_path=None):
    """
    Scans local TF2 configuration files for configured or aliased rcon_password values
    (e.g., autoexec.cfg, PREC_Settings.cfg, serveme configs).
    """
    candidates = []
    if not tf_path:
        return candidates

    base = Path(tf_path)
    paths_to_check = [
        base / "cfg/overrides/autoexec.cfg",
        base / "cfg/autoexec.cfg",
        base / "cfg/user/autoexec.cfg",
        base / "custom/P-REC/cfg/PREC_Settings.cfg",
        base / "cfg/PREC_Settings.cfg",
    ]
    cfg_dir = base / "cfg"
    if cfg_dir.exists():
        for f in cfg_dir.glob("*.cfg"):
            fl = f.name.lower()
            if fl.startswith("serveme") or "rcon" in fl or "etf2l" in fl or "match" in fl:
                if f not in paths_to_check:
                    paths_to_check.append(f)

    for cp in paths_to_check:
        if cp.exists():
            try:
                content = cp.read_text(encoding="utf-8", errors="ignore")
                for line in content.splitlines():
                    matches = re.findall(r'rcon_password\s+["\']?([^"\'\s;]+)', line)
                    for pw in matches:
                        pw_clean = pw.strip()
                        if pw_clean and pw_clean.lower() not in ('""', "''", "changeme", "generate"):
                            if pw_clean not in candidates:
                                candidates.append(pw_clean)
            except Exception:
                pass
    return candidates


def get_app_dir():
    """Gets true directory whether running as a .py script or compiled PyInstaller binary."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def detect_tf2_directory():
    """Attempts to find the tf/ directory on Windows and Linux, checking DemoMan config first."""
    # 0. Check if running directly inside tf/custom/ or tf/
    try:
        app_dir = get_app_dir()
        curr = app_dir
        for _ in range(4):
            if curr and curr.name.lower() == "tf" and curr.exists():
                return curr
            if curr:
                curr = curr.parent
    except Exception:
        pass

    # 1. Prioritize path from DemoMan if present
    try:
        demoman = detect_demoman_config()
        if demoman.get("tf_path") and demoman["tf_path"].exists():
            return demoman["tf_path"]
    except Exception:
        pass

    # 2. Standard Steam locations
    home = Path.home()

    if sys.platform == "win32":
        common_paths = [
            Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Steam/steamapps/common/Team Fortress 2/tf",
            Path("C:/Steam/steamapps/common/Team Fortress 2/tf"),
            Path("D:/Steam/steamapps/common/Team Fortress 2/tf"),
            Path("D:/SteamLibrary/steamapps/common/Team Fortress 2/tf"),
            Path("E:/SteamLibrary/steamapps/common/Team Fortress 2/tf"),
            Path("F:/SteamLibrary/steamapps/common/Team Fortress 2/tf"),
        ]
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
            winreg.CloseKey(key)
            reg_tf = Path(steam_path) / "steamapps/common/Team Fortress 2/tf"
            if reg_tf.exists():
                return reg_tf
        except Exception:
            pass
    else:
        common_paths = [
            home / ".local/share/Steam/steamapps/common/Team Fortress 2/tf",
            home / ".steam/steam/steamapps/common/Team Fortress 2/tf",
            home / ".steam/root/steamapps/common/Team Fortress 2/tf",
            home / ".var/app/com.valvesoftware.Steam/.local/share/Steam/steamapps/common/Team Fortress 2/tf",
        ]

    for p in common_paths:
        if p.exists():
            return p
    return None


# ====================================================================
# Auto-Start Configuration (Windows Registry / Linux Autostart)
# ====================================================================

REG_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
REG_APP_NAME = "PRECExternal"


def is_startup_enabled() -> bool:
    """Checks whether P-REC External is set to start automatically on system boot/login."""
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN_KEY, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, REG_APP_NAME)
                return bool(val)
        except Exception:
            return False
    else:
        autostart_dir = Path.home() / ".config" / "autostart"
        desktop_file = autostart_dir / "prec64.desktop"
        return bool(desktop_file and desktop_file.exists())


def set_startup(enable: bool, exe_path: Path = None) -> bool:
    """Enables or disables autostart via Windows Registry or Linux desktop autostart."""
    if not exe_path:
        if getattr(sys, 'frozen', False):
            exe_path = Path(sys.executable).resolve()
        else:
            exe_path = Path(__file__).resolve()

    if sys.platform == "win32":
        # Clean any legacy vbs or bat in Startup folder to avoid antivirus false alarms
        try:
            appdata = os.environ.get("APPDATA", "")
            if appdata:
                startup_dir = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
                for legacy in (startup_dir / "prec64_autostart.vbs", startup_dir / "prec64.bat"):
                    if legacy.exists():
                        legacy.unlink()
        except Exception:
            pass

        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_RUN_KEY, 0, winreg.KEY_ALL_ACCESS) as key:
                if enable:
                    winreg.SetValueEx(key, REG_APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}" --tray')
                else:
                    try:
                        winreg.DeleteValue(key, REG_APP_NAME)
                    except FileNotFoundError:
                        pass
            return True
        except Exception as e:
            print(f"[STARTUP] Registry update error: {e}", flush=True)
            return False
    else:
        autostart_dir = Path.home() / ".config" / "autostart"
        desktop_file = autostart_dir / "prec64.desktop"
        if enable:
            try:
                autostart_dir.mkdir(parents=True, exist_ok=True)
                content = f"""[Desktop Entry]
Type=Application
Exec="{exe_path}" --tray
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name={APP_NAME}
Comment=TF2 Automated Match Recorder
"""
                with open(desktop_file, "w", encoding="utf-8") as f:
                    f.write(content)
                return True
            except Exception:
                return False
        else:
            if desktop_file and desktop_file.exists():
                try:
                    desktop_file.unlink()
                except Exception:
                    pass
            return True


# ====================================================================
# Single-Instance Lock (Prevent Dual Process Conflicts)
# ====================================================================

_single_instance_mutex = None


def acquire_single_instance_lock():
    global _single_instance_mutex
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            ERROR_ALREADY_EXISTS = 183
            _single_instance_mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\PREC64_SingleInstance_Mutex")
            if ctypes.windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
                print(f"[{APP_NAME}] Another instance of {APP_NAME} is already running in the background/system tray. Exiting duplicate.", flush=True)
                sys.exit(0)
        except Exception:
            pass


_ctrl_handler_ref = None


def setup_console_close_protection():
    """Intercepts terminal/cmd cross-out (CTRL_CLOSE_EVENT) so clicking 'X' detaches and hides to tray instead of exiting."""
    global _ctrl_handler_ref
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            PHANDLER_ROUTINE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

            def ctrl_handler(ctrl_type):
                if ctrl_type in (0, 2):  # CTRL_C_EVENT or CTRL_CLOSE_EVENT
                    h_con = ctypes.windll.kernel32.GetConsoleWindow()
                    if h_con:
                        ctypes.windll.user32.ShowWindow(h_con, 0)  # SW_HIDE
                    ctypes.windll.kernel32.FreeConsole()
                    return True
                return False

            _ctrl_handler_ref = PHANDLER_ROUTINE(ctrl_handler)
            ctypes.windll.kernel32.SetConsoleCtrlHandler(_ctrl_handler_ref, True)
        except Exception:
            pass


# ====================================================================
# Desktop Shortcut Support (Windows .lnk via PowerShell / Linux .desktop)
# ====================================================================

def get_desktop_path() -> Path:
    """Returns the user's Desktop directory across Windows and Linux."""
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            # CSIDL_DESKTOP = 0
            ctypes.windll.shell32.SHGetFolderPathW(None, 0, None, 0, buf)
            if buf.value:
                return Path(buf.value)
        except Exception:
            pass
        userprofile = os.environ.get("USERPROFILE")
        if userprofile and (Path(userprofile) / "Desktop").exists():
            return Path(userprofile) / "Desktop"
        return Path.home() / "Desktop"
    else:
        return Path.home() / "Desktop"


def get_desktop_shortcut_path() -> Path:
    """Returns the expected Desktop shortcut file path."""
    desktop = get_desktop_path()
    if sys.platform == "win32":
        return desktop / "P-REC External.lnk"
    else:
        return desktop / "prec64.desktop"


def create_desktop_shortcut(target_exe: Path = None) -> bool:
    """Creates a desktop shortcut for P-REC External with embedded icon and working directory."""
    if not target_exe:
        if getattr(sys, 'frozen', False):
            target_exe = Path(sys.executable).resolve()
        else:
            target_exe = Path(__file__).resolve()

    desktop_path = get_desktop_path()
    try:
        desktop_path.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    shortcut_file = get_desktop_shortcut_path()

    # Locate application icon
    icon_candidate = None
    app_dir = get_app_dir()
    for cand in (
        app_dir / "assets" / "supreme_soviet.ico",
        target_exe.parent / "assets" / "supreme_soviet.ico",
        Path(__file__).parent / "assets" / "supreme_soviet.ico" if "__file__" in globals() else None,
    ):
        if cand and cand.exists():
            icon_candidate = cand.resolve()
            break

    if sys.platform == "win32":
        try:
            workdir = target_exe.parent.resolve()
            if target_exe.suffix.lower() == ".py":
                exe_target = sys.executable
                arguments = f'"{target_exe.resolve()}"'
            else:
                exe_target = str(target_exe.resolve())
                arguments = ""

            icon_line = f"if (Test-Path '{icon_candidate}') {{ $s.IconLocation = '{icon_candidate}' }}" if icon_candidate else ""
            arg_line = f"$s.Arguments = '{arguments}'" if arguments else ""

            ps_script = f"""
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut('{shortcut_file.resolve()}')
$s.TargetPath = '{exe_target}'
{arg_line}
$s.WorkingDirectory = '{workdir}'
$s.Description = 'P-REC External - Zero-Lag Match Recorder for TF2'
{icon_line}
$s.Save()
"""
            res = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script], capture_output=True, text=True)
            if res.returncode == 0 and shortcut_file.exists():
                print(f"[SHORTCUT] Desktop shortcut created at: {shortcut_file.resolve()}", flush=True)
                return True
            else:
                print(f"[SHORTCUT] Failed to create shortcut: {res.stderr.strip()}", flush=True)
                return False
        except Exception as e:
            print(f"[SHORTCUT] Error creating shortcut: {e}", flush=True)
            return False
    else:
        # Linux .desktop entry
        try:
            exec_str = f'"{target_exe.resolve()}"' if target_exe.suffix.lower() != ".py" else f'{sys.executable} "{target_exe.resolve()}"'
            icon_str = str(icon_candidate.resolve()) if icon_candidate else ""
            content = f"""[Desktop Entry]
Type=Application
Name=P-REC External
Comment=Zero-Lag Match Recorder for TF2
Exec={exec_str}
Icon={icon_str}
Terminal=true
Categories=Game;
"""
            with open(shortcut_file, "w", encoding="utf-8") as f:
                f.write(content)
            shortcut_file.chmod(0o755)
            print(f"[SHORTCUT] Linux desktop shortcut created at: {shortcut_file.resolve()}", flush=True)
            return True
        except Exception as e:
            print(f"[SHORTCUT] Error creating Linux desktop shortcut: {e}", flush=True)
            return False


def ensure_desktop_shortcut(target_exe: Path = None) -> bool:
    """Ensures a desktop shortcut exists; if missing, creates it automatically."""
    shortcut_path = get_desktop_shortcut_path()
    if not shortcut_path.exists():
        return create_desktop_shortcut(target_exe)
    return True


# ====================================================================
# Conflict Scanner & Auditor (tf/custom and tf/cfg)
# ====================================================================

def scan_custom_conflicts(tf_path: Path):
    """Scans tf/custom/ for interfering mods like PeachREC loops and legacy 32-bit plugins."""
    custom_dir = tf_path / "custom"
    if not custom_dir.exists():
        return []

    conflicts = []

    # 1. PeachREC animation files
    for p in custom_dir.glob("**/hudanimations_peachrec.txt"):
        conflicts.append({
            "type": "peachrec_animation",
            "path": p,
            "desc": f"PeachREC animation loop in: {p.relative_to(tf_path)}"
        })

    # 2. PeachREC directories
    for p in custom_dir.glob("*PeachREC*"):
        if p.is_dir():
            conflicts.append({
                "type": "peachrec_dir",
                "path": p,
                "desc": f"PeachREC custom folder: {p.relative_to(tf_path)}"
            })

    # 3. PeachREC hooks in HUD manifests
    for p in custom_dir.glob("**/hudanimations_manifest.txt"):
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "hudanimations_peachrec" in content:
                conflicts.append({
                    "type": "peachrec_manifest",
                    "path": p,
                    "desc": f"HUD animation manifest hook referencing PeachREC: {p.relative_to(tf_path)}"
                })
        except Exception:
            pass

    # 4. Legacy 32-bit P-REC plugins
    for p in custom_dir.glob("**/addons/prec.vdf"):
        conflicts.append({
            "type": "legacy_vdf",
            "path": p,
            "desc": f"Legacy 32-bit P-REC addon manifest: {p.relative_to(tf_path)}"
        })

    for p in custom_dir.glob("**/addons/prec.dll"):
        conflicts.append({
            "type": "legacy_dll",
            "path": p,
            "desc": f"Legacy 32-bit prec.dll plugin (cannot load on VAC 64-bit): {p.relative_to(tf_path)}"
        })

    # 5. Root addons folder
    addons_dir = tf_path / "addons"
    if addons_dir.exists():
        for p in addons_dir.glob("*prec*"):
            conflicts.append({
                "type": "legacy_root_addon",
                "path": p,
                "desc": f"Legacy addon file in /tf/addons/: {p.name}"
            })

    return conflicts


def clean_conflict(conflict: dict):
    """Safely cleans up an interfering mod file or directory."""
    path = conflict["path"]
    c_type = conflict["type"]
    try:
        if c_type in ("peachrec_animation", "legacy_vdf", "legacy_dll", "legacy_root_addon"):
            if path.exists():
                path.unlink()
        elif c_type == "peachrec_dir":
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)
        elif c_type == "peachrec_manifest":
            if path.exists():
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                new_lines = [l for l in lines if "hudanimations_peachrec" not in l]
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
    except Exception as e:
        print(f"[CLEANUP ERROR] Could not clean {path}: {e}", flush=True)


def find_target_autoexec(tf_path: Path) -> Path:
    """
    Finds the single active autoexec.cfg for TF2.
    Prioritizes:
    1. tf/cfg/overrides/autoexec.cfg (mastercomfig / modern configs)
    2. tf/cfg/autoexec.cfg (standard TF2 location)
    If neither exists, targets overrides/autoexec.cfg if overrides/ exists,
    otherwise cfg/autoexec.cfg.
    Never creates multiple autoexec files and never targets game_overrides.cfg.
    """
    cfg_dir = tf_path / "cfg"
    overrides_auto = cfg_dir / "overrides" / "autoexec.cfg"
    standard_auto = cfg_dir / "autoexec.cfg"

    if overrides_auto.exists():
        return overrides_auto
    if standard_auto.exists():
        return standard_auto

    if (cfg_dir / "overrides").exists():
        return overrides_auto
    return standard_auto


def clean_legacy_peachrec_configs(tf_path: Path):
    """
    Scans tf/cfg/ to detect conflicting PeachREC lines without modifying any existing cfg files.
    """
    cfg_dir = tf_path / "cfg"
    if not cfg_dir.exists():
        return
    for p in cfg_dir.glob("**/*.cfg"):
        if "prec" in p.name.lower() or "settings" in p.name.lower():
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if re.search(r'^\s*exec\s+peachrec', content, re.MULTILINE | re.I):
                print(f"[AUDIT] Notice: Legacy 'exec peachrec' found in: {p.relative_to(tf_path)} (leaving file unchanged).", flush=True)
        except Exception:
            pass


def get_recommended_snippet(cfg_filename="PREC_Settings.cfg"):
    return f"""// ==========================================================
// P-REC: Point-of-view Recording External Companion
// ==========================================================
ds_enable 0              // Manual mode: P-REC auto-triggers ds_record on live countdown
ds_dir "demos"           // Save folder
ds_notify 1              // Chat notifications
ds_sound 1               // Audio cue on start/stop
ds_screens 1             // Screenshot at match end (ETF2L compliance)
ds_autodelete 0          // CRITICAL: League compliance, never delete match demos
bind "F8" "ds_mark"      // Optional bookmark key
sv_rcon_whitelist_address "127.0.0.1" // Prevent localhost from being banned by Source engine
removeip 127.0.0.1       // Clear any temporary localhost ban
exec {cfg_filename}   // Load P-REC chat message aliases
"""


def apply_cfg_update(cfg_path: Path, cfg_filename="PREC_Settings.cfg"):
    """Applies optimal recording settings and comments out conflicting peachrec commands."""
    snippet = get_recommended_snippet(cfg_filename)

    existing_content = ""
    if cfg_path.exists():
        # Create backup
        backup_path = cfg_path.with_suffix(".cfg.bak")
        try:
            shutil.copy2(cfg_path, backup_path)
        except Exception:
            pass

        with open(cfg_path, "r", encoding="utf-8", errors="ignore") as f:
            existing_content = f.read()

    # Comment out conflicting PeachREC lines
    updated = re.sub(r'^(exec\s+peachrec.*)', r'// \1 (disabled for P-REC)', existing_content, flags=re.MULTILINE | re.I)

    # Avoid duplicate snippet if already present
    if "ds_autodelete" not in updated and "P-REC" not in updated:
        if updated and not updated.endswith("\n"):
            updated += "\n"
        updated += snippet

    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(updated)


def clean_autoexec_prec(tf_path: Path):
    """Safely cleans P-REC lines and commands from active autoexec.cfg."""
    if not tf_path:
        return
    autoexec = find_target_autoexec(tf_path)
    if not autoexec or not autoexec.exists():
        return
    try:
        lines = autoexec.read_text(encoding="utf-8", errors="ignore").splitlines()
        filtered = []
        skip_prec_block = False
        for line in lines:
            if "P-REC" in line and ("MATCH RECORDER" in line or "Recording External Companion" in line or "=====" in line):
                skip_prec_block = True
                continue
            if skip_prec_block:
                if line.strip() == "" or line.startswith("//") or "exec" in line.lower() or "ds_" in line.lower() or "sv_rcon" in line.lower() or "removeip" in line.lower() or "ds_mark" in line.lower():
                    if "exec" in line.lower() and ("prec_settings" in line.lower() or "settings.cfg" in line.lower()):
                        skip_prec_block = False
                    continue
                else:
                    skip_prec_block = False

            if re.search(r'^\s*exec\s+(?:PREC_Settings|Settings)\.cfg', line, re.I):
                continue
            if re.search(r'^\s*bind\s+["\']?F8["\']?\s+["\']?ds_mark["\']?', line, re.I):
                continue
            if re.search(r'^\s*sv_rcon_whitelist_address\s+["\']?127\.0\.0\.1["\']?', line, re.I):
                continue
            if re.search(r'^\s*removeip\s+127\.0\.0\.1', line, re.I):
                continue

            m = re.match(r'^\s*//\s*(exec\s+peachrec.*)\s*\(disabled for P-REC\)', line, re.I)
            if m:
                filtered.append(m.group(1))
                continue

            filtered.append(line)

        cleaned_text = "\n".join(filtered)
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text).strip() + "\n"
        autoexec.write_text(cleaned_text, encoding="utf-8")
        print(f"[UNINSTALL] Cleaned P-REC entries from: {autoexec}", flush=True)
    except Exception as e:
        print(f"[UNINSTALL] Note: Could not update autoexec: {e}", flush=True)


def show_manual_cfg_instructions(cfg_file: Path, cfg_filename="PREC_Settings.cfg", tf_path: Path = None):
    """
    Displays explicit manual configuration instructions for a declined file,
    including what lines to remove and what lines to add, and waits for user confirmation.
    """
    rel = cfg_file.name
    if tf_path:
        try:
            rel = str(cfg_file.relative_to(tf_path))
        except Exception:
            pass

    print("\n" + "=" * 65, flush=True)
    print(f" [MANUAL CONFIGURATION REQUIRED] {rel}", flush=True)
    print("=" * 65, flush=True)
    print(f"Target Config File: {cfg_file.resolve()}\n", flush=True)
    print("Because automatic configuration was declined, you must update this file manually:", flush=True)
    print("\n1. LINES TO REMOVE (if present in the file):", flush=True)
    print("   - Any PeachREC commands (causing main-thread stutter):", flush=True)
    print("       exec peachrec", flush=True)
    print("       hudanimations_peachrec.txt", flush=True)
    print("   - Any legacy 32-bit plugin loaders (causes VAC server errors):", flush=True)
    print("       plugin_load prec", flush=True)
    print("       plugin_load ../bin/prec", flush=True)
    print("\n2. LINES TO ADD (paste at the bottom of the file):", flush=True)
    print("-" * 65, flush=True)
    print(get_recommended_snippet(cfg_filename).strip(), flush=True)
    print("-" * 65 + "\n", flush=True)

    if is_interactive():
        while True:
            confirm = input(f"Have you made and saved these changes to '{rel}' manually? [y/N]: ").strip().lower()
            if confirm == 'y':
                print(f"[OK] Confirmed manual changes for {rel}!\n", flush=True)
                break
            elif confirm == 'skip':
                print(f"[SKIP] Proceeding without manual verification for {rel}.\n", flush=True)
                break
            else:
                print(f"[WAIT] Please open '{cfg_file.resolve()}', apply the changes, save the file, then enter 'y' to continue (or 'skip').", flush=True)


# ====================================================================
# Auto-Update Detection & Self-Updater
# ====================================================================

def parse_semver(ver_str: str):
    """Extracts numeric tuple (major, minor, patch) from version string (e.g. 'v1.0.1' -> (1, 0, 1))."""
    nums = re.findall(r'\d+', str(ver_str))
    return tuple(map(int, nums)) if nums else (0, 0, 0)


def check_for_updates(interactive=True) -> dict:
    """
    Checks GitHub API for a newer release version.
    If a newer release is detected:
      - In interactive mode: displays release notes and prompts user to auto-download and update.
      - In non-interactive mode: returns release info dict for background notification.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    headers = {
        "User-Agent": f"P-REC-External-Updater/{APP_VERSION}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return {}

    remote_tag = data.get("tag_name", "")
    remote_ver = parse_semver(remote_tag)
    current_ver = parse_semver(APP_VERSION)

    if remote_ver <= current_ver:
        return {}

    release_name = data.get("name") or remote_tag
    html_url = data.get("html_url", f"https://github.com/{GITHUB_REPO}/releases/latest")
    assets = data.get("assets", [])

    print("\n" + "=" * 65, flush=True)
    print(f" [UPDATE AVAILABLE] A new version of {APP_NAME} is available!", flush=True)
    print(f"   Latest Release:  {remote_tag} ({release_name})", flush=True)
    print(f"   Current Version: v{APP_VERSION}", flush=True)
    print(f"   Release Notes:   {html_url}", flush=True)
    print("=" * 65, flush=True)

    if not interactive or not is_interactive():
        return {
            "version": remote_tag,
            "name": release_name,
            "url": html_url,
            "assets": assets
        }

    is_win = sys.platform == "win32"
    asset_name = "prec64.exe" if is_win else "prec64"
    target_asset = next((a for a in assets if a.get("name") == asset_name), None)

    prompt = f"Would you like to automatically download and update to {remote_tag} now? [Y/n]: "
    user_choice = input(prompt).strip().lower()

    if user_choice == 'n':
        print("[UPDATE] Update deferred. You can update later from GitHub.\n", flush=True)
        return {"version": remote_tag, "url": html_url}

    if not target_asset or not target_asset.get("browser_download_url"):
        print(f"[UPDATE] Direct binary '{asset_name}' not found in release assets.", flush=True)
        print(f"Please download the update manually from: {html_url}\n", flush=True)
        return {"version": remote_tag, "url": html_url}

    download_url = target_asset["browser_download_url"]
    file_size = target_asset.get("size", 0)
    print(f"[UPDATE] Downloading {asset_name} ({file_size // 1024} KB)...", flush=True)

    current_bin = Path(sys.executable) if getattr(sys, 'frozen', False) else Path(__file__).resolve()
    temp_download = current_bin.with_suffix(".new")

    try:
        req_dl = urllib.request.Request(download_url, headers={"User-Agent": f"P-REC-External-Updater/{APP_VERSION}"})
        with urllib.request.urlopen(req_dl) as resp_dl, open(temp_download, "wb") as f_out:
            shutil.copyfileobj(resp_dl, f_out)

        if not is_win:
            os.chmod(temp_download, 0o755)

        if is_win:
            old_backup = current_bin.with_suffix(".old")
            if old_backup.exists():
                try:
                    old_backup.unlink()
                except Exception:
                    pass
            os.rename(current_bin, old_backup)
            os.rename(temp_download, current_bin)
        else:
            os.replace(temp_download, current_bin)

        print("\n" + "=" * 65, flush=True)
        print(f" [SUCCESS] Successfully updated {APP_NAME} to {remote_tag}!", flush=True)
        print(" Restarting application with the updated version...", flush=True)
        print("=" * 65 + "\n", flush=True)

        subprocess.Popen([str(current_bin)] + sys.argv[1:])
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Auto-update failed: {e}", flush=True)
        print(f"Please manually download the update from: {html_url}\n", flush=True)
        if temp_download.exists():
            try:
                temp_download.unlink()
            except Exception:
                pass

    return {"version": remote_tag, "url": html_url}


# ====================================================================
# Interactive First-Time Installation Wizard
# ====================================================================

def run_setup_wizard():
    # Check for latest releases before beginning setup
    if is_interactive():
        check_for_updates(interactive=True)

    print("\n" + "=" * 65, flush=True)
    print(f"      {APP_FULL_TITLE}       ", flush=True)
    print("      Interactive Setup & Configuration Wizard       ", flush=True)
    print("=" * 65, flush=True)
    print("Welcome! Let's get your zero-lag match recorder installed.\n", flush=True)

    # 0. Check DemoMan Installation
    demoman = detect_demoman_config()
    if demoman.get("installed"):
        print("=" * 65, flush=True)
        print(" [DEMOMAN DETECTED] Found existing DemoMan installation!", flush=True)
        if demoman.get("tf_path"):
            print(f"  * Auto-detected /tf folder:   {demoman['tf_path']}", flush=True)
        if demoman.get("rcon_password"):
            print(f"  * Auto-detected RCON token:  {demoman['rcon_password']}", flush=True)
        print("=" * 65 + "\n", flush=True)

    # 1. ALWAYS ask where the /tf directory is (with auto-detected default)
    detected = demoman.get("tf_path") or detect_tf2_directory()
    tf_path = None

    while True:
        print("Please specify your Team Fortress 2 '/tf' folder:", flush=True)
        if detected:
            print(f"  [Auto-Detected]: {detected}", flush=True)
            prompt = "  Press Enter to accept detected path, or enter custom /tf path: "
        else:
            prompt = "  Enter full path to your /tf folder: "

        if not is_interactive():
            tf_path = detected or Path("C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf")
            break

        user_input = input(prompt).strip()
        if not user_input and detected:
            tf_path = Path(detected)
            break
        elif user_input:
            cand = Path(user_input.strip('"').strip("'"))
            if cand.exists() and (cand.name.lower() == "tf" or (cand / "cfg").exists() or (cand / "custom").exists()):
                tf_path = cand
                print(f"[OK] Valid TF2 directory confirmed: {tf_path.resolve()}\n", flush=True)
                break
            else:
                print("[ERROR] Path is not a valid TF2 '/tf' folder (must contain 'cfg' or 'custom'). Try again.\n", flush=True)

    # 2. Scan tf/custom for interfering mods (PeachREC HUD loops, legacy plugins)
    print("\n[AUDIT] Scanning /tf/custom/ for interfering mods...", flush=True)
    custom_conflicts = scan_custom_conflicts(tf_path)
    if custom_conflicts:
        print("-" * 65, flush=True)
        print(f"[WARNING] Found {len(custom_conflicts)} interfering mod element(s) in /tf/custom/:", flush=True)
        for idx, c in enumerate(custom_conflicts, 1):
            print(f"  [{idx}] {c['desc']}", flush=True)
        print("-" * 65, flush=True)
        print("Note: PeachREC's HUD animation loops cause severe in-game microstutters.", flush=True)
        if is_interactive():
            do_clean = input("Would you like to automatically clean up these interfering files? [Y/n]: ").strip().lower()
        else:
            do_clean = "y"

        if do_clean != 'n':
            for c in custom_conflicts:
                clean_conflict(c)
            print("[OK] Interfering mod elements cleaned up successfully!\n", flush=True)
    else:
        print("[OK] No conflicting mods found in /tf/custom/.\n", flush=True)

    # 3. Target installation directories
    # Note: Installing application executables inside steamapps/common/ causes Discord
    # and game overlays to falsely report you as playing Team Fortress 2.
    # Therefore, we install the binary in a dedicated program folder outside Steam,
    # and keep PREC_Settings.cfg inside tf/custom/P-REC/cfg/ where TF2 loads it.
    if sys.platform == "win32":
        local_appdata = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local"))
        app_install_dir = Path(local_appdata) / "Programs/P-REC"
    else:
        app_install_dir = Path.home() / ".local/share/P-REC"

    app_install_dir.mkdir(parents=True, exist_ok=True)
    custom_cfg_dir = tf_path / "custom/P-REC"
    custom_cfg_dir.mkdir(parents=True, exist_ok=True)
    target_dir = app_install_dir

    # Automatically purge legacy binaries from steamapps/common/.../P-REC/ to stop Discord false detection
    for old_exe in (custom_cfg_dir / "prec64.exe", custom_cfg_dir / "prec64"):
        if old_exe.exists():
            try:
                old_exe.unlink()
            except Exception:
                pass

    print(f"Target program directory: {app_install_dir.resolve()}", flush=True)
    print(f"Target settings directory: {custom_cfg_dir.resolve()}", flush=True)

    # 4. Check for existing PREC_Settings.cfg / Settings.cfg to preserve user settings
    existing_cfg = None
    for cand_name in DEFAULT_CONFIG_FILES:
        for cand_dir in (custom_cfg_dir, custom_cfg_dir / "cfg", target_dir, get_app_dir(), tf_path / "cfg"):
            cand = cand_dir / cand_name
            if cand.exists():
                existing_cfg = cand.resolve()
                break
        if existing_cfg:
            break

    if existing_cfg:
        print("=" * 65, flush=True)
        print(" [EXISTING CONFIGURATION DETECTED]", flush=True)
        print(f" Found: {existing_cfg}", flush=True)
        print(" Keeping all your existing settings intact (file will NOT be edited or overwritten).", flush=True)
        print("=" * 65 + "\n", flush=True)
        cfg_target = existing_cfg
        loaded_cfg = PrecConfig(existing_cfg)
        selected_league = loaded_cfg.prec_league
        rcon_pw = loaded_cfg.prec_rcon_password

        # Ensure TF2 can locate this config if located inside a custom folder
        if "custom" in [p.lower() for p in existing_cfg.parts]:
            try:
                mirror_dir = existing_cfg.parent / "cfg"
                mirror_dir.mkdir(parents=True, exist_ok=True)
                mirror_file = mirror_dir / existing_cfg.name
                if not mirror_file.exists():
                    shutil.copy2(existing_cfg, mirror_file)
            except Exception:
                pass
    else:
        # 4. Choose League Profile (Modular JSON profiles)
        discovered_leagues = load_league_profiles(tf_path)
        print("\nSelect your primary competitive league profile (modular JSON ruleset):", flush=True)
        league_keys = list(discovered_leagues.keys())
        for idx, l_key in enumerate(league_keys, 1):
            l_info = discovered_leagues[l_key]
            print(f"  [{idx}] {l_info.get('name', l_key.upper())} ({l_key})", flush=True)

        if is_interactive():
            choice = input(f"Enter choice [1-{len(league_keys)}, default 1]: ").strip()
            try:
                choice_idx = int(choice) - 1
                selected_league = league_keys[choice_idx] if 0 <= choice_idx < len(league_keys) else "etf2l"
            except Exception:
                selected_league = "etf2l"
        else:
            selected_league = "etf2l"
        print(f"[OK] Selected league: {selected_league.upper()}\n", flush=True)

        # 5. RCON Configuration
        rcon_pw = ""
        if demoman.get("rcon_password"):
            d_pw = demoman["rcon_password"]
            print(f"[DEMOMAN] Automatically detected DemoMan RCON password: '{d_pw}'", flush=True)
            if is_interactive():
                use_demo = input(f"Adopt DemoMan's password ({d_pw})? [Y/n]: ").strip().lower()
                if use_demo != 'n':
                    rcon_pw = d_pw
            else:
                rcon_pw = d_pw

        if not rcon_pw and is_interactive():
            has_rcon = input("Do you already have an existing RCON password? [y/N]: ").strip().lower()
            if has_rcon == 'y':
                rcon_pw = input("Enter your existing RCON password: ").strip()

        if not rcon_pw:
            rcon_pw = secrets.token_hex(6)
            print(f"[SECURITY] Generated secure random RCON password: {rcon_pw}", flush=True)

        # 6. Write PREC_Settings.cfg to custom_cfg_dir (new file only)
        cfg_target = custom_cfg_dir / "PREC_Settings.cfg"
        write_wizard_config(cfg_target, selected_league, rcon_pw, str(tf_path.resolve()))
        print(f"[OK] Configuration saved: {cfg_target.resolve()}", flush=True)

    # 7. Copy binary / script & leagues directory into app_install_dir
    current_exe = Path(sys.executable) if getattr(sys, 'frozen', False) else get_app_dir() / "prec64.py"
    if target_dir != get_app_dir() and current_exe.exists():
        try:
            dest_file = target_dir / current_exe.name
            shutil.copy2(current_exe, dest_file)
            print(f"[OK] Installed application binary to: {dest_file.resolve()}", flush=True)
        except Exception as e:
            print(f"[INFO] Using application from: {current_exe.resolve()} ({e})", flush=True)

    src_leagues = get_app_dir() / "leagues"
    if src_leagues.exists() and target_dir != get_app_dir():
        dest_leagues = target_dir / "leagues"
        try:
            shutil.copytree(src_leagues, dest_leagues, dirs_exist_ok=True)
            print(f"[OK] Installed modular league profiles to: {dest_leagues.resolve()}", flush=True)
        except Exception as e:
            print(f"[INFO] Using built-in league profiles ({e})", flush=True)

    # 8. Detect and update the single active autoexec.cfg
    print("\n[AUDIT] Locating your active autoexec.cfg in tf/cfg/...", flush=True)
    target_autoexec = find_target_autoexec(tf_path)
    rel_auto = target_autoexec.relative_to(tf_path)
    status_str = "Pre-existing file" if target_autoexec.exists() else "Will be created"

    # Safely clean legacy PeachREC loops from all configs
    clean_legacy_peachrec_configs(tf_path)

    print("=" * 65, flush=True)
    print(f"Target Primary Autoexec: {rel_auto} ({status_str})", flush=True)
    print(f"Path: {target_autoexec.resolve()}", flush=True)
    print("=" * 65, flush=True)

    # Check if target autoexec already contains P-REC configuration
    already_configured = False
    if target_autoexec.exists():
        try:
            with open(target_autoexec, "r", encoding="utf-8", errors="ignore") as f:
                autoexec_text = f.read()
            if cfg_target.name.lower() in autoexec_text.lower() or "exec prec_settings" in autoexec_text.lower() or ("p-rec" in autoexec_text.lower() and "ds_autodelete" in autoexec_text.lower()):
                already_configured = True
        except Exception:
            pass

    if already_configured:
        print(f"[OK] Active autoexec '{rel_auto}' already contains P-REC configuration!", flush=True)
        print("     Skipping configuration prompt (no duplicate lines needed).\n", flush=True)
    else:
        print("P-REC External only needs to load once in your primary autoexec.", flush=True)
        print("It will NOT touch game_overrides.cfg or create duplicate configs.\n", flush=True)
        print("Proposed addition:\n" + get_recommended_snippet(cfg_target.name), flush=True)

        if is_interactive():
            ans = input(f"Add optimal P-REC settings to {rel_auto}? [Y/n]: ").strip().lower()
        else:
            ans = "n" if target_autoexec.exists() else "y"

        if ans != "n":
            apply_cfg_update(target_autoexec, cfg_target.name)
            print(f"[OK] Successfully configured {rel_auto}!\n", flush=True)
        else:
            print(f"[SKIP] Automatic update declined for {rel_auto}.", flush=True)
            show_manual_cfg_instructions(target_autoexec, cfg_target.name, tf_path)

    # 9. Auto-Start Configuration
    if sys.platform == "win32":
        run_exe = target_dir / ("prec64.exe" if getattr(sys, 'frozen', False) else "prec64.py")
    else:
        run_exe = target_dir / "prec64"

    if is_interactive():
        print("=" * 65, flush=True)
        print(" [SYSTEM STARTUP]", flush=True)
        print("=" * 65, flush=True)
        os_label = "Windows" if sys.platform == "win32" else "system login"
        print(f"P-REC External can start silently in the background when {os_label} boots.", flush=True)
        print("This means you never have to remember to launch it manually before playing TF2.", flush=True)
        ans = input(f"Start P-REC External automatically with {os_label}? [Y/n]: ").strip().lower()
        if ans in ("", "y", "yes"):
            set_startup(True, run_exe.resolve())
            print(f"[OK] Auto-start enabled! P-REC will start silently on {os_label} boot.\n", flush=True)
        else:
            set_startup(False)
            print("[INFO] Auto-start not enabled.\n", flush=True)

    # 10. Desktop Shortcut Creation
    print("=" * 65, flush=True)
    print(" [DESKTOP SHORTCUT]", flush=True)
    print("=" * 65, flush=True)
    print("P-REC External can place a shortcut on your Desktop for easy access.", flush=True)
    if is_interactive():
        ans = input("Create a desktop shortcut for P-REC External? [Y/n]: ").strip().lower()
        make_shortcut = ans not in ("n", "no")
    else:
        make_shortcut = True

    if make_shortcut:
        if create_desktop_shortcut(run_exe.resolve()):
            print("[OK] Desktop shortcut created successfully on your Desktop!\n", flush=True)
        else:
            print("[INFO] Could not create desktop shortcut.\n", flush=True)

    # 11. Output Steam Launch Options (Both RCON and Netcon)
    print("=" * 65, flush=True)
    print("             SETUP COMPLETE! STEAM LAUNCH OPTIONS:             ", flush=True)
    print("=" * 65, flush=True)
    print("Add EITHER of these to the end of your existing Launch Options", flush=True)
    print("in Steam (Right-click Team Fortress 2 in Steam -> Properties):\n", flush=True)
    print("[Option 1: RCON Mode] (Recommended - identical to DemoMan):", flush=True)
    print(f"  -usercon +rcon_password {rcon_pw} +ip 0.0.0.0 +hostport 27969 +net_start\n", flush=True)
    print("  * If you already run DemoMan, you already have this in Steam!", flush=True)
    print("  💡 SERVEME.TF & SERVER RCON SYNERGY:", flush=True)
    print("    TF2 uses 'rcon_password' for BOTH outgoing server rcon and local listen rcon.", flush=True)
    print("    For the best experience, configure your serveme.tf account's default RCON password", flush=True)
    print(f"    to match your launch option ('{rcon_pw}').", flush=True)
    print("    P-REC External also features Auto-Healing RCON: if you ever switch rcon_password in-game", flush=True)
    print("    to run server commands, P-REC automatically re-authenticates in <1ms without dropping recording!\n", flush=True)
    print("[Option 2: Netcon Mode] (Ultra-short, 16 characters):", flush=True)
    print("  -netconport 2121\n", flush=True)
    print("-" * 65, flush=True)
    print("Both options fit directly into Steam's box alongside your existing flags.", flush=True)
    print("When TF2 opens, P-REC External connects automatically and announces", flush=True)
    print("its status directly into your TF2 in-game developer console (~).", flush=True)
    print("=" * 65, flush=True)

    if is_interactive():
        input("\nPress Enter to continue launching P-REC...")
    return cfg_target


def write_wizard_config(path: Path, league: str, rcon_pw: str, tf_path: str):
    if path.exists():
        print(f"[CONFIG] '{path.resolve()}' already exists. Preserving existing settings without overwriting.", flush=True)
        return
    content = f"""// ====================================================================
// {APP_FULL_TITLE} — Settings & Configuration
// ====================================================================
// Works seamlessly with mastercomfig, m0rehud, and DemoMan.
// ====================================================================

// --------------------------------------------------------------------
// Engine Compatibility Aliases (Suppresses console warnings in TF2)
// --------------------------------------------------------------------
alias prec_league                ""
alias prec_mode                  ""
alias prec_dir                   ""
alias prec_sound                 ""
alias prec_screens               ""
alias prec_notify                ""
alias prec_tag                   ""
alias prec_demo_name             ""
alias prec_min_streak            ""
alias prec_kill_delay            ""
alias prec_log                   ""
alias prec_server_rcon_passwords ""

// --------------------------------------------------------------------
// 1. League Ruleset Profile
// --------------------------------------------------------------------
// Available Profiles:
//   - "etf2l"        : European TF2 League (Strict Rule 2.1 compliance)
//   - "rgl"          : RGL.gg North American League (Rule 1008.5 compliance)
//   - "ozfortress"   : Oceanic TF2 League (Demo Checker compliance)
//   - "asiafortress" : AsiaFortress Cup & League (af_ configs)
//   - "matcha"       : Matcha.tf Asia/Pacific League
//   - "cltf2"        : CustomLander TF2 (4v4, Ultiduo, Highlander)
//   - "custom"       : Custom user triggers
prec_league                "{league}"

// --------------------------------------------------------------------
// 2. Recording Mode
// --------------------------------------------------------------------
// Modes:
//   3 = Record ALL matches (every map, round, and server automatically)
//   2 = Record tournament matches only (Auto-records when match goes LIVE - Default)
//   1 = Manual recording only (records on custom triggers/manual start)
//   0 = Disabled (turns off all demo recording)
prec_mode                  2

// --------------------------------------------------------------------
// 3. Demo Storage & Alerts
// --------------------------------------------------------------------
prec_dir                   "demos"
prec_sound                 1
prec_screens               1
prec_notify                1

// --------------------------------------------------------------------
// 4. Demo Naming Pattern
// --------------------------------------------------------------------
prec_tag                   ""
prec_demo_name             "%date%_%time%_%map%_%red%_%blu%"

// --------------------------------------------------------------------
// 5. Team Chat Messages (Configurable)
// --------------------------------------------------------------------
alias pr_message_start "say_team [P-REC] Recording started."
alias pr_message_stop  "say_team [P-REC] Stop recording."
alias pr_message_mark  "say_team [P-REC] Bookmark placed."

// --------------------------------------------------------------------
// 6. Killstreaks & Bookmarks (Optional)
// --------------------------------------------------------------------
prec_min_streak            3
prec_kill_delay            15
prec_log                   0

// --------------------------------------------------------------------
// 7. Server RCON / serveme.tf Synergy (Optional)
// --------------------------------------------------------------------
prec_server_rcon_passwords ""

sv_rcon_whitelist_address "127.0.0.1"
removeip 127.0.0.1
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    # In Source Engine, 'exec' commands strictly search the 'cfg/' directory.
    # If installed in tf/custom/P-REC, also place a copy in tf/custom/P-REC/cfg/ so TF2 can find it!
    if "custom" in [p.lower() for p in path.parts]:
        try:
            custom_cfg_dir = path.parent / "cfg"
            custom_cfg_dir.mkdir(parents=True, exist_ok=True)
            custom_cfg_file = custom_cfg_dir / path.name
            if not custom_cfg_file.exists():
                shutil.copy2(path, custom_cfg_file)
        except Exception:
            pass


# ====================================================================
# Uninstallation Logic (System Tray & CLI)
# ====================================================================

def prompt_uninstall_choices():
    """
    Prompts the user for uninstallation confirmation and whether to keep settings.
    Returns True to keep settings, False to wipe settings, or None if cancelled.
    """
    if sys.platform == "win32":
        try:
            import ctypes
            user32 = ctypes.windll.user32
            MB_YESNO = 0x00000004
            MB_YESNOCANCEL = 0x00000003
            MB_ICONQUESTION = 0x00000020
            MB_DEFBUTTON2 = 0x00000100
            IDYES = 6
            IDNO = 7
            IDCANCEL = 2

            # Step 1: Confirmation
            confirm = user32.MessageBoxW(
                0,
                f"Are you sure you want to uninstall {APP_NAME}?",
                f"Uninstall {APP_NAME}",
                MB_YESNO | MB_ICONQUESTION | MB_DEFBUTTON2
            )
            if confirm != IDYES:
                return None

            # Step 2: Keep Settings or Not
            prompt_text = (
                "Do you want to KEEP your configuration and league settings files?\n\n"
                "• Click YES to keep your settings (PREC_Settings.cfg, aliases, and custom league files).\n"
                "• Click NO to completely remove all settings, configs, and P-REC folders.\n"
                "• Click CANCEL to abort uninstallation."
            )
            settings_choice = user32.MessageBoxW(
                0,
                prompt_text,
                f"{APP_NAME} Uninstall — Settings",
                MB_YESNOCANCEL | MB_ICONQUESTION
            )
            if settings_choice == IDCANCEL:
                return None
            return (settings_choice == IDYES)
        except Exception:
            pass

    if is_interactive():
        print("\n" + "=" * 65, flush=True)
        print(f" [UNINSTALL {APP_NAME.upper()}]", flush=True)
        print("=" * 65, flush=True)
        ans = input(f"Are you sure you want to completely uninstall {APP_NAME}? [y/N]: ").strip().lower()
        if ans not in ("y", "yes"):
            print("[CANCELLED] Uninstallation aborted.", flush=True)
            return None
        keep_ans = input("Keep your configuration and settings files (PREC_Settings.cfg)? [Y/n]: ").strip().lower()
        return keep_ans not in ("n", "no")

    return None


def execute_uninstall(keep_settings: bool, tf_path="", config_path=""):
    """
    Executes the clean removal of P-REC External:
    - Removes Windows Startup registry key / Linux autostart entry
    - Removes Desktop shortcut
    - Cleans autoexec.cfg if requested
    - Removes settings / custom folder if keep_settings is False
    - Schedules self-deletion of executable and program directory
    - Displays confirmation dialog and exits
    """
    print(f"\n[{APP_NAME}] Beginning uninstallation (keep_settings={keep_settings})...", flush=True)

    # 1. Remove from Windows Startup (registry) or Linux autostart
    try:
        set_startup(False)
        print("[UNINSTALL] Removed from system startup.", flush=True)
    except Exception as e:
        print(f"[UNINSTALL] Note on startup removal: {e}", flush=True)

    # 2. Remove Desktop shortcut
    try:
        if sys.platform == "win32":
            desktop_dirs = [
                Path(os.environ.get("USERPROFILE", "")) / "Desktop",
                Path(os.environ.get("PUBLIC", "")) / "Desktop",
            ]
            for d in desktop_dirs:
                lnk = d / f"{APP_NAME}.lnk"
                if lnk.exists():
                    lnk.unlink()
                    print(f"[UNINSTALL] Removed desktop shortcut: {lnk}", flush=True)
        else:
            for p in (Path.home() / "Desktop/prec64.desktop", Path.home() / ".local/share/applications/prec64.desktop"):
                if p.exists():
                    p.unlink()
    except Exception as e:
        print(f"[UNINSTALL] Note on shortcut removal: {e}", flush=True)

    # 3. Clean autoexec.cfg and settings files
    effective_tf = Path(tf_path) if tf_path else detect_tf2_directory()
    if effective_tf and effective_tf.exists():
        if not keep_settings:
            clean_autoexec_prec(effective_tf)
            custom_prec = effective_tf / "custom/P-REC"
            if custom_prec.exists():
                try:
                    shutil.rmtree(custom_prec, ignore_errors=True)
                    print(f"[UNINSTALL] Removed custom directory: {custom_prec}", flush=True)
                except Exception as e:
                    print(f"[UNINSTALL] Error removing {custom_prec}: {e}", flush=True)
            cfg_in_cfg = effective_tf / "cfg/PREC_Settings.cfg"
            if cfg_in_cfg.exists():
                try:
                    cfg_in_cfg.unlink()
                except Exception:
                    pass
        else:
            print("[UNINSTALL] Preserving configuration files in tf/custom/P-REC/ and tf/cfg/.", flush=True)

    # 4. Schedule self-deletion of program directory & executable
    current_exe = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve()
    
    if sys.platform == "win32":
        local_appdata = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local"))
        prog_dir = Path(local_appdata) / "Programs/P-REC"
    else:
        prog_dir = Path.home() / ".local/share/P-REC"

    # 5. Show completion dialog to user
    if sys.platform == "win32":
        try:
            import ctypes
            settings_note = (
                "Your configuration and settings files were preserved."
                if keep_settings else
                "All settings, configs, and P-REC folders have been completely removed."
            )
            ctypes.windll.user32.MessageBoxW(
                0,
                f"P-REC External has been successfully uninstalled from your computer.\n\n{settings_note}",
                f"{APP_NAME} — Uninstall Complete",
                0x00000000 | 0x00000040  # MB_OK | MB_ICONINFORMATION
            )
        except Exception:
            pass
    print("[UNINSTALL] P-REC External has been successfully uninstalled.", flush=True)

    # 6. Execute self-deletion after process terminates
    is_git_repo = (current_exe.parent / ".git").exists() or (current_exe.parent.parent / ".git").exists()
    if sys.platform == "win32":
        try:
            pid = os.getpid()
            delete_exe = f'del /f /q \\"{current_exe}\\" &' if not is_git_repo else ""
            delete_dir = f'rmdir /s /q \\"{prog_dir}\\"' if prog_dir.exists() and prog_dir != current_exe.parent and not is_git_repo else (f'rmdir /s /q \\"{prog_dir}\\"' if prog_dir.exists() and not is_git_repo else "")
            
            cmd = f'cmd.exe /c "timeout /t 1 /nobreak >nul & :loop & tasklist /FI \\"PID eq {pid}\\" 2>nul | find \\"{pid}\\" >nul && (timeout /t 1 /nobreak >nul & goto loop) & {delete_exe} {delete_dir}"'
            DETACHED_PROCESS = 0x00000008
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(cmd, shell=True, creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW)
        except Exception:
            pass
    else:
        try:
            if not is_git_repo and current_exe.exists():
                current_exe.unlink(missing_ok=True)
            if prog_dir.exists() and not is_git_repo:
                shutil.rmtree(prog_dir, ignore_errors=True)
        except Exception:
            pass

    os._exit(0)


def run_uninstaller():
    existing_cfg = find_existing_config()
    tf_dir = detect_tf2_directory()
    keep_settings = prompt_uninstall_choices()
    if keep_settings is None:
        return
    execute_uninstall(
        keep_settings=keep_settings,
        tf_path=str(tf_dir) if tf_dir else "",
        config_path=str(existing_cfg) if existing_cfg else ""
    )


# ====================================================================
# Source RCON Implementation (Zero-Dependency)
# ====================================================================

class SourceRcon:
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_AUTH = 3
    SERVERDATA_RESPONSE_VALUE = 0
    SERVERDATA_AUTH_RESPONSE = 2

    def __init__(self, host="127.0.0.1", port=27969, password="", candidate_passwords=None):
        self.host = host
        self.port = port
        self.password = password
        self.candidate_passwords = list(candidate_passwords or [])
        if password and password not in self.candidate_passwords:
            self.candidate_passwords.insert(0, password)
        self.sock = None
        self.req_id = 1
        self.lock = threading.Lock()

    def connect(self, timeout=2.0, verbose=False):
        self.close()
        passwords_to_try = [self.password] if self.password else []
        for p in self.candidate_passwords:
            if p and p not in passwords_to_try:
                passwords_to_try.append(p)

        if verbose:
            print(f"[RCON DEBUG] Connecting to TCP {self.host}:{self.port}...", flush=True)

        last_err = None
        for pw in passwords_to_try:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout)
                s.connect((self.host, self.port))

                # Send SERVERDATA_AUTH
                req_id = 1
                payload = pw.encode("utf-8", errors="replace") + b"\x00\x00"
                packet = struct.pack("<iii", 4 + 4 + len(payload), req_id, self.SERVERDATA_AUTH) + payload
                s.sendall(packet)

                # Read auth response
                start_t = time.time()
                auth_ok = False
                while time.time() - start_t < timeout:
                    size_hdr = self._recv_exact_s(s, 4)
                    size = struct.unpack("<i", size_hdr)[0]
                    if size < 10 or size > 65536:
                        break
                    data = self._recv_exact_s(s, size)
                    r_id, r_type = struct.unpack("<ii", data[:8])
                    if r_type == self.SERVERDATA_AUTH_RESPONSE:
                        if r_id != -1 and r_id == req_id:
                            auth_ok = True
                            break
                        else:
                            break
                    elif r_type == self.SERVERDATA_RESPONSE_VALUE:
                        continue
                    else:
                        break

                if auth_ok:
                    self.sock = s
                    if pw != self.password:
                        print(f"[RCON AUTO-HEAL] Reconnected & synchronized active password: '{pw}'", flush=True)
                    self.password = pw
                    return True
                else:
                    s.close()
            except Exception as e:
                last_err = e

        if last_err:
            raise last_err
        raise PermissionError("RCON password rejected by TF2")

    def _recv_exact_s(self, s, n):
        buf = bytearray()
        while len(buf) < n:
            chunk = s.recv(n - len(buf))
            if not chunk:
                raise ConnectionResetError("RCON connection closed by remote host")
            buf.extend(chunk)
        return bytes(buf)

    def _send_raw(self, packet_type, body):
        self.req_id = (self.req_id + 1) % 0x7FFFFFFF or 1
        payload = body.encode("utf-8", errors="replace") + b"\x00\x00"
        packet_size = 4 + 4 + len(payload)
        packet = struct.pack("<iii", packet_size, self.req_id, packet_type) + payload
        self.sock.sendall(packet)
        return self.req_id

    def _recv_exact(self, n):
        return self._recv_exact_s(self.sock, n)

    def _read_raw(self):
        size_header = self._recv_exact(4)
        size = struct.unpack("<i", size_header)[0]
        if size < 10 or size > 65536:
            raise ValueError(f"Invalid RCON packet size: {size}")
        data = self._recv_exact(size)
        req_id, packet_type = struct.unpack("<ii", data[:8])
        body = data[8:-2].decode("utf-8", errors="replace")
        return req_id, packet_type, body

    def send_command(self, cmd, retry=True):
        with self.lock:
            try:
                if not self.sock:
                    self.connect()
                self._send_raw(self.SERVERDATA_EXECCOMMAND, cmd)
                req_id, packet_type, body = self._read_raw()
                return body
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError) as e:
                self.close()
                if retry:
                    try:
                        for p in detect_process_rcon_passwords():
                            if p and p not in self.candidate_passwords:
                                self.candidate_passwords.insert(0, p)
                        self.connect()
                        self._send_raw(self.SERVERDATA_EXECCOMMAND, cmd)
                        req_id, packet_type, body = self._read_raw()
                        return body
                    except Exception:
                        pass
                raise e

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


# ====================================================================
# Netcon Client (Telnet Stream)
# ====================================================================

class NetconClient:
    def __init__(self, host="127.0.0.1", port=2121):
        self.host = host
        self.port = port
        self.sock = None
        self.lock = threading.Lock()

    def connect(self, timeout=3.0):
        self.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((self.host, self.port))
        s.settimeout(None)
        self.sock = s
        return True

    def send_command(self, cmd):
        with self.lock:
            if not self.sock:
                raise ConnectionResetError("Netcon disconnected")
            payload = (cmd.strip() + "\n").encode("utf-8", errors="replace")
            self.sock.sendall(payload)

    def line_stream(self):
        buffer = ""
        while self.sock:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    yield line.strip("\r")
            except Exception:
                break
        self.close()

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


# ====================================================================
# Console Log Tailer (For RCON Mode)
# ====================================================================

class ConsoleLogTailer:
    def __init__(self, log_path):
        self.log_path = Path(log_path)
        self.running = False

    def tail(self):
        self.running = True
        while self.running and not self.log_path.exists():
            time.sleep(1.0)

        if not self.running:
            return

        with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
            f.seek(0, os.SEEK_END)
            last_proc_check = time.time()
            while self.running:
                line = f.readline()
                if line:
                    yield line.strip("\r\n")
                else:
                    time.sleep(0.05)
                    now = time.time()
                    if now - last_proc_check > 3.0:
                        last_proc_check = now
                        running, _, _ = is_tf2_running()
                        if not running:
                            print(f"\n[{APP_NAME}] Team Fortress 2 process exited.", flush=True)
                            break

    def stop(self):
        self.running = False


# ====================================================================
# Desktop Bottom-Right Toast Notification
# ====================================================================

def get_icon_path(filename="supreme_soviet.png"):
    """Locates specified asset in assets folder or bundled PyInstaller folder."""
    dirs = [
        get_app_dir() / "assets",
        Path.cwd() / "assets",
        get_app_dir(),
        Path.cwd(),
    ]
    if getattr(sys, '_MEIPASS', None):
        dirs.insert(0, Path(sys._MEIPASS) / "assets")
        dirs.insert(0, Path(sys._MEIPASS))
    for d in dirs:
        cand = d / filename
        if cand.exists():
            return cand
    for d in dirs:
        for fallback in ["supreme_soviet.png", "supreme_soviet.ico"]:
            cand = d / fallback
            if cand.exists():
                return cand
    return None


# ====================================================================
# Native Console Window (Cross-out hides to Hidden Pictograms / Tray)
# ====================================================================

class ConsoleRedirector:
    def __init__(self, native_console, orig_stream):
        self.native_console = native_console
        self.orig_stream = orig_stream

    def write(self, s):
        if self.orig_stream:
            try:
                self.orig_stream.write(s)
                self.orig_stream.flush()
            except Exception:
                pass
        if self.native_console:
            self.native_console.write(s)

    def flush(self):
        if self.orig_stream:
            try:
                self.orig_stream.flush()
            except Exception:
                pass

    def isatty(self):
        return False

    def fileno(self):
        raise io.UnsupportedOperation("fileno not supported on ConsoleRedirector")

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return False


class NativeConsoleWindow:
    """
    Native Win32 console window for P-REC External on Windows.
    Intercepts WM_CLOSE so clicking 'X' (cross-out) smoothly moves the
    window to the background (Hidden Pictograms / Tray) instead of closing the application.
    Features:
      - Dark terminal theme (#121212 background, #E0E0E0 text)
      - Consolas monospace font
      - Real-time stream of all stdout and stderr prints
      - Safe buffer trimming (keeps last 500,000 characters)
    """
    def __init__(self, title=f"{APP_FULL_TITLE} - Console", on_hide_callback=None):
        self.title = title
        self.hwnd = None
        self.edit_hwnd = None
        self.visible = False
        self.thread = None
        self.ready_event = threading.Event()
        self.on_hide_callback = on_hide_callback
        self._buffer = []
        self._lock = threading.Lock()

    def start(self):
        if sys.platform != "win32":
            return
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.ready_event.wait(timeout=2.0)

    def show(self):
        if sys.platform != "win32" or not self.hwnd:
            return
        ctypes.windll.user32.ShowWindow(self.hwnd, 9)  # SW_RESTORE
        ctypes.windll.user32.SetForegroundWindow(self.hwnd)
        self.visible = True

    def hide(self):
        if sys.platform != "win32" or not self.hwnd:
            return
        ctypes.windll.user32.ShowWindow(self.hwnd, 0)  # SW_HIDE
        self.visible = False

    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def write(self, text):
        if not text or sys.platform != "win32":
            return
        clean_text = text.replace("\r\n", "\n").replace("\n", "\r\n")
        with self._lock:
            if not self.edit_hwnd:
                self._buffer.append(clean_text)
                return
            try:
                user32 = ctypes.windll.user32
                length = user32.GetWindowTextLengthW(self.edit_hwnd)
                if length > 500000:
                    user32.SendMessageW(self.edit_hwnd, 0x00B1, 0, ctypes.c_void_p(100000))
                    user32.SendMessageW(self.edit_hwnd, 0x00C2, 0, ctypes.cast(ctypes.create_unicode_buffer(""), ctypes.c_void_p))
                    length = user32.GetWindowTextLengthW(self.edit_hwnd)
                buf = ctypes.create_unicode_buffer(clean_text)
                user32.SendMessageW(self.edit_hwnd, 0x00B1, length, ctypes.c_void_p(length))
                user32.SendMessageW(self.edit_hwnd, 0x00C2, 0, ctypes.cast(buf, ctypes.c_void_p))
                user32.SendMessageW(self.edit_hwnd, 0x0115, 7, None)  # WM_VSCROLL SB_BOTTOM
            except Exception:
                pass

    def _run_loop(self):
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            gdi32 = ctypes.windll.gdi32

            LRESULT = ctypes.c_longlong
            user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
            user32.DefWindowProcW.restype = LRESULT
            user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, ctypes.c_void_p]
            user32.SendMessageW.restype = LRESULT
            user32.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT, ctypes.c_int, ctypes.c_int, wintypes.UINT]
            user32.LoadImageW.restype = wintypes.HANDLE
            user32.LoadIconW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
            user32.LoadIconW.restype = wintypes.HICON
            user32.CreateWindowExW.argtypes = [
                wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
                wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID
            ]
            user32.CreateWindowExW.restype = wintypes.HWND

            class_name = f"PREC_NativeConsole_{os.getpid()}"
            h_inst = kernel32.GetModuleHandleW(None)

            WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

            def wnd_proc(hwnd, msg, wp, lp):
                if msg == 0x0010:  # WM_CLOSE
                    # Cross out clicked ('X') -> Move to background / hidden pictograms, DO NOT CLOSE
                    user32.ShowWindow(hwnd, 0)  # SW_HIDE
                    self.visible = False
                    if self.on_hide_callback:
                        try:
                            self.on_hide_callback()
                        except Exception:
                            pass
                    return 0
                elif msg == 0x0005:  # WM_SIZE
                    w = lp & 0xFFFF
                    h = (lp >> 16) & 0xFFFF
                    if self.edit_hwnd:
                        user32.MoveWindow(self.edit_hwnd, 0, 0, w, h, True)
                    return 0
                elif msg == 0x0138:  # WM_CTLCOLORSTATIC (dark theme)
                    hdc = wintypes.HDC(wp)
                    gdi32.SetTextColor(hdc, 0x00E0E0E0)
                    gdi32.SetBkColor(hdc, 0x00121212)
                    return gdi32.GetStockObject(4)  # BLACK_BRUSH
                return user32.DefWindowProcW(hwnd, msg, wp, lp)

            self._wnd_proc = WNDPROC(wnd_proc)

            class WNDCLASSEXW(ctypes.Structure):
                _fields_ = [
                    ("cbSize", wintypes.UINT),
                    ("style", wintypes.UINT),
                    ("lpfnWndProc", WNDPROC),
                    ("cbClsExtra", ctypes.c_int),
                    ("cbWndExtra", ctypes.c_int),
                    ("hInstance", wintypes.HINSTANCE),
                    ("hIcon", wintypes.HICON),
                    ("hCursor", wintypes.HICON),
                    ("hbrBackground", wintypes.HBRUSH),
                    ("lpszMenuName", wintypes.LPCWSTR),
                    ("lpszClassName", wintypes.LPCWSTR),
                    ("hIconSm", wintypes.HICON),
                ]

            h_icon = None
            try:
                h_icon = user32.LoadIconW(h_inst, ctypes.cast(1, wintypes.LPCWSTR))
            except Exception:
                h_icon = None
            if not h_icon:
                ico_file = get_icon_path("supreme_soviet.ico")
                if ico_file and Path(ico_file).exists():
                    try:
                        h_icon = user32.LoadImageW(None, str(ico_file), 1, 0, 0, 0x00000010 | 0x00000040)
                    except Exception:
                        h_icon = None
            if not h_icon:
                try:
                    h_icon = user32.LoadIconW(None, ctypes.cast(32512, wintypes.LPCWSTR))
                except Exception:
                    h_icon = None

            wc = WNDCLASSEXW()
            wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
            wc.style = 0x0008  # CS_DBLCLKS
            wc.lpfnWndProc = self._wnd_proc
            wc.hInstance = h_inst
            wc.lpszClassName = class_name
            wc.hIcon = h_icon
            wc.hIconSm = h_icon
            wc.hbrBackground = gdi32.GetStockObject(4)
            user32.RegisterClassExW(ctypes.byref(wc))

            self.hwnd = user32.CreateWindowExW(
                0, class_name, self.title,
                0x00CF0000, 150, 150, 800, 520,
                None, None, h_inst, None
            )

            edit_style = 0x40000000 | 0x10000000 | 0x00200000 | 0x0004 | 0x0040 | 0x0800
            self.edit_hwnd = user32.CreateWindowExW(
                0, "EDIT", "",
                edit_style, 0, 0, 784, 481,
                self.hwnd, None, h_inst, None
            )

            h_font = gdi32.CreateFontW(16, 0, 0, 0, 400, False, False, False, 1, 0, 0, 2, 0, "Consolas")
            user32.SendMessageW(self.edit_hwnd, 0x0030, h_font, None)

            if h_icon:
                try:
                    user32.SendMessageW(self.hwnd, 0x0080, 1, ctypes.c_void_p(h_icon))
                    user32.SendMessageW(self.hwnd, 0x0080, 0, ctypes.c_void_p(h_icon))
                except Exception:
                    pass

            with self._lock:
                for buffered in self._buffer:
                    self.write(buffered)
                self._buffer.clear()

            self.ready_event.set()

            msg = wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        except Exception:
            pass


# Windows System Tray (Hidden Pictograms / Notification Area)
# ====================================================================

class WindowsSystemTray:
    """
    Manages a native Windows system tray icon in the 'hidden pictograms' (notification area)
    using Win32 Shell_NotifyIconW and ctypes. Zero external dependencies required.
    Includes right-click context menu:
      - Status header (grayed out)
      - Show / Hide Console Window
      - Go to Settings (PREC_Settings.cfg)
      - Open tf/custom/ Folder
      - Close P-REC External
    Double-clicking the icon opens PREC_Settings.cfg directly.
    """
    def __init__(self, config_path, tf_path="", on_exit_callback=None):
        self.config_path = str(config_path) if config_path else ""
        self.tf_path = str(tf_path) if tf_path else ""
        self.on_exit_callback = on_exit_callback
        self.on_check_conn_callback = None
        self.on_uninstall_callback = None
        self.status = "Waiting for TF2..."
        self.hwnd = None
        self.nid = None
        self.running = True
        self.thread = None
        self.console_visible = True
        self.native_console = None

    def _on_console_hidden(self):
        self.console_visible = False

    def start(self):
        if sys.platform != "win32":
            return
        try:
            self.native_console = NativeConsoleWindow(
                title=f"{APP_FULL_TITLE} - Console (Close hides to tray)",
                on_hide_callback=self._on_console_hidden
            )
            self.native_console.start()
            sys.stdout = ConsoleRedirector(self.native_console, sys.__stdout__)
            sys.stderr = ConsoleRedirector(self.native_console, sys.__stderr__)
        except Exception:
            pass
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def update_status(self, new_status: str):
        self.status = new_status
        if sys.platform != "win32" or not self.hwnd or not self.nid:
            return
        try:
            import ctypes
            shell32 = ctypes.windll.shell32
            tip = f"{APP_NAME} v{APP_VERSION} - {new_status}"
            self.nid.szTip = tip[:127]
            self.nid.uFlags = 0x00000004  # NIF_TIP
            shell32.Shell_NotifyIconW(0x00000001, ctypes.byref(self.nid))  # NIM_MODIFY
        except Exception:
            pass

    def open_settings(self):
        try:
            target = None
            if self.config_path and Path(self.config_path).exists():
                target = Path(self.config_path)
            else:
                target = find_existing_config()
            if target and target.exists():
                os.startfile(str(target.resolve()))
            else:
                print(f"[TRAY] Settings config not found: {self.config_path}", flush=True)
        except Exception as e:
            print(f"[TRAY] Error opening settings: {e}", flush=True)

    def open_custom_folder(self):
        try:
            target = None
            if self.tf_path and Path(self.tf_path).exists():
                target = Path(self.tf_path) / "custom"
            if not target or not target.exists():
                det = detect_tf2_directory()
                if det and (det / "custom").exists():
                    target = det / "custom"
            if target and target.exists():
                os.startfile(str(target.resolve()))
        except Exception as e:
            print(f"[TRAY] Error opening custom folder: {e}", flush=True)

    def hide_console(self):
        if sys.platform != "win32":
            return
        if getattr(self, "native_console", None):
            self.native_console.hide()
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
        except Exception:
            pass
        self.console_visible = False

    def show_console(self):
        if sys.platform != "win32":
            return
        if getattr(self, "native_console", None):
            self.native_console.show()
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                ctypes.windll.user32.SetForegroundWindow(hwnd)
        except Exception:
            pass
        self.console_visible = True

    def toggle_console(self):
        if self.console_visible:
            self.hide_console()
        else:
            self.show_console()

    def close(self):
        self.running = False
        if getattr(self, "native_console", None) and self.native_console.hwnd:
            try:
                import ctypes
                ctypes.windll.user32.DestroyWindow(self.native_console.hwnd)
            except Exception:
                pass
        if sys.platform == "win32" and self.hwnd:
            try:
                import ctypes
                ctypes.windll.user32.PostMessageW(self.hwnd, 0x0010, 0, 0)  # WM_CLOSE
            except Exception:
                pass

    def _run_loop(self):
        try:
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            shell32 = ctypes.windll.shell32
            kernel32 = ctypes.windll.kernel32

            LRESULT = ctypes.c_longlong
            user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
            user32.DefWindowProcW.restype = LRESULT
            user32.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT, ctypes.c_int, ctypes.c_int, wintypes.UINT]
            user32.LoadImageW.restype = wintypes.HANDLE
            user32.LoadIconW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
            user32.LoadIconW.restype = wintypes.HICON
            user32.CreateWindowExW.argtypes = [
                wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
                wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID
            ]
            user32.CreateWindowExW.restype = wintypes.HWND

            WM_USER = 0x0400
            WM_TRAY = WM_USER + 20
            WM_LBUTTONUP = 0x0202
            WM_LBUTTONDBLCLK = 0x0203
            WM_RBUTTONUP = 0x0205
            WM_COMMAND = 0x0111
            WM_DESTROY = 0x0002
            WM_CLOSE = 0x0010
            WM_NULL = 0x0000

            NIM_ADD = 0x00000000
            NIM_MODIFY = 0x00000001
            NIM_DELETE = 0x00000002

            NIF_MESSAGE = 0x00000001
            NIF_ICON = 0x00000002
            NIF_TIP = 0x00000004

            IMAGE_ICON = 1
            LR_LOADFROMFILE = 0x00000010
            LR_DEFAULTSIZE = 0x00000040

            MF_STRING = 0x00000000
            MF_SEPARATOR = 0x00000800
            MF_GRAYED = 0x00000001
            MF_CHECKED = 0x00000008
            MF_UNCHECKED = 0x00000000
            TPM_RIGHTBUTTON = 0x0002
            TPM_BOTTOMALIGN = 0x0020

            ID_STATUS = 1001
            ID_TOGGLE_CONSOLE = 1002
            ID_CHECK_CONN = 1003
            ID_STARTUP = 1004
            ID_SETTINGS = 1005
            ID_CUSTOM_DIR = 1006
            ID_UPDATE = 1007
            ID_SHORTCUT = 1008
            ID_UNINSTALL = 1009
            ID_EXIT = 1010

            class NOTIFYICONDATAW(ctypes.Structure):
                _fields_ = [
                    ("cbSize", wintypes.DWORD),
                    ("hWnd", wintypes.HWND),
                    ("uID", wintypes.UINT),
                    ("uFlags", wintypes.UINT),
                    ("uCallbackMessage", wintypes.UINT),
                    ("hIcon", wintypes.HICON),
                    ("szTip", wintypes.WCHAR * 128),
                    ("dwState", wintypes.DWORD),
                    ("dwStateMask", wintypes.DWORD),
                    ("szInfo", wintypes.WCHAR * 256),
                    ("uTimeoutOrVersion", wintypes.UINT),
                    ("szInfoTitle", wintypes.WCHAR * 64),
                    ("dwInfoFlags", wintypes.DWORD),
                ]

            WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

            class WNDCLASSEXW(ctypes.Structure):
                _fields_ = [
                    ("cbSize", wintypes.UINT),
                    ("style", wintypes.UINT),
                    ("lpfnWndProc", WNDPROC),
                    ("cbClsExtra", ctypes.c_int),
                    ("cbWndExtra", ctypes.c_int),
                    ("hInstance", wintypes.HINSTANCE),
                    ("hIcon", wintypes.HICON),
                    ("hCursor", wintypes.HICON),
                    ("hbrBackground", wintypes.HBRUSH),
                    ("lpszMenuName", wintypes.LPCWSTR),
                    ("lpszClassName", wintypes.LPCWSTR),
                    ("hIconSm", wintypes.HICON),
                ]

            class POINT(ctypes.Structure):
                _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

            h_inst = kernel32.GetModuleHandleW(None)
            class_name = f"PREC_Tray_Class_{os.getpid()}"

            def show_menu():
                h_menu = user32.CreatePopupMenu()
                status_header = f"{APP_NAME} ({self.status})"
                user32.AppendMenuW(h_menu, MF_STRING, ID_STATUS, status_header)
                user32.EnableMenuItem(h_menu, ID_STATUS, MF_GRAYED)
                user32.AppendMenuW(h_menu, MF_SEPARATOR, 0, None)

                if getattr(self, "available_update", None):
                    up_text = f"⚡ Update to {self.available_update.get('version', 'New Release')}"
                    user32.AppendMenuW(h_menu, MF_STRING, ID_UPDATE, up_text)
                    user32.AppendMenuW(h_menu, MF_SEPARATOR, 0, None)

                console_label = "Hide Console Window" if self.console_visible else "Show Console Window"
                user32.AppendMenuW(h_menu, MF_STRING, ID_TOGGLE_CONSOLE, console_label)

                user32.AppendMenuW(h_menu, MF_STRING, ID_CHECK_CONN, "Check RCON / Connection")

                startup_flag = MF_CHECKED if is_startup_enabled() else MF_UNCHECKED
                user32.AppendMenuW(h_menu, MF_STRING | startup_flag, ID_STARTUP, "Start with Windows")

                user32.AppendMenuW(h_menu, MF_STRING, ID_SETTINGS, "Go to Settings (PREC_Settings.cfg)")
                user32.AppendMenuW(h_menu, MF_STRING, ID_CUSTOM_DIR, "Open tf/custom/ Folder")
                user32.AppendMenuW(h_menu, MF_STRING, ID_SHORTCUT, "Create Desktop Shortcut")
                user32.AppendMenuW(h_menu, MF_SEPARATOR, 0, None)
                user32.AppendMenuW(h_menu, MF_STRING, ID_UNINSTALL, "Uninstall P-REC External...")
                user32.AppendMenuW(h_menu, MF_STRING, ID_EXIT, f"Close {APP_NAME}")

                pt = POINT()
                user32.GetCursorPos(ctypes.byref(pt))
                user32.SetForegroundWindow(self.hwnd)
                user32.TrackPopupMenu(h_menu, TPM_RIGHTBUTTON | TPM_BOTTOMALIGN, pt.x, pt.y, 0, self.hwnd, None)
                user32.PostMessageW(self.hwnd, WM_NULL, 0, 0)
                user32.DestroyMenu(h_menu)

            def wnd_proc(hwnd, msg, wparam, lparam):
                if msg == WM_TRAY:
                    if lparam == WM_RBUTTONUP:
                        show_menu()
                    elif lparam in (WM_LBUTTONUP, WM_LBUTTONDBLCLK):
                        self.toggle_console()
                    return 0
                elif msg == WM_COMMAND:
                    cmd_id = int(wparam) & 0xFFFF
                    if cmd_id == ID_UPDATE:
                        if getattr(self, "available_update", None) and self.available_update.get("url"):
                            try:
                                os.startfile(self.available_update["url"])
                            except Exception:
                                pass
                    elif cmd_id == ID_TOGGLE_CONSOLE:
                        self.toggle_console()
                    elif cmd_id == ID_CHECK_CONN:
                        if getattr(self, "on_check_conn_callback", None):
                            threading.Thread(target=self.on_check_conn_callback, daemon=True).start()
                    elif cmd_id == ID_STARTUP:
                        set_startup(not is_startup_enabled())
                    elif cmd_id == ID_SETTINGS:
                        self.open_settings()
                    elif cmd_id == ID_CUSTOM_DIR:
                        self.open_custom_folder()
                    elif cmd_id == ID_SHORTCUT:
                        create_desktop_shortcut()
                    elif cmd_id == ID_UNINSTALL:
                        if getattr(self, "on_uninstall_callback", None):
                            threading.Thread(target=self.on_uninstall_callback, daemon=True).start()
                        else:
                            threading.Thread(target=run_uninstaller, daemon=True).start()
                    elif cmd_id == ID_EXIT:
                        self.running = False
                        user32.DestroyWindow(hwnd)
                        if self.on_exit_callback:
                            self.on_exit_callback()
                        else:
                            os._exit(0)
                    return 0
                elif msg == WM_CLOSE:
                    user32.DestroyWindow(hwnd)
                    return 0
                elif msg == WM_DESTROY:
                    if self.nid:
                        shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))
                    user32.PostQuitMessage(0)
                    return 0
                return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

            self._wnd_proc = WNDPROC(wnd_proc)

            h_icon = None
            try:
                h_icon = user32.LoadIconW(h_inst, ctypes.cast(1, wintypes.LPCWSTR))
            except Exception:
                h_icon = None
            if not h_icon:
                ico_file = get_icon_path("supreme_soviet.ico")
                if ico_file and Path(ico_file).exists():
                    try:
                        h_icon = user32.LoadImageW(None, str(ico_file), IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE)
                    except Exception:
                        h_icon = None
            if not h_icon:
                try:
                    h_icon = user32.LoadIconW(None, ctypes.cast(32512, wintypes.LPCWSTR))
                except Exception:
                    h_icon = None

            wc = WNDCLASSEXW()
            wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
            wc.style = 0x0008  # CS_DBLCLKS
            wc.lpfnWndProc = self._wnd_proc
            wc.hInstance = h_inst
            wc.lpszClassName = class_name
            wc.hIcon = h_icon
            wc.hIconSm = h_icon
            user32.RegisterClassExW(ctypes.byref(wc))

            self.hwnd = user32.CreateWindowExW(
                0, class_name, "P-REC Tray",
                0, 0, 0, 0, 0,
                None, None, h_inst, None
            )

            self.nid = NOTIFYICONDATAW()
            self.nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
            self.nid.hWnd = self.hwnd
            self.nid.uID = 1
            self.nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
            self.nid.uCallbackMessage = WM_TRAY
            self.nid.hIcon = h_icon
            tip = f"{APP_NAME} v{APP_VERSION} - {self.status}"
            self.nid.szTip = tip[:127]

            shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(self.nid))

            msg = wintypes.MSG()
            while self.running and user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        except Exception as e:
            print(f"[TRAY] System tray error: {e}", flush=True)
        finally:
            if self.nid and sys.platform == "win32":
                try:
                    import ctypes
                    ctypes.windll.shell32.Shell_NotifyIconW(0x00000002, ctypes.byref(self.nid))
                except Exception:
                    pass


# ====================================================================
# Engine Core & League Rule Enforcer
# ====================================================================

class PrecEngine:
    def __init__(self, config: PrecConfig):
        self.cfg = config
        self.is_recording = False
        self.is_tournament = False
        self.is_scrim = False
        self.last_record_start = 0.0
        self.last_record_stop = 0.0
        self.last_connected_server = ""
        self.last_connected_map = ""
        self.was_in_match = False
        self.client_mode = None
        self.sender = None
        self.tailer = None
        self.current_server_ip = ""
        self.current_map = ""
        self.current_red_team = "red"
        self.current_blu_team = "blu"
        self.current_demo_name = ""
        self.match_start_time = 0.0
        self.status_screenshot_taken = False
        self.status_screenshot_timer = None
        self.profiles = load_league_profiles(self.cfg.prec_tf_path)
        league_id = self.cfg.prec_league.lower()
        self.active_profile = self.profiles.get(league_id, self.profiles.get("custom", {}))

        # Windows System Tray
        self.tray = WindowsSystemTray(
            config_path=self.cfg.cfg_path,
            tf_path=self.cfg.prec_tf_path,
            on_exit_callback=self.stop_all
        )
        self.tray.on_check_conn_callback = self.check_connection
        self.tray.on_uninstall_callback = self.uninstall
        self.tray.start()

        # Show console window on startup unless explicitly launched silently via --tray or --minimized
        if sys.platform == "win32":
            if any(arg in sys.argv for arg in ("--tray", "--minimized", "--silent", "--daemon")):
                self.tray.hide_console()
            else:
                self.tray.show_console()

        # Ensure Desktop Shortcut exists if enabled (default=1)
        if getattr(self.cfg, "prec_desktop_shortcut", 1):
            ensure_desktop_shortcut()

        # Background update check
        def _bg_update_check():
            try:
                info = check_for_updates(interactive=False)
                if info and self.tray:
                    self.tray.available_update = info
                    self.tray.update_status(f"Update: {info.get('version')}")
            except Exception:
                pass
        threading.Thread(target=_bg_update_check, daemon=True).start()

    def check_connection(self):
        """
        Manually tests connection to TF2, prints diagnostics,
        sends confirmation to TF2 in-game console, and updates tray status.
        """
        prof_name = self.active_profile.get("name", self.cfg.prec_league.upper())
        print("\n" + "=" * 60, flush=True)
        print(f"[{APP_NAME}] --- RCON & Netcon Connection Diagnostics ---", flush=True)
        print("=" * 60, flush=True)

        if self.sender:
            mode_upper = self.client_mode.upper()
            port = self.cfg.prec_netcon_port if self.client_mode == "netcon" else self.cfg.prec_rcon_port
            print(f"[STATUS] Connected to Team Fortress 2 via {mode_upper} (Port {port})!", flush=True)
            print(f"         Active Profile: {prof_name}", flush=True)
            print(f"         Recording Mode: {self.cfg.prec_mode}", flush=True)
            print(f"         Tournament Live: {'YES' if self.is_tournament else 'NO (Waiting for match countdown)'}", flush=True)
            print(f"         Currently Recording: {'YES' if self.is_recording else 'NO'}", flush=True)

            # In-game console feedback
            self.send_cmd('echo ""')
            self.send_cmd('echo "[P-REC External] ================================================"')
            self.send_cmd('echo "[P-REC External] CONNECTION CHECK: SUCCESS!"')
            self.send_cmd(f'echo "[P-REC External] Communication active via {mode_upper} (Port {port})"')
            self.send_cmd(f'echo "[P-REC External] Active League: {prof_name} | Mode: {self.cfg.prec_mode}"')
            self.send_cmd('echo "[P-REC External] All systems operational. Match monitoring engaged."')
            self.send_cmd('echo "[P-REC External] ================================================"')
            self.send_cmd('echo ""')
            self.query_tournament_teams()
            sample_name = self.format_demo_name()
            self.send_cmd(f'say_team [P-REC] Connection check: SUCCESS! Active League: {prof_name} | Demo Template: {sample_name}.dem')

            if hasattr(self, "tray") and self.tray:
                self.tray.update_status(f"Connected ({mode_upper} • {prof_name}) - OK")
            self.play_sound(is_start=True)
            print("[RESULT] In-game confirmation sent to TF2 developer console (~).", flush=True)
            print("[RESULT] Connection is fully operational!\n", flush=True)
        else:
            tf_running, tf_pname, tf_pid = is_tf2_running()
            print("[STATUS] Not currently connected to Team Fortress 2.", flush=True)
            if tf_running:
                print(f"[STATUS] Team Fortress 2 IS RUNNING! (Process: {tf_pname}, PID: {tf_pid})", flush=True)
            else:
                print("[STATUS] Team Fortress 2 process is not currently running.", flush=True)
            print("P-REC External is probing ports on localhost...", flush=True)

            # Probe Netcon
            netcon_ok = False
            try:
                nc = NetconClient(port=self.cfg.prec_netcon_port)
                nc.connect(timeout=0.8)
                nc.close()
                netcon_ok = True
                print(f"  [+] Netcon (Port {self.cfg.prec_netcon_port}): PORT OPEN! TF2 is listening.", flush=True)
            except Exception:
                print(f"  [-] Netcon (Port {self.cfg.prec_netcon_port}): Port closed / not listening.", flush=True)

            # Probe RCON
            rcon_ok = False
            rcon_error = None
            try:
                rc = SourceRcon(port=self.cfg.prec_rcon_port, password=self.cfg.prec_rcon_password, candidate_passwords=self.cfg.candidate_passwords)
                rc.connect(timeout=1.2, verbose=True)
                if rc.password != self.cfg.prec_rcon_password:
                    self.cfg.prec_rcon_password = rc.password
                rc.close()
                rcon_ok = True
                print(f"  [+] RCON (Port {self.cfg.prec_rcon_port}): PORT OPEN! Password authenticated successfully.", flush=True)
            except Exception as e:
                rcon_error = e
                print(f"  [-] RCON (Port {self.cfg.prec_rcon_port}): Failed ({e}).", flush=True)

            if not netcon_ok and not rcon_ok:
                if not tf_running:
                    print("\n[DIAGNOSIS] Team Fortress 2 is not currently running.", flush=True)
                    print("Start TF2 from Steam with these Launch Options:\n", flush=True)
                    print(f"  -usercon +rcon_password {self.cfg.prec_rcon_password} +ip 0.0.0.0 +hostport {self.cfg.prec_rcon_port} +net_start\n", flush=True)
                else:
                    err_str = str(rcon_error)
                    if "10054" in err_str or "Connection reset" in err_str or "10053" in err_str or "closed by remote" in err_str:
                        print(f"\n[DIAGNOSIS] TF2 is running on PID {tf_pid}, but reset the connection on port {self.cfg.prec_rcon_port}.", flush=True)
                        print("  Cause: TF2's internal flood protection temporarily banned 127.0.0.1 due to earlier connection attempts,", flush=True)
                        print("         or the game needs the whitelist address cvar active.", flush=True)
                        print("  FIX: Open TF2 in-game console (~) and enter:", flush=True)
                        print("       removeip 127.0.0.1; sv_rcon_whitelist_address 127.0.0.1", flush=True)
                        print("       Or simply restart Team Fortress 2.\n", flush=True)
                    elif "PermissionError" in str(type(rcon_error)) or "rejected" in err_str:
                        print(f"\n[DIAGNOSIS] TF2 is listening on port {self.cfg.prec_rcon_port}, but the password was rejected.", flush=True)
                        print(f"  Check that 'rcon_password' in TF2 matches your settings password ({self.cfg.prec_rcon_password}).\n", flush=True)
                    else:
                        print(f"\n[DIAGNOSIS] TF2 is running on PID {tf_pid}, but port {self.cfg.prec_rcon_port} is not listening.", flush=True)
                        print("  Make sure TF2 was launched with:", flush=True)
                        print(f"  -usercon +rcon_password {self.cfg.prec_rcon_password} +ip 0.0.0.0 +hostport {self.cfg.prec_rcon_port} +net_start\n", flush=True)
                if hasattr(self, "tray") and self.tray:
                    self.tray.update_status("Waiting for TF2...")
                self.play_sound(is_start=False)
            else:
                print("\n[DIAGNOSIS] Port is open! The main listener loop will hook in within 2 seconds.", flush=True)

        print("=" * 60 + "\n", flush=True)

    def stop_all(self):
        print(f"\n[{APP_NAME}] Exit requested from System Tray. Shutting down...", flush=True)
        if getattr(self, "status_screenshot_timer", None):
            try:
                self.status_screenshot_timer.cancel()
            except Exception:
                pass
            self.status_screenshot_timer = None
        if self.is_recording:
            try:
                self.stop_recording("User Exit")
            except Exception:
                pass
        if self.tray:
            self.tray.close()
        os._exit(0)

    def uninstall(self):
        keep_settings = prompt_uninstall_choices()
        if keep_settings is None:
            return

        print(f"\n[{APP_NAME}] Uninstallation confirmed. Stopping operations...", flush=True)
        if getattr(self, "status_screenshot_timer", None):
            try:
                self.status_screenshot_timer.cancel()
            except Exception:
                pass
            self.status_screenshot_timer = None

        if self.is_recording:
            try:
                self.stop_recording("Uninstalling P-REC")
            except Exception:
                pass

        try:
            if self.sender:
                self.sender.close()
                self.sender = None
            if self.tailer:
                self.tailer.stop()
        except Exception:
            pass

        if self.tray:
            try:
                self.tray.close()
            except Exception:
                pass

        execute_uninstall(
            keep_settings=keep_settings,
            tf_path=self.cfg.prec_tf_path,
            config_path=self.cfg.cfg_path
        )

    def query_tournament_teams(self):
        """Queries TF2 for active tournament red and blu team names."""
        if not self.sender:
            return
        try:
            body_red = self.send_cmd_response("mp_tournament_redteamname")
            m_red = re.search(r'=\s*"([^"]*)"', body_red)
            if m_red and m_red.group(1).strip():
                raw = m_red.group(1).strip()
                clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', raw.lower())
                clean = re.sub(r'_+', '_', clean).strip('_')
                if clean:
                    self.current_red_team = clean
        except Exception:
            pass

        try:
            body_blu = self.send_cmd_response("mp_tournament_blueteamname")
            m_blu = re.search(r'=\s*"([^"]*)"', body_blu)
            if m_blu and m_blu.group(1).strip():
                raw = m_blu.group(1).strip()
                clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', raw.lower())
                clean = re.sub(r'_+', '_', clean).strip('_')
                if clean:
                    self.current_blu_team = clean
        except Exception:
            pass

    def format_demo_name(self, now=None) -> str:
        """Formats the demo filename using % % indicators according to the classic P-REC convention.
        Default pattern: %date%_%time%_%map%_%red%_%blu%
        Produces e.g.: 20200906_2253_koth_coalplant_b8_red_blu
        """
        import datetime
        if not now:
            now = datetime.datetime.now()

        template = self.cfg.prec_demo_name if self.cfg.prec_demo_name else "%date%_%time%_%map%_%red%_%blu%"

        clean_map = re.sub(r'[^a-zA-Z0-9_\-]', '_', (self.current_map or "unknown_map").strip().lower())
        clean_map = re.sub(r'_+', '_', clean_map).strip('_') or "unknown_map"

        clean_red = re.sub(r'[^a-zA-Z0-9_\-]', '_', (self.current_red_team or "red").strip().lower())
        clean_red = re.sub(r'_+', '_', clean_red).strip('_') or "red"

        clean_blu = re.sub(r'[^a-zA-Z0-9_\-]', '_', (self.current_blu_team or "blu").strip().lower())
        clean_blu = re.sub(r'_+', '_', clean_blu).strip('_') or "blu"

        clean_tag = re.sub(r'[^a-zA-Z0-9_\-]', '_', (self.cfg.prec_tag or "").strip().lower())
        clean_tag = re.sub(r'_+', '_', clean_tag).strip('_')

        clean_league = re.sub(r'[^a-zA-Z0-9_\-]', '_', (self.cfg.prec_league or "match").strip().lower())
        clean_league = re.sub(r'_+', '_', clean_league).strip('_') or "match"

        tokens = {
            "%date%": now.strftime("%Y%m%d"),
            "%time%": now.strftime("%H%M"),
            "%map%": clean_map,
            "%red%": clean_red,
            "%blu%": clean_blu,
            "%league%": clean_league,
            "%tag%": clean_tag,
            "%year%": now.strftime("%Y"),
            "%month%": now.strftime("%m"),
            "%day%": now.strftime("%d"),
            "%hour%": now.strftime("%H"),
            "%min%": now.strftime("%M"),
            "%sec%": now.strftime("%S"),
        }

        result = template
        for token, val in tokens.items():
            result = re.sub(re.escape(token), val, result, flags=re.I)

        if self.is_scrim and "_scrim" not in result.lower():
            result = f"{result}_scrim"

        result = re.sub(r'_+', '_', result).strip('_')
        return result or f"{now.strftime('%Y%m%d_%H%M')}_{clean_map}"

    def get_demo_prefix(self) -> str:
        """Determines the demo prefix for TF2 Demo Support."""
        name = self.format_demo_name()
        return f"{name}_"

    def apply_league_cvars(self):
        prof_name = self.active_profile.get("name", self.cfg.prec_league.upper())
        mode_label = "SCRIM (Practice)" if self.is_scrim else "OFFICIAL MATCH"
        print(f"[{APP_NAME}] Applying cvars for: {prof_name} [{mode_label}]", flush=True)

        # Immunize localhost and clear any transient bans
        self.send_cmd('sv_rcon_whitelist_address "127.0.0.1"')
        self.send_cmd("removeip 127.0.0.1")
        self.send_cmd('con_logfile "console.log"')

        self.send_cmd(f'ds_dir "{self.cfg.prec_dir}"')
        self.send_cmd(f"ds_notify {self.cfg.prec_notify}")
        self.send_cmd(f"ds_sound {self.cfg.prec_sound}")

        # In scrim mode, skip mandatory status screenshots to avoid cluttering screenshot folder
        if self.is_scrim:
            self.send_cmd("ds_screens 0")
        else:
            screens_val = 1 if (self.cfg.prec_screens or self.active_profile.get("mandatory_status_screenshot")) else 0
            self.send_cmd(f"ds_screens {screens_val}")

        self.send_cmd(f"ds_autodelete {self.active_profile.get('ds_autodelete', 0)}")
        self.send_cmd(f"ds_min_streak {self.cfg.prec_min_streak}")
        self.send_cmd(f"ds_kill_delay {self.cfg.prec_kill_delay}")
        self.send_cmd(f"ds_log {self.cfg.prec_log}")

        # Prefix logic: default <mapname>_<date>_<time>
        prefix = self.get_demo_prefix()
        if prefix:
            self.send_cmd(f'ds_prefix "{prefix}"')

        ds_mode = self.active_profile.get("ds_enable", 0)
        self.send_cmd(f"ds_enable {ds_mode}")
        if self.active_profile.get("server_demo_checker_bypass"):
            print(f"        [{prof_name}] Set ds_enable {ds_mode} & ds_autodelete 0 for Server Demo Checker compliance.", flush=True)
        else:
            print(f"        [{prof_name}] Set ds_enable {ds_mode} (manual mode: auto-triggered on match live).", flush=True)

        self.send_cmd(f'echo "[P-REC External] League profile active: {prof_name} [{mode_label}]"')
        self.send_cmd(f'echo "[P-REC External] Target demo directory: tf/{self.cfg.prec_dir}/ | Prefix: {prefix}"')

    def play_sound(self, is_start=True):
        if not self.cfg.prec_sound:
            return
        try:
            if sys.platform == "win32":
                import winsound
                if is_start:
                    winsound.Beep(900, 120)
                    time.sleep(0.04)
                    winsound.Beep(1200, 180)
                else:
                    winsound.Beep(1200, 120)
                    time.sleep(0.04)
                    winsound.Beep(800, 180)
            else:
                try:
                    sound_name = "bell" if is_start else "dialog-warning"
                    subprocess.run(["paplay", f"/usr/share/sounds/freedesktop/stereo/{sound_name}.oga"],
                                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    sys.stdout.write("\a")
                    sys.stdout.flush()
        except Exception:
            pass

    def capture_status_screenshot(self, trigger_type="Mid-Game (3+ mins)"):
        """Captures in-game status & screenshot via Source engine RCON (status; jpeg)."""
        if not self.is_recording:
            return

        should_screen = (self.cfg.prec_screens and not self.is_scrim) or (
            self.active_profile.get("mandatory_status_screenshot") and not self.is_scrim
        )
        if not should_screen:
            return

        print(f"\n[{APP_NAME}] Capturing mandatory status screenshot ({trigger_type})...", flush=True)
        self.send_cmd("status; jpeg")
        self.send_cmd(f'echo "[P-REC External] Status screenshot captured ({trigger_type})"')
        self.status_screenshot_taken = True

    def schedule_status_screenshot(self):
        """Schedules random in-game status screenshot after 3 minutes of play (ETF2L Rule 2.1 compliance)."""
        if self.status_screenshot_timer:
            try:
                self.status_screenshot_timer.cancel()
            except Exception:
                pass
            self.status_screenshot_timer = None

        should_screen = (self.cfg.prec_screens and not self.is_scrim) or (
            self.active_profile.get("mandatory_status_screenshot") and not self.is_scrim
        )
        if not should_screen:
            return

        now = time.time()
        elapsed = (now - self.match_start_time) if self.match_start_time else 0.0
        if elapsed >= 180.0:
            # Match is already 3+ minutes in (substitute or mid-game reconnect)
            delay = random.uniform(10.0, 45.0)
        else:
            # Fresh match: wait until 3 minutes (180s) have passed, plus a random offset (15-75s)
            delay = (180.0 - elapsed) + random.uniform(15.0, 75.0)

        total_play_time = elapsed + delay
        mins = int(total_play_time // 60)
        secs = int(total_play_time % 60)
        print(f"[{APP_NAME}] In-game status screenshot scheduled in {int(delay)}s (after ~{mins}m {secs:02d}s of play)", flush=True)

        def _worker():
            if self.is_recording and not self.status_screenshot_taken:
                self.capture_status_screenshot(f"Mid-Game: ~{mins}m {secs:02d}s")

        self.status_screenshot_timer = threading.Timer(delay, _worker)
        self.status_screenshot_timer.daemon = True
        self.status_screenshot_timer.start()

    def start_recording(self, reason="Match Live"):
        now = time.time()
        if self.is_recording or (now - self.last_record_start < 1.5):
            return

        self.last_record_start = now
        self.is_recording = True
        self.was_in_match = True
        if not self.match_start_time:
            self.match_start_time = now
        self.status_screenshot_taken = False
        self.schedule_status_screenshot()

        if self.current_server_ip:
            self.last_connected_server = self.current_server_ip
        if self.current_map:
            self.last_connected_map = self.current_map

        sub_type = "Scrim Practice" if self.is_scrim else "Official Match"

        # Query tournament team names (e.g. Froyotech, Witness Gaming, red, blu)
        self.query_tournament_teams()

        demo_name = self.format_demo_name()
        self.current_demo_name = demo_name
        demo_dir = (self.cfg.prec_dir or "demos").strip("/\\")
        demo_rel_path = f"{demo_dir}/{demo_name}" if demo_dir else demo_name

        print(f"\n[{APP_NAME}] >>> START RECORDING <<< ({sub_type}: {reason})", flush=True)
        print(f"[{APP_NAME}] Demo filename: {demo_name}.dem (Target: tf/{demo_rel_path}.dem)", flush=True)

        # Set ds_prefix for demo support compliance
        self.send_cmd(f'ds_prefix "{demo_name}_"')

        # Record demo with exact name using Source Engine record command
        if self.active_profile.get("server_demo_checker_bypass"):
            self.send_cmd(f'stop; ds_stop; record "{demo_rel_path}"')
        else:
            self.send_cmd(f'record "{demo_rel_path}"')

        self.send_cmd(f'echo "[P-REC External] >>> RECORDING STARTED ({sub_type}: {reason}) <<<"')
        self.send_cmd(f'echo "[P-REC External] Target demo: tf/{demo_rel_path}.dem"')

        if self.cfg.prec_notify >= 1 and self.cfg.pr_message_start:
            msg = self.cfg.pr_message_start
            if self.is_scrim and "[P-REC]" in msg:
                msg = msg.replace("[P-REC]", "[P-REC Scrim]")
            self.send_cmd(msg)

        self.play_sound(is_start=True)
        if hasattr(self, "tray") and self.tray:
            self.tray.update_status(f"Recording ({self.current_demo_name})")

    def stop_recording(self, reason="Match Finished"):
        now = time.time()
        if not self.is_recording or (now - self.last_record_stop < 1.5):
            return

        self.last_record_stop = now
        self.is_recording = False
        print(f"\n[{APP_NAME}] >>> STOP RECORDING <<< ({reason})", flush=True)

        if self.status_screenshot_timer:
            try:
                self.status_screenshot_timer.cancel()
            except Exception:
                pass
            self.status_screenshot_timer = None

        # In scrim mode, skip mandatory status screenshots unless explicitly configured
        should_screen = (self.cfg.prec_screens and not self.is_scrim) or (self.active_profile.get("mandatory_status_screenshot") and not self.is_scrim)
        if should_screen:
            if not self.status_screenshot_taken:
                self.capture_status_screenshot("Match End Fallback")
                time.sleep(0.4)
            elif self.cfg.prec_screens >= 1:
                print(f"[{APP_NAME}] Capturing match end scoreboard screenshot...", flush=True)
                self.send_cmd("status; jpeg")
                time.sleep(0.4)

        self.match_start_time = 0.0

        self.send_cmd("stop; ds_stop")
        demo_dir = (self.cfg.prec_dir or "demos").strip("/\\")
        print(f"[{APP_NAME}] Demo finalized and saved: tf/{demo_dir}/{self.current_demo_name}.dem", flush=True)
        self.send_cmd(f'echo "[P-REC External] >>> RECORDING STOPPED ({reason}) <<<"')
        self.send_cmd(f'echo "[P-REC External] Demo finalized: tf/{demo_dir}/{self.current_demo_name}.dem"')

        if self.cfg.prec_notify >= 1 and self.cfg.pr_message_stop:
            msg = self.cfg.pr_message_stop
            if self.is_scrim and "[P-REC]" in msg:
                msg = msg.replace("[P-REC]", "[P-REC Scrim]")
            self.send_cmd(msg)

        self.play_sound(is_start=False)
        if hasattr(self, "tray") and self.tray:
            self.tray.update_status("Connected to TF2")

    def send_cmd_response(self, cmd: str) -> str:
        """Sends command to TF2 and returns the response string synchronously."""
        if not self.sender:
            return ""
        try:
            if hasattr(self.sender, "send_command"):
                resp = self.sender.send_command(cmd)
                return resp or ""
        except Exception:
            pass
        return ""

    def send_cmd(self, cmd):
        if not self.sender:
            return
        try:
            self.sender.send_command(cmd)
        except Exception as e:
            print(f"[{APP_NAME} ERROR] Failed to send command '{cmd}': {e}", flush=True)

    def process_console_line(self, line):
        if not line:
            return

        map_match = re.search(r"(?:Map:\s+|map\s*:\s+)([a-zA-Z0-9_]+)", line, re.I)
        if map_match:
            new_map = map_match.group(1)
            if new_map != self.current_map:
                self.current_map = new_map
                prefix = self.get_demo_prefix()
                if prefix:
                    self.send_cmd(f'ds_prefix "{prefix}"')

        red_match = re.search(r'mp_tournament_redteamname(?: changed to)?\s+"?([^"\n\r]+)"?', line, re.I)
        if red_match:
            raw = red_match.group(1).strip()
            clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', raw.lower())
            clean = re.sub(r'_+', '_', clean).strip('_')
            if clean:
                self.current_red_team = clean

        blu_match = re.search(r'mp_tournament_blueteamname(?: changed to)?\s+"?([^"\n\r]+)"?', line, re.I)
        if blu_match:
            raw = blu_match.group(1).strip()
            clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', raw.lower())
            clean = re.sub(r'_+', '_', clean).strip('_')
            if clean:
                self.current_blu_team = clean

        conn_match = re.search(r"Connecting to\s+([a-zA-Z0-9_\-\.\:]+)", line)
        if conn_match:
            self.current_server_ip = conn_match.group(1)
            self.apply_league_cvars()

        if re.search(r"mp_tournament['\"]\s*(?:changed to\s+|=)?\s*['\"]?1", line, re.I):
            self.is_tournament = True
        elif re.search(r"mp_tournament['\"]\s*(?:changed to\s+|=)?\s*['\"]?0", line, re.I):
            self.is_tournament = False

        # Auto-detect league from whitelist or server hostname (in case configs loaded on server boot)
        if "mp_tournament_whitelist" in line or "hostname:" in line or "sv_tags" in line:
            for l_id, prof in self.profiles.items():
                if l_id == "custom":
                    continue
                patterns = [prof.get("prefix", l_id), l_id]
                for p in prof.get("server_config_patterns", []):
                    clean_p = re.sub(r'[^a-zA-Z0-9]', '', p)
                    if len(clean_p) >= 2:
                        patterns.append(clean_p)
                if any(re.search(pat, line, re.I) for pat in patterns):
                    self.is_tournament = True
                    is_scrim = bool(re.search(r"scrim", line, re.I))
                    if self.active_profile.get("id") != l_id or self.is_scrim != is_scrim:
                        self.active_profile = prof
                        self.is_scrim = is_scrim
                        mode_label = "SCRIM MODE (Practice)" if is_scrim else "OFFICIAL MATCH"
                        print(f"\n[{APP_NAME}] ⚡ AUTO-DETECTED LEAGUE FROM SERVER: {prof.get('name')} [{mode_label}]", flush=True)
                        print(f"[{APP_NAME}] Source: {line.strip()}", flush=True)
                        self.apply_league_cvars()
                        if hasattr(self, "tray") and self.tray:
                            self.tray.update_status(f"{prof.get('name')} [{mode_label}]")
                    break

        # 1. Auto-switch League Profile & Scrim / Match mode based on loaded server configs
        for l_id, prof in self.profiles.items():
            for pattern in prof.get("server_config_patterns", []):
                if re.search(pattern, line, re.I):
                    self.is_tournament = True
                    is_scrim = bool(re.search(r"scrim", line, re.I) or re.search(r"scrim", pattern, re.I))

                    # Switch profile or mode if changed
                    if self.active_profile.get("id") != l_id or self.is_scrim != is_scrim:
                        self.active_profile = prof
                        self.is_scrim = is_scrim
                        mode_label = "SCRIM MODE (Practice)" if is_scrim else "OFFICIAL MATCH"
                        print(f"\n[{APP_NAME}] ⚡ AUTO-SWITCHED LEAGUE PROFILE: {prof.get('name')} [{mode_label}]", flush=True)
                        print(f"[{APP_NAME}] Triggered by config execution: {line.strip()}", flush=True)
                        self.apply_league_cvars()
                        if hasattr(self, "tray") and self.tray:
                            self.tray.update_status(f"{prof.get('name')} [{mode_label}]")
                    return

        # Generic scrim config detection (e.g. exec scrim, loading scrim)
        if re.search(r"\b(exec\s+[a-zA-Z0-9_]*scrim|loading\s+scrim|scrim_config)\b", line, re.I):
            if not self.is_scrim:
                self.is_scrim = True
                print(f"\n[{APP_NAME}] ⚡ Switched to SCRIM MODE (Practice Match)", flush=True)
                self.apply_league_cvars()
                if hasattr(self, "tray") and self.tray:
                    self.tray.update_status(f"{self.active_profile.get('name')} [SCRIM]")

        # 2. Active League Chat Triggers (from leagues/*.json)
        for trigger in self.active_profile.get("chat_triggers", []):
            if re.search(trigger, line, re.I):
                self.is_tournament = True
                self.start_recording(f"{self.active_profile.get('name', 'League')} Trigger: {trigger}")
                return

        # 2. General Tournament Live Events
        if re.search(r"The match will begin in \d+ seconds", line, re.I):
            self.is_tournament = True
            if self.is_recording:
                self.send_cmd("ds_stop; ds_record")
                self.send_cmd('echo "[P-REC External] Tournament countdown begun — restarted demo for official match!"')
            else:
                self.start_recording("Tournament Countdown Started")
            return

        if re.search(r"Tournament mode restarted", line, re.I) or "mp_tournament_restart" in line:
            self.is_tournament = True
            if self.is_recording:
                self.send_cmd("ds_stop; ds_record")
                self.send_cmd('echo "[P-REC External] Tournament mode restarted — restarted demo for official match!"')
            else:
                self.start_recording("Tournament Mode Restarted (Live)")
            return

        # SOAP DM & ProperPregame (Universal Match Live Indicators on serveme.tf & competitive servers)
        if re.search(r"\[SOAP\]\s+(?:Soap DM|Plugins)\s+unloaded", line, re.I) or "[ProperPregame] Class limits restored" in line:
            self.is_tournament = True
            if self.is_recording:
                # If already recording during warmup, restart demo cleanly for official match
                self.stop_recording("Warmup Ended / Match Live")
                time.sleep(0.3)
                self.start_recording("Soap DM Unloaded (Official Match Live)")
            else:
                self.start_recording("Soap DM Unloaded / ProperPregame (Match Live)")
            return

        # Whitelist enforcement message: indicates active tournament whitelist on server
        if re.search(r"has been disabled in this tournament match by the server whitelist", line, re.I):
            self.is_tournament = True
            if self.cfg.prec_mode >= 2 and not self.is_recording:
                reconnect_note = "Mid-Match Reconnect" if self.was_in_match else "Mid-Game Join / Substitute"
                self.start_recording(f"Tournament Whitelist Active ({reconnect_note})")
            return

        if "[SOAP] Match is starting" in line or "[SOAP] Match begins" in line:
            self.is_tournament = True
            if self.is_recording:
                self.stop_recording("Warmup Ended / Match Live")
                time.sleep(0.3)
                self.start_recording("SOAP DM Match Live")
            else:
                self.start_recording("SOAP DM Match Live")
            return

        if re.search(r"(Both teams are ready|Match is LIVE|All players are ready)", line, re.I):
            self.is_tournament = True
            if self.is_recording:
                self.stop_recording("Pregame Ended / Match Live")
                time.sleep(0.3)
                self.start_recording("Competitive League Match Live")
            else:
                self.start_recording("Competitive League Match Live")
            return

        if 'World triggered "Round_Start"' in line:
            if self.is_tournament or self.cfg.prec_mode == 3:
                self.start_recording("Round Start")
            return

        # Player spawn or connection established -> inspect server tournament state
        if re.search(r"Client reached server_spawn", line, re.I) or re.search(r"Connected to\s+([a-zA-Z0-9_\-\.\:]+)", line) or "Team Fortress 2 is ready." in line:
            if self.cfg.prec_mode >= 2 and not self.is_recording:
                threading.Thread(target=self._check_midmatch_reconnect, daemon=True).start()

        if re.search(r"Commencing connection retry", line, re.I):
            if self.is_recording:
                self.stop_recording("Connection Retry")
            self.is_tournament = False
            return

        if re.search(r"Win panel created", line, re.I) or re.search(r'Team ".*" won the (match|round)', line, re.I):
            self.was_in_match = False
            if self.is_recording:
                self.stop_recording("Round/Match Win Detected")
                return

        # Demos.tf, LogsTF, and Soap DM Reload (Universal Competitive Match End Indicators)
        if "[demos.tf]: Demo recording completed" in line or "[LogsTF] Uploading logs" in line or re.search(r"\[SOAP\]\s+(?:Soap DM|Plugins)\s+(?:re)?loaded", line, re.I):
            self.was_in_match = False
            if self.is_recording:
                self.stop_recording("Match Ended (Logs.tf / demos.tf / Warmup Restored)")
                return

        if re.search(r"(Loading map|Disconnecting from server|Dropped .* from server)", line, re.I):
            if self.is_recording:
                self.stop_recording("Map Change / Server Disconnect")
            self.is_tournament = False
            return

    def _check_midmatch_reconnect(self):
        time.sleep(1.0)
        if not self.sender:
            return

        print(f"[{APP_NAME}] Checking server tournament status on connection...", flush=True)

        # 1. Direct synchronous query of mp_tournament from TF2 via RCON
        resp_tourney = self.send_cmd_response("mp_tournament")
        if re.search(r'mp_tournament[\'"]?\s*(?:changed to\s+|=)?\s*[\'"]?1', resp_tourney, re.I):
            self.is_tournament = True
        elif re.search(r'mp_tournament[\'"]?\s*(?:changed to\s+|=)?\s*[\'"]?0', resp_tourney, re.I):
            self.is_tournament = False

        if not self.is_tournament:
            self.send_cmd("mp_tournament")

        # 2. Query tournament team names and whitelist
        self.query_tournament_teams()
        resp_wl = self.send_cmd_response("mp_tournament_whitelist")
        if not resp_wl:
            self.send_cmd("mp_tournament_whitelist")
        else:
            for l_id, prof in self.profiles.items():
                if l_id == "custom":
                    continue
                patterns = [prof.get("prefix", l_id), l_id]
                for p in prof.get("server_config_patterns", []):
                    clean_p = re.sub(r'[^a-zA-Z0-9]', '', p)
                    if len(clean_p) >= 2:
                        patterns.append(clean_p)
                if any(re.search(pat, resp_wl, re.I) for pat in patterns):
                    self.is_tournament = True
                    is_scrim = bool(re.search(r"scrim", resp_wl, re.I))
                    if self.active_profile.get("id") != l_id or self.is_scrim != is_scrim:
                        self.active_profile = prof
                        self.is_scrim = is_scrim
                        mode_label = "SCRIM MODE (Practice)" if is_scrim else "OFFICIAL MATCH"
                        print(f"[{APP_NAME}] ⚡ AUTO-DETECTED LEAGUE FROM SERVER WHITELIST: {prof.get('name')} [{mode_label}]", flush=True)
                        self.apply_league_cvars()
                        if hasattr(self, "tray") and self.tray:
                            self.tray.update_status(f"{prof.get('name')} [{mode_label}]")
                    break

        # 3. Check if reconnecting to the same match or joining midgame as substitute
        is_reconnect = self.was_in_match and (
            (self.current_server_ip and self.current_server_ip == self.last_connected_server) or
            (self.current_map and self.current_map == self.last_connected_map)
        )

        if (self.is_tournament or is_reconnect) and self.cfg.prec_mode >= 2 and not self.is_recording:
            self.is_tournament = True
            if is_reconnect:
                print(f"[{APP_NAME}] ⚡ Rejoined active match on {self.current_map} ({self.current_server_ip}) — resuming recording!", flush=True)
                self.start_recording("Mid-Match Reconnect (ETF2L Rule 2.1 Recovery)")
            else:
                print(f"[{APP_NAME}] ⚡ Joined live tournament match in-progress (mp_tournament 1 active) — starting recording!", flush=True)
                self.start_recording("Mid-Game Substitute / Tournament Join (mp_tournament 1)")

    def run(self):
        prof_name = self.active_profile.get("name", self.cfg.prec_league.upper())
        print("\n" + "=" * 65, flush=True)
        print(f"   {APP_FULL_TITLE}   ", flush=True)
        print(f"   League Profile: {prof_name} (Rule Compliant)", flush=True)
        print("   [100% Vibecoded Edition - VAC-Safe, Zero Game Lag]", flush=True)
        print("=" * 65, flush=True)
        print("Waiting for Team Fortress 2 to boot / connect...", flush=True)

        while True:
            connected = False

            if self.cfg.prec_connection_mode in ("auto", "netcon"):
                try:
                    netcon = NetconClient(port=self.cfg.prec_netcon_port)
                    netcon.connect(timeout=1.0)
                    self.sender = netcon
                    self.client_mode = "netcon"
                    print(f"\n[CONNECTED] Netcon stream active on port {self.cfg.prec_netcon_port}!", flush=True)
                    self.send_cmd('echo ""')
                    self.send_cmd('echo "[P-REC External] ================================================"')
                    self.send_cmd(f'echo "[P-REC External] CONNECTED: {APP_FULL_TITLE} via NETCON"')
                    self.send_cmd(f'echo "[P-REC External] Active League: {prof_name} | Mode: {self.cfg.prec_mode}"')
                    self.send_cmd('echo "[P-REC External] All systems working! Match monitoring engaged."')
                    self.send_cmd('echo "[P-REC External] ================================================"')
                    self.send_cmd('echo ""')
                    self.apply_league_cvars()
                    connected = True
                    if hasattr(self, "tray") and self.tray:
                        self.tray.update_status(f"Connected (Netcon • {self.active_profile.get('name')})")
                    self._run_netcon_loop(netcon)
                except Exception:
                    pass

            if not connected and self.cfg.prec_connection_mode in ("auto", "rcon"):
                try:
                    rcon = SourceRcon(port=self.cfg.prec_rcon_port, password=self.cfg.prec_rcon_password, candidate_passwords=self.cfg.candidate_passwords)
                    rcon.connect(timeout=1.0)
                    if rcon.password != self.cfg.prec_rcon_password:
                        self.cfg.prec_rcon_password = rcon.password
                    self.sender = rcon
                    self.client_mode = "rcon"
                    print(f"\n[CONNECTED] RCON session active on port {self.cfg.prec_rcon_port} (DemoMan bridge)!", flush=True)
                    self.send_cmd('echo ""')
                    self.send_cmd('echo "[P-REC External] ================================================"')
                    self.send_cmd(f'echo "[P-REC External] CONNECTED: {APP_FULL_TITLE} via RCON"')
                    self.send_cmd(f'echo "[P-REC External] Active League: {prof_name} | Mode: {self.cfg.prec_mode}"')
                    self.send_cmd('echo "[P-REC External] All systems working! Match monitoring engaged."')
                    self.send_cmd('echo "[P-REC External] ================================================"')
                    self.send_cmd('echo ""')
                    self.apply_league_cvars()
                    connected = True
                    if hasattr(self, "tray") and self.tray:
                        self.tray.update_status(f"Connected (RCON • {self.active_profile.get('name')})")
                    self._run_rcon_loop(rcon)
                except Exception:
                    pass

            if not connected:
                time.sleep(2.0)

    def _run_netcon_loop(self, netcon: NetconClient):
        try:
            for line in netcon.line_stream():
                self.process_console_line(line)
        except Exception as e:
            print(f"[DISCONNECTED] Netcon connection lost: {e}", flush=True)
        finally:
            if self.is_recording:
                self.stop_recording("TF2 Closed / Crashed")
            netcon.close()
            self.sender = None
            if hasattr(self, "tray") and self.tray:
                self.tray.update_status("Waiting for TF2...")
            print("[IDLE] Waiting for TF2...", flush=True)

    def _run_rcon_loop(self, rcon: SourceRcon):
        tf_dir = Path(self.cfg.prec_tf_path) if self.cfg.prec_tf_path else detect_tf2_directory()
        if not tf_dir or not tf_dir.exists():
            print(f"[WARNING] Could not locate TF2 /tf/ directory for console.log!", flush=True)
            print("          Please set 'prec_tf_path' in your settings config.", flush=True)
            time.sleep(3.0)
            return

        # Ensure TF2 actively writes console output to console.log (even without -condebug)
        try:
            rcon.send_command('con_logfile "console.log"')
        except Exception:
            pass

        log_path = tf_dir / "console.log"
        print(f"[TAILER] Monitoring console log at: {log_path}", flush=True)

        # Pre-scan recent console.log lines to detect current map & server state immediately
        if log_path.exists():
            try:
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f_init:
                    f_init.seek(0, os.SEEK_END)
                    size = f_init.tell()
                    f_init.seek(max(0, size - 32768))
                    for init_line in f_init.readlines():
                        m = re.search(r"(?:Map:\s+|map\s*:\s+)([a-zA-Z0-9_]+)", init_line, re.I)
                        if m:
                            self.current_map = m.group(1)
            except Exception:
                pass

        if self.current_map:
            prefix = self.get_demo_prefix()
            if prefix:
                self.send_cmd(f'ds_prefix "{prefix}"')
            print(f"[{APP_NAME}] Current map detected: {self.current_map} | Demo Prefix: {prefix}", flush=True)

        tailer = ConsoleLogTailer(log_path)
        self.tailer = tailer

        try:
            for line in tailer.tail():
                self.process_console_line(line)
        except Exception as e:
            print(f"[DISCONNECTED] RCON/Tailer interrupted: {e}", flush=True)
        finally:
            if self.is_recording:
                self.stop_recording("TF2 Closed / Crashed")
            rcon.close()
            tailer.stop()
            self.sender = None
            if hasattr(self, "tray") and self.tray:
                self.tray.update_status("Waiting for TF2...")
            print("[IDLE] Waiting for TF2...", flush=True)


# ====================================================================
# Entry Point & Config Discovery
# ====================================================================

def find_existing_config():
    """Searches standard paths for existing PREC_Settings.cfg or Settings.cfg."""
    app_dir = get_app_dir()
    search_dirs = [
        Path.cwd(),
        app_dir,
        app_dir / "cfg",
    ]

    tf_dir = detect_tf2_directory()
    if tf_dir:
        search_dirs.extend([
            tf_dir / f"custom/{APP_NAME}/cfg",
            tf_dir / f"custom/{APP_NAME}",
            tf_dir / "custom/P-REC/cfg",
            tf_dir / "custom/P-REC",
            tf_dir / "custom/prec64/cfg",
            tf_dir / "custom/prec64",
            tf_dir / "custom",
            tf_dir / "cfg",
        ])

    for s_dir in search_dirs:
        for fname in DEFAULT_CONFIG_FILES:
            cand = s_dir / fname
            if cand.exists():
                return cand.resolve()
    return None


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            h_con = ctypes.windll.kernel32.GetConsoleWindow()
            if h_con and any(arg in sys.argv for arg in ("--tray", "--minimized", "--silent", "--daemon")):
                ctypes.windll.user32.ShowWindow(h_con, 0)  # SW_HIDE
        except Exception:
            pass

    if any(arg in sys.argv for arg in ("--uninstall", "-u", "/uninstall")):
        run_uninstaller()
        sys.exit(0)

    if any(arg in sys.argv for arg in ("--shortcut", "--create-shortcut")):
        create_desktop_shortcut()
        sys.exit(0)

    # Ensure single instance to prevent dual-process conflicts
    acquire_single_instance_lock()

    # Intercept console window close so crossing out hides to hidden pictograms
    setup_console_close_protection()

    force_wizard = "--install" in sys.argv or "--setup" in sys.argv

    if is_interactive() and not force_wizard and not any(arg in sys.argv for arg in ("--no-update", "--daemon")):
        check_for_updates(interactive=True)

    if force_wizard:
        cfg_path = run_setup_wizard()
    else:
        existing_cfg = find_existing_config()
        if existing_cfg:
            cfg_path = existing_cfg
        else:
            # First-time run: launch interactive setup wizard
            cfg_path = run_setup_wizard()

    config = PrecConfig(cfg_path)
    engine = PrecEngine(config)
    engine.run()
