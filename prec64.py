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
import time
import socket
import struct
import re
import json
import shutil
import threading
import secrets
import subprocess
from pathlib import Path

APP_NAME = "P-REC External"
APP_VERSION = "1.0.0"
APP_FULL_TITLE = f"P-REC External v{APP_VERSION}"
DEFAULT_CONFIG_FILES = ["PREC_Settings.cfg", "Settings.cfg"]

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
            r"All players are ready"
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
            r"All players are ready"
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
            r"All players are ready"
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
        self.prec_screens = 1             # Status & scoreboard screenshot on round/match end
        self.prec_notify = 1
        self.prec_min_streak = 3
        self.prec_kill_delay = 15
        self.prec_log = 0
        self.prec_delete_useless_demo = 0 # 0=never delete (mandatory across all leagues)
        self.prec_stv_status = 1
        self.prec_tag = ""

        # Chat Aliases
        self.pr_message_start = "say_team [P-REC] Recording started."
        self.pr_message_stop = "say_team [P-REC] Stop recording."
        self.pr_message_mark = "say_team [P-REC] Bookmark placed."

        # Connection Settings
        self.prec_connection_mode = "auto" # "auto", "netcon", or "rcon"
        self.prec_rcon_port = 27969
        self.prec_rcon_password = ""
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
                elif key in ("prec_dir", "dir"):
                    self.prec_dir = val
                elif key in ("prec_sound", "sound"):
                    self.prec_sound = int(val)
                elif key in ("prec_popup", "popup"):
                    self.prec_popup = int(val)
                elif key in ("prec_hide_to_tray", "hide_to_tray", "prec_tray"):
                    self.prec_hide_to_tray = int(val)
                elif key in ("prec_screens", "screens"):
                    self.prec_screens = int(val)
                elif key in ("prec_notify", "notify"):
                    self.prec_notify = int(val)
                elif key in ("prec_min_streak", "min_streak"):
                    self.prec_min_streak = int(val)
                elif key in ("prec_kill_delay", "kill_delay"):
                    self.prec_kill_delay = int(val)
                elif key in ("prec_log", "log"):
                    self.prec_log = int(val)
                elif key in ("prec_delete_useless_demo", "delete_useless_demo"):
                    self.prec_delete_useless_demo = int(val)
                elif key in ("prec_stv_status", "stv_status"):
                    self.prec_stv_status = int(val)
                elif key in ("prec_tag", "tag"):
                    self.prec_tag = val
                elif key in ("prec_connection_mode", "connection_mode"):
                    self.prec_connection_mode = val.lower()
                elif key in ("prec_rcon_port", "rcon_port"):
                    self.prec_rcon_port = int(val)
                elif key in ("prec_rcon_password", "rcon_password"):
                    self.prec_rcon_password = val
                elif key in ("prec_netcon_port", "netcon_port"):
                    self.prec_netcon_port = int(val)
                elif key in ("prec_tf_path", "tf_path"):
                    self.prec_tf_path = val

        # Auto-detect DemoMan or generate secure password if not set or default
        demoman = detect_demoman_config()
        if not self.prec_rcon_password or self.prec_rcon_password.lower() in ("changeme", "generate", ""):
            if demoman.get("rcon_password"):
                self.prec_rcon_password = demoman["rcon_password"]
                self._save_password_to_cfg(self.prec_rcon_password)
                print(f"[DEMOMAN] Automatically adopted RCON password from DemoMan: {self.prec_rcon_password}", flush=True)
            else:
                generated_pw = secrets.token_hex(6)
                self.prec_rcon_password = generated_pw
                self._save_password_to_cfg(generated_pw)
                print("\n" + "=" * 65, flush=True)
                print(" [SECURITY] Generated new secure RCON password: " + generated_pw, flush=True)
                print(f" Updated {self.cfg_path.name} automatically.", flush=True)
                print(f" Ensure your Steam launch option has: +rcon_password {generated_pw}", flush=True)
                print("=" * 65 + "\n", flush=True)

        if not self.prec_tf_path and demoman.get("tf_path"):
            self.prec_tf_path = str(demoman["tf_path"].resolve())

        print(f"[CONFIG] Loaded configuration from {self.cfg_path.resolve()}", flush=True)
        print(f"         League Profile: {self.prec_league.upper()} | Mode: {self.prec_mode} | Connection: {self.prec_connection_mode}", flush=True)

    def _save_password_to_cfg(self, new_pw):
        if not self.cfg_path.exists():
            return
        try:
            with open(self.cfg_path, "r", encoding="utf-8") as f:
                content = f.read()

            pattern = r'((?:prec_)?rcon_password\s+)("[^"]*"|\S+)'
            replacement = f'\\1"{new_pw}"'
            new_content = re.sub(pattern, replacement, content)

            with open(self.cfg_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        except Exception as e:
            print(f"[CONFIG WARNING] Could not write generated password to cfg: {e}", flush=True)

    def _generate_default_cfg(self):
        default_content = """// ====================================================================
// P-REC: Point-of-view Recording External Companion
// ====================================================================
// ⚠️ 100% Vibecoded Application — Use at your own risk.
// ====================================================================

prec_league              "etf2l"
prec_mode                2
prec_dir                 "demos"
prec_sound               1
prec_hide_to_tray        1
prec_screens             1
prec_notify              1
prec_min_streak          3
prec_kill_delay          15
prec_log                 0
prec_delete_useless_demo 0
prec_stv_status          1
prec_tag                 ""

alias pr_message_start "say_team [P-REC] Recording started."
alias pr_message_stop  "say_team [P-REC] Stop recording."
alias pr_message_mark  "say_team [P-REC] Bookmark placed."

prec_connection_mode     "auto"
prec_rcon_port           27969
prec_rcon_password       "changeme"
prec_netcon_port         2121
prec_tf_path             ""
"""
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            f.write(default_content)


# ====================================================================
# Directory & Process Helpers (with DemoMan Auto-Detection)
# ====================================================================

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


def get_app_dir():
    """Gets true directory whether running as a .py script or compiled PyInstaller binary."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def detect_tf2_directory():
    """Attempts to find the tf/ directory on Windows and Linux, checking DemoMan config first."""
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


def scan_cfg_candidates(tf_path: Path):
    """
    Audits tf/cfg/overrides and tf/cfg/ primarily, plus subfolders,
    looking for autoexecs, overrides, and configs containing demo settings.
    """
    cfg_dir = tf_path / "cfg"
    if not cfg_dir.exists():
        return []

    primary_candidates = [
        cfg_dir / "overrides/autoexec.cfg",
        cfg_dir / "autoexec.cfg",
        cfg_dir / "overrides/game_overrides.cfg",
    ]

    found = []
    seen = set()

    # Check primary locations
    for p in primary_candidates:
        if p.exists():
            found.append(p)
            seen.add(str(p.resolve()).lower())
        elif p.name == "autoexec.cfg" and p.parent.exists():
            # If autoexec does not exist yet, we can create it
            found.append(p)
            seen.add(str(p.resolve()).lower())

    # Quick scan of all cfg files in subfolders for demo commands or peachrec
    for p in cfg_dir.glob("**/*.cfg"):
        resolved_str = str(p.resolve()).lower()
        if resolved_str in seen:
            continue
        if "prec" in p.name.lower() or "settings" in p.name.lower():
            continue

        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                head = f.read(4096)
            if any(k in head for k in ("ds_enable", "ds_autodelete", "peachrec")):
                found.append(p)
                seen.add(resolved_str)
        except Exception:
            pass

    return found


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


# ====================================================================
# Interactive First-Time Installation Wizard
# ====================================================================

def run_setup_wizard():
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

        if not sys.stdin.isatty():
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
        if sys.stdin.isatty():
            do_clean = input("Would you like to automatically clean up these interfering files? [Y/n]: ").strip().lower()
        else:
            do_clean = "y"

        if do_clean != 'n':
            for c in custom_conflicts:
                clean_conflict(c)
            print("[OK] Interfering mod elements cleaned up successfully!\n", flush=True)
    else:
        print("[OK] No conflicting mods found in /tf/custom/.\n", flush=True)

    # 3. Target installation in tf/custom/P-REC
    custom_dir = tf_path / "custom"
    app_install_dir = custom_dir / "P-REC"
    print(f"Target installation directory:\n -> {app_install_dir.resolve()}", flush=True)

    if sys.stdin.isatty():
        confirm_custom = input("Install app and settings into this custom folder for easy file management? [Y/n]: ").strip().lower()
    else:
        confirm_custom = "y"

    if confirm_custom != 'n':
        app_install_dir.mkdir(parents=True, exist_ok=True)
        target_dir = app_install_dir
    else:
        target_dir = get_app_dir()

    # 4. Choose League Profile (Modular JSON profiles)
    discovered_leagues = load_league_profiles(tf_path)
    print("\nSelect your primary competitive league profile (modular JSON ruleset):", flush=True)
    league_keys = list(discovered_leagues.keys())
    for idx, l_key in enumerate(league_keys, 1):
        l_info = discovered_leagues[l_key]
        print(f"  [{idx}] {l_info.get('name', l_key.upper())} ({l_key})", flush=True)

    if sys.stdin.isatty():
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
        if sys.stdin.isatty():
            use_demo = input(f"Adopt DemoMan's password ({d_pw})? [Y/n]: ").strip().lower()
            if use_demo != 'n':
                rcon_pw = d_pw
        else:
            rcon_pw = d_pw

    if not rcon_pw and sys.stdin.isatty():
        has_rcon = input("Do you already have an existing RCON password? [y/N]: ").strip().lower()
        if has_rcon == 'y':
            rcon_pw = input("Enter your existing RCON password: ").strip()

    if not rcon_pw:
        rcon_pw = secrets.token_hex(6)
        print(f"[SECURITY] Generated secure random RCON password: {rcon_pw}", flush=True)

    # 6. Write PREC_Settings.cfg to target_dir
    cfg_target = target_dir / "PREC_Settings.cfg"
    write_wizard_config(cfg_target, selected_league, rcon_pw, str(tf_path.resolve()))
    print(f"[OK] Configuration saved: {cfg_target.resolve()}", flush=True)

    # 7. Copy binary / script & leagues directory into tf/custom/P-REC if requested
    current_exe = Path(sys.executable) if getattr(sys, 'frozen', False) else get_app_dir() / "prec64.py"
    if target_dir != get_app_dir() and current_exe.exists():
        try:
            dest_file = target_dir / current_exe.name
            shutil.copy2(current_exe, dest_file)
            print(f"[OK] Copied application binary to: {dest_file.resolve()}", flush=True)
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

    # 8. Audit and update tf/cfg/overrides and tf/cfg/ (One-by-one or in Bulk)
    print("\n[AUDIT] Scanning tf/cfg/overrides/ and tf/cfg/ for pre-existing configs...", flush=True)
    cfg_candidates = scan_cfg_candidates(tf_path)

    if cfg_candidates:
        print("=" * 65, flush=True)
        print(f"Found {len(cfg_candidates)} configuration file(s):", flush=True)
        for idx, cand in enumerate(cfg_candidates, 1):
            st = "(Exists)" if cand.exists() else "(Will be created)"
            print(f"  [{idx}] {cand.relative_to(tf_path)} {st}", flush=True)
        print("=" * 65, flush=True)
        print("How would you like to update pre-existing configs with optimal P-REC settings?")
        print("  [1] Bulk apply to all files (Recommended)")
        print("  [2] Review and approve changes file-by-file (one by one)")
        print("  [3] Skip all (make no changes to existing files)")

        if sys.stdin.isatty():
            apply_mode = input("Enter choice [1-3, default 1]: ").strip()
        else:
            apply_mode = "1"

        if apply_mode == "2":
            # File by file
            for cand in cfg_candidates:
                rel = cand.relative_to(tf_path)
                print(f"\n--- Reviewing: {rel} ---", flush=True)
                print("Proposed additions / updates:\n" + get_recommended_snippet(cfg_target.name), flush=True)
                if sys.stdin.isatty():
                    ans = input(f"Apply changes to {rel}? [Y/n]: ").strip().lower()
                else:
                    ans = "y"
                if ans != 'n':
                    apply_cfg_update(cand, cfg_target.name)
                    print(f"[OK] Updated {rel}", flush=True)
                else:
                    print(f"[SKIP] Skipped {rel}", flush=True)
        elif apply_mode != "3":
            # Bulk
            for cand in cfg_candidates:
                apply_cfg_update(cand, cfg_target.name)
                print(f"[OK] Updated {cand.relative_to(tf_path)}", flush=True)
        else:
            print("[SKIP] Skipped updating cfg files.", flush=True)

    # 9. Output Steam Launch Option
    print("\n" + "=" * 65, flush=True)
    print("             SETUP COMPLETE! STEAM LAUNCH OPTIONS:             ", flush=True)
    print("=" * 65, flush=True)
    print("Copy and paste this into TF2's Launch Options in Steam:\n", flush=True)
    if sys.platform == "win32":
        run_exe = target_dir / ("prec64.exe" if getattr(sys, 'frozen', False) else "prec64.py")
        if run_exe.suffix == ".exe":
            print(f'cmd /c start "" "{run_exe.resolve()}" & %command% -condebug -usercon +rcon_password {rcon_pw} +ip 0.0.0.0 +hostport 27969 +net_start\n', flush=True)
        else:
            print(f'cmd /c start "" python "{run_exe.resolve()}" & %command% -condebug -usercon +rcon_password {rcon_pw} +ip 0.0.0.0 +hostport 27969 +net_start\n', flush=True)
    else:
        run_exe = target_dir / "prec64"
        print(f'"{run_exe.resolve()}" & %command% -condebug -usercon +rcon_password {rcon_pw} +ip 0.0.0.0 +hostport 27969 +net_start\n', flush=True)
    print("=" * 65, flush=True)

    if sys.stdin.isatty():
        input("\nPress Enter to continue launching P-REC...")
    return cfg_target


def write_wizard_config(path: Path, league: str, rcon_pw: str, tf_path: str):
    content = f"""// ====================================================================
// {APP_FULL_TITLE}
// ====================================================================
// ⚠️ 100% Vibecoded Application — Use at your own risk.
// ====================================================================

// Application Version
prec_version             "{APP_VERSION}"

// League Ruleset Profile: "etf2l", "rgl", "ozfortress", "matcha", "cltf2", "custom"
// Or any custom profile defined in leagues/<id>.json
prec_league              "{league}"

// Recording Modes & Triggers
prec_mode                2      // 2 = Record active tournament matches only
prec_dir                 "demos"// Subfolder in /tf/ for recorded demos
prec_sound               1      // Audio cue on start/stop
prec_hide_to_tray        1      // Hide console window to system tray (hidden pictograms)
prec_screens             1      // Screenshot of status & scoreboard at match end
prec_notify              1      // 1 = team chat start/stop announcement

// Killstreaks & Demos
prec_min_streak          3
prec_kill_delay          15
prec_log                 0
prec_delete_useless_demo 0      // 0 = never delete (mandatory for league compliance)
prec_stv_status          1
prec_tag                 ""

// Chat Announcements
alias pr_message_start "say_team [P-REC] Recording started."
alias pr_message_stop  "say_team [P-REC] Stop recording."
alias pr_message_mark  "say_team [P-REC] Bookmark placed."

// Connection Settings
prec_connection_mode     "auto"
prec_rcon_port           27969
prec_rcon_password       "{rcon_pw}"
prec_netcon_port         2121
prec_tf_path             "{tf_path}"
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ====================================================================
# Source RCON Implementation (Zero-Dependency)
# ====================================================================

class SourceRcon:
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_AUTH = 3
    SERVERDATA_RESPONSE_VALUE = 0
    SERVERDATA_AUTH_RESPONSE = 2

    def __init__(self, host="127.0.0.1", port=27969, password=""):
        self.host = host
        self.port = port
        self.password = password
        self.sock = None
        self.req_id = 1
        self.lock = threading.Lock()

    def connect(self, timeout=3.0):
        self.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((self.host, self.port))
        self.sock = s
        self._send_raw(self.SERVERDATA_AUTH, self.password)
        resp_id, resp_type, _ = self._read_raw()
        if resp_type != self.SERVERDATA_AUTH_RESPONSE or resp_id == -1:
            self.close()
            raise PermissionError("RCON password rejected by TF2")
        return True

    def _send_raw(self, packet_type, body):
        self.req_id += 1
        payload = body.encode("utf-8", errors="replace") + b"\x00\x00"
        packet_size = 4 + 4 + len(payload)
        packet = struct.pack("<iii", packet_size, self.req_id, packet_type) + payload
        self.sock.sendall(packet)
        return self.req_id

    def _read_raw(self):
        size_header = self.sock.recv(4)
        if not size_header or len(size_header) < 4:
            raise ConnectionResetError("RCON socket disconnected")
        size = struct.unpack("<i", size_header)[0]
        data = b""
        while len(data) < size:
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                break
            data += chunk
        req_id, packet_type = struct.unpack("<ii", data[:8])
        body = data[8:-2].decode("utf-8", errors="replace")
        return req_id, packet_type, body

    def send_command(self, cmd):
        with self.lock:
            if not self.sock:
                self.connect()
            self._send_raw(self.SERVERDATA_EXECCOMMAND, cmd)
            req_id, packet_type, body = self._read_raw()
            return body

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
            while self.running:
                line = f.readline()
                if line:
                    yield line.strip("\r\n")
                else:
                    time.sleep(0.05)

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
        self.status = "Waiting for TF2..."
        self.hwnd = None
        self.nid = None
        self.running = True
        self.thread = None
        self.console_visible = True

    def start(self):
        if sys.platform != "win32":
            return
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
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
                self.console_visible = False
        except Exception:
            pass

    def show_console(self):
        if sys.platform != "win32":
            return
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                self.console_visible = True
        except Exception:
            pass

    def toggle_console(self):
        if self.console_visible:
            self.hide_console()
        else:
            self.show_console()

    def close(self):
        self.running = False
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

            WM_USER = 0x0400
            WM_TRAY = WM_USER + 20
            WM_RBUTTONUP = 0x0205
            WM_LBUTTONDBLCLK = 0x0203
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
            TPM_RIGHTBUTTON = 0x0002
            TPM_BOTTOMALIGN = 0x0020

            ID_STATUS = 1001
            ID_TOGGLE_CONSOLE = 1002
            ID_SETTINGS = 1003
            ID_CUSTOM_DIR = 1004
            ID_EXIT = 1005

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

                console_label = "Hide Console Window" if self.console_visible else "Show Console Window"
                user32.AppendMenuW(h_menu, MF_STRING, ID_TOGGLE_CONSOLE, console_label)
                user32.AppendMenuW(h_menu, MF_STRING, ID_SETTINGS, "Go to Settings (PREC_Settings.cfg)")
                user32.AppendMenuW(h_menu, MF_STRING, ID_CUSTOM_DIR, "Open tf/custom/ Folder")
                user32.AppendMenuW(h_menu, MF_SEPARATOR, 0, None)
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
                    elif lparam == WM_LBUTTONDBLCLK:
                        self.open_settings()
                    return 0
                elif msg == WM_COMMAND:
                    cmd_id = wintypes.LOWORD(wparam)
                    if cmd_id == ID_TOGGLE_CONSOLE:
                        self.toggle_console()
                    elif cmd_id == ID_SETTINGS:
                        self.open_settings()
                    elif cmd_id == ID_CUSTOM_DIR:
                        self.open_custom_folder()
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

            wc = WNDCLASSEXW()
            wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
            wc.lpfnWndProc = self._wnd_proc
            wc.hInstance = h_inst
            wc.lpszClassName = class_name
            user32.RegisterClassExW(ctypes.byref(wc))

            self.hwnd = user32.CreateWindowExW(
                0, class_name, "P-REC Tray",
                0, 0, 0, 0, 0,
                None, None, h_inst, None
            )

            ico_file = get_icon_path("supreme_soviet.ico")
            h_icon = None
            if ico_file:
                h_icon = user32.LoadImageW(None, str(ico_file), IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE)
            if not h_icon:
                h_icon = user32.LoadIconW(None, 32512)

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
        self.last_record_toggle = 0.0
        self.client_mode = None
        self.sender = None
        self.tailer = None
        self.current_server_ip = ""
        self.current_map = ""
        self.profiles = load_league_profiles(self.cfg.prec_tf_path)
        league_id = self.cfg.prec_league.lower()
        self.active_profile = self.profiles.get(league_id, self.profiles.get("custom", {}))

        # Windows System Tray
        self.tray = WindowsSystemTray(
            config_path=self.cfg.cfg_path,
            tf_path=self.cfg.prec_tf_path,
            on_exit_callback=self.stop_all
        )
        self.tray.start()

        # Hide console to system tray (hidden pictograms) if configured
        if getattr(self.cfg, "prec_hide_to_tray", 1) and sys.platform == "win32":
            if not any(arg in sys.argv for arg in ("--console", "--debug", "--install", "--setup")):
                self.tray.hide_console()

    def stop_all(self):
        print(f"\n[{APP_NAME}] Exit requested from System Tray. Shutting down...", flush=True)
        if self.is_recording:
            try:
                self.stop_recording("User Exit")
            except Exception:
                pass
        if self.tray:
            self.tray.close()
        os._exit(0)

    def apply_league_cvars(self):
        prof_name = self.active_profile.get("name", self.cfg.prec_league.upper())
        mode_label = "SCRIM (Practice)" if self.is_scrim else "OFFICIAL MATCH"
        print(f"[{APP_NAME}] Applying cvars for: {prof_name} [{mode_label}]", flush=True)

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

        # Prefix logic: if prec_tag set by user, use that. Otherwise use scrim_prefix or base prefix
        if self.cfg.prec_tag:
            prefix = self.cfg.prec_tag
        elif self.is_scrim:
            prefix = self.active_profile.get("scrim_prefix", f"{self.active_profile.get('prefix', self.cfg.prec_league)}_scrim")
        else:
            prefix = self.active_profile.get("prefix", self.cfg.prec_league)

        if prefix:
            self.send_cmd(f'ds_prefix "{prefix}"')

        ds_mode = self.active_profile.get("ds_enable", 0)
        self.send_cmd(f"ds_enable {ds_mode}")
        if self.active_profile.get("server_demo_checker_bypass"):
            print(f"        [{prof_name}] Set ds_enable {ds_mode} & ds_autodelete 0 for Server Demo Checker compliance.", flush=True)
        else:
            print(f"        [{prof_name}] Set ds_enable {ds_mode} (manual mode: auto-triggered on match live).", flush=True)

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

    def start_recording(self, reason="Match Live"):
        now = time.time()
        if self.is_recording or (now - self.last_record_toggle < 3.0):
            return

        self.last_record_toggle = now
        self.is_recording = True
        sub_type = "Scrim Practice" if self.is_scrim else "Official Match"
        print(f"\n[{APP_NAME}] >>> START RECORDING <<< ({sub_type}: {reason})", flush=True)

        if self.active_profile.get("server_demo_checker_bypass"):
            self.send_cmd("ds_stop; ds_record")
        else:
            self.send_cmd("ds_record")

        if self.cfg.prec_notify >= 1 and self.cfg.pr_message_start:
            msg = self.cfg.pr_message_start
            if self.is_scrim and "[P-REC]" in msg:
                msg = msg.replace("[P-REC]", "[P-REC Scrim]")
            self.send_cmd(msg)

        self.play_sound(is_start=True)
        if hasattr(self, "tray") and self.tray:
            self.tray.update_status(f"Recording ({sub_type})")

    def stop_recording(self, reason="Match Finished"):
        now = time.time()
        if not self.is_recording or (now - self.last_record_toggle < 3.0):
            return

        self.last_record_toggle = now
        self.is_recording = False
        print(f"\n[{APP_NAME}] >>> STOP RECORDING <<< ({reason})", flush=True)

        # In scrim mode, skip mandatory status screenshots unless explicitly configured
        should_screen = (self.cfg.prec_screens and not self.is_scrim) or (self.active_profile.get("mandatory_status_screenshot") and not self.is_scrim)
        if should_screen:
            print(f"[{APP_NAME}] Capturing mandatory status & scoreboard screenshot...", flush=True)
            self.send_cmd("status; jpeg")
            time.sleep(0.4)

        self.send_cmd("ds_stop")

        if self.cfg.prec_notify >= 1 and self.cfg.pr_message_stop:
            msg = self.cfg.pr_message_stop
            if self.is_scrim and "[P-REC]" in msg:
                msg = msg.replace("[P-REC]", "[P-REC Scrim]")
            self.send_cmd(msg)

        self.play_sound(is_start=False)
        if hasattr(self, "tray") and self.tray:
            self.tray.update_status("Connected to TF2")

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

        map_match = re.search(r"Map:\s+([a-zA-Z0-9_]+)", line)
        if map_match:
            self.current_map = map_match.group(1)

        conn_match = re.search(r"Connecting to\s+([0-9\.\:]+)", line)
        if conn_match:
            self.current_server_ip = conn_match.group(1)
            self.apply_league_cvars()

        if "mp_tournament 1" in line or "mp_tournament changed to 1" in line:
            self.is_tournament = True
        elif "mp_tournament 0" in line or "mp_tournament changed to 0" in line:
            self.is_tournament = False

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
            self.start_recording("Tournament Countdown Started")
            return

        if re.search(r"Tournament mode restarted", line, re.I) or "mp_tournament_restart" in line:
            self.is_tournament = True
            self.start_recording("Tournament Mode Restarted (Live)")
            return

        if "[SOAP] Match is starting" in line or "[SOAP] Match begins" in line:
            self.is_tournament = True
            self.start_recording("SOAP DM Match Live")
            return

        if re.search(r"(Both teams are ready|Match is LIVE|All players are ready)", line, re.I):
            self.is_tournament = True
            self.start_recording("Competitive League Match Live")
            return

        if 'World triggered "Round_Start"' in line:
            if self.is_tournament or self.cfg.prec_mode == 3:
                self.start_recording("Round Start")
            return

        if re.search(r"Connected to\s+([0-9\.\:]+)", line) or "Team Fortress 2 is ready." in line:
            if self.cfg.prec_mode >= 2 and not self.is_recording:
                threading.Thread(target=self._check_midmatch_reconnect, daemon=True).start()

        if re.search(r"Win panel created", line, re.I) or re.search(r'Team ".*" won the (match|round)', line, re.I):
            if self.is_recording:
                self.stop_recording("Round/Match Win Detected")
                return

        if re.search(r"(Loading map|Disconnecting from server|Dropped .* from server)", line, re.I):
            if self.is_recording:
                self.stop_recording("Map Change / Server Disconnect")
            self.is_tournament = False
            return

    def _check_midmatch_reconnect(self):
        time.sleep(3.0)
        if not self.is_recording and self.sender:
            print(f"[{APP_NAME}] Verifying match state after connection...", flush=True)
            self.send_cmd("status")

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
                    self.apply_league_cvars()
                    connected = True
                    if hasattr(self, "tray") and self.tray:
                        self.tray.update_status(f"Connected (Netcon • {self.active_profile.get('name')})")
                    self._run_netcon_loop(netcon)
                except Exception:
                    pass

            if not connected and self.cfg.prec_connection_mode in ("auto", "rcon"):
                try:
                    rcon = SourceRcon(port=self.cfg.prec_rcon_port, password=self.cfg.prec_rcon_password)
                    rcon.connect(timeout=1.0)
                    self.sender = rcon
                    self.client_mode = "rcon"
                    print(f"\n[CONNECTED] RCON session active on port {self.cfg.prec_rcon_port} (DemoMan bridge)!", flush=True)
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

        log_path = tf_dir / "console.log"
        print(f"[TAILER] Monitoring console log at: {log_path}", flush=True)

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
    search_dirs = [
        Path.cwd(),
        get_app_dir(),
    ]

    tf_dir = detect_tf2_directory()
    if tf_dir:
        search_dirs.extend([
            tf_dir / f"custom/{APP_NAME}",
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
    force_wizard = "--install" in sys.argv or "--setup" in sys.argv

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
