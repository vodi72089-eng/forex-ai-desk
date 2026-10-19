"""GitHub Releases updater for the packaged Windows executable."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

OWNER = "vodi72089-eng"
REPO = "forex-ai-desk"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
APP_NAME = "ForexAIDesk.exe"


class UpdateError(RuntimeError):
    pass


def _request(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Forex-AI-Desk-Updater",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def _version_tuple(value: str) -> tuple[int, ...]:
    nums = re.findall(r"\d+", value)
    return tuple(int(n) for n in nums) if nums else (0,)


def latest_release() -> dict[str, Any]:
    try:
        return json.loads(_request(API_URL).decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise UpdateError(f"Impossible de vérifier les mises à jour : {exc}") from exc


def check_for_update(current_version: str) -> dict[str, Any] | None:
    release = latest_release()
    tag = str(release.get("tag_name", "")).strip()
    remote_version = tag.lstrip("vV")
    if not remote_version:
        raise UpdateError("La dernière version publiée n'a pas de numéro de version.")
    if _version_tuple(remote_version) <= _version_tuple(current_version):
        return None
    assets = {str(a.get("name")): a for a in release.get("assets", [])}
    exe_asset = assets.get(APP_NAME)
    checksum_asset = assets.get(APP_NAME + ".sha256")
    if not exe_asset or not checksum_asset:
        raise UpdateError("La release existe, mais son EXE ou son fichier SHA-256 est absent.")
    return {
        "version": remote_version,
        "tag": tag,
        "name": str(release.get("name") or tag),
        "notes": str(release.get("body") or ""),
        "exe_url": str(exe_asset.get("browser_download_url") or ""),
        "checksum_url": str(checksum_asset.get("browser_download_url") or ""),
    }


def install_update(update: dict[str, Any]) -> None:
    if not getattr(sys, "frozen", False):
        raise UpdateError("L'auto-mise à jour fonctionne uniquement dans la version EXE installée.")
    destination = Path(sys.executable).resolve()
    if destination.name.lower() != APP_NAME.lower():
        raise UpdateError(f"Nom inattendu de l'application : {destination.name}")
    if not update.get("exe_url", "").startswith("https://github.com/"):
        raise UpdateError("URL de téléchargement non reconnue.")
    if not update.get("checksum_url", "").startswith("https://github.com/"):
        raise UpdateError("URL de checksum non reconnue.")

    try:
        exe_bytes = _request(update["exe_url"], timeout=120)
        checksum_text = _request(update["checksum_url"], timeout=30).decode("utf-8").strip()
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError) as exc:
        raise UpdateError(f"Échec du téléchargement : {exc}") from exc

    expected = checksum_text.split()[0].lower() if checksum_text else ""
    actual = hashlib.sha256(exe_bytes).hexdigest()
    if not re.fullmatch(r"[0-9a-f]{64}", expected) or actual != expected:
        raise UpdateError("Vérification SHA-256 échouée. Le fichier téléchargé n'a pas été installé.")

    update_dir = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "ForexAIDesk" / "updates"
    update_dir.mkdir(parents=True, exist_ok=True)
    staged_exe = update_dir / APP_NAME
    staged_exe.write_bytes(exe_bytes)

    # A separate script replaces the executable only after this process exits.
    script = update_dir / "apply_update.bat"
    log = update_dir / "update.log"
    script.write_text(
        "@echo off\r\n"
        "setlocal\r\n"
        f'set "SRC={staged_exe}"\r\n'
        f'set "DST={destination}"\r\n'
        f'set "LOG={log}"\r\n'
        "for /L %%i in (1,1,30) do (\r\n"
        "  copy /Y \"%SRC%\" \"%DST%\" >nul 2>&1 && goto installed\r\n"
        "  timeout /t 1 /nobreak >nul\r\n"
        ")\r\n"
        "echo Could not replace application file.>>\"%LOG%\"\r\n"
        "exit /b 1\r\n"
        ":installed\r\n"
        'start "" "%DST%"\r\n'
        "del \"%SRC%\" >nul 2>&1\r\n"
        "del \"%~f0\" >nul 2>&1\r\n",
        encoding="utf-8",
    )
    creation_flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    subprocess.Popen(
        ["cmd.exe", "/c", str(script)],
        cwd=str(update_dir),
        close_fds=True,
        creationflags=creation_flags,
    )
