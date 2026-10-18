"""Optional AI-agent adapters with fixed CLI invocation and environment-based secrets."""
from __future__ import annotations
import json, os, shutil, subprocess, urllib.error, urllib.request
from dataclasses import dataclass

@dataclass
class AgentReply:
    provider: str
    text: str
    ok: bool
    detail: str = ""

def _run_fixed_cli(executable: str, args: list[str], prompt: str, timeout: int = 90) -> AgentReply:
    path = shutil.which(executable)
    if not path:
        return AgentReply(executable, "", False, f"Commande {executable!r} introuvable.")
    try:
        completed = subprocess.run([path, *args], input=prompt, capture_output=True, text=True,
                                   timeout=timeout, check=False, shell=False)
    except subprocess.TimeoutExpired:
        return AgentReply(executable, "", False, "Délai d'attente dépassé.")
    except OSError as exc:
        return AgentReply(executable, "", False, str(exc))
    output = (completed.stdout or "").strip()
    if completed.returncode != 0:
        return AgentReply(executable, output, False, (completed.stderr or "Échec CLI").strip()[:1200])
    return AgentReply(executable, output, bool(output), "Aucune sortie." if not output else "")

def ask_opencode(prompt: str) -> AgentReply:
    return _run_fixed_cli("opencode", ["run"], prompt)

def ask_hermes(prompt: str) -> AgentReply:
    raw = os.getenv("HERMES_ARGS", "[]")
    try:
        args = json.loads(raw)
        if not isinstance(args, list) or not all(isinstance(x, str) for x in args):
            raise ValueError("HERMES_ARGS doit être une liste JSON de chaînes.")
    except (json.JSONDecodeError, ValueError) as exc:
        return AgentReply("hermes", "", False, str(exc))
    return _run_fixed_cli("hermes", args, prompt)

def ask_jev_compatible(prompt: str) -> AgentReply:
    base = os.getenv("JEV_BASE_URL", "").strip().rstrip("/")
    api_key = os.getenv("JEV_API_KEY", "").strip()
    model = os.getenv("JEV_MODEL", "").strip()
    if not base or not api_key or not model:
        return AgentReply("jev", "", False, "Configurez JEV_BASE_URL, JEV_API_KEY et JEV_MODEL.")
    payload = json.dumps({"model": model, "messages": [
        {"role": "system", "content": "Analyse les stratégies Forex, explique les risques et n'envoie aucun ordre."},
        {"role": "user", "content": prompt}], "temperature": 0.2}).encode("utf-8")
    request = urllib.request.Request(base + "/chat/completions", data=payload, method="POST",
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
        answer = data["choices"][0]["message"]["content"]
        return AgentReply("jev", str(answer), True)
    except (urllib.error.URLError, TimeoutError, KeyError, IndexError, ValueError, json.JSONDecodeError) as exc:
        return AgentReply("jev", "", False, "Appel API impossible : " + str(exc))

def ask_agent(prompt: str, preferred: str = "jev") -> AgentReply:
    providers = {"jev": ask_jev_compatible, "opencode": ask_opencode, "hermes": ask_hermes}
    order = [preferred] + [name for name in ("jev", "hermes", "opencode") if name != preferred]
    errors = []
    for name in order:
        reply = providers.get(name, ask_jev_compatible)(prompt)
        if reply.ok:
            return reply
        errors.append(name + ": " + (reply.detail or "indisponible"))
    return AgentReply("none", "", False, "Aucun agent disponible. " + " | ".join(errors))
