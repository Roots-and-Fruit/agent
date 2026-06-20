"""Minimal DataForSEO REST client (stdlib only)."""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://api.dataforseo.com/v3"


def agent_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_env(env_path: Path | None = None) -> dict[str, str]:
    path = env_path or (agent_root() / ".env")
    env: dict[str, str] = {}
    if not path.is_file():
        return env
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def credentials(env_path: Path | None = None) -> tuple[str, str]:
    env = load_env(env_path)
    username = env.get("DATAFORSEO_USERNAME") or os.environ.get("DATAFORSEO_USERNAME", "")
    password = env.get("DATAFORSEO_PASSWORD") or os.environ.get("DATAFORSEO_PASSWORD", "")
    if not username.strip() or not password.strip():
        raise RuntimeError(
            "Missing DATAFORSEO_USERNAME or DATAFORSEO_PASSWORD in agent/.env"
        )
    return username.strip(), password.strip()


def post(endpoint: str, payload: list | dict, *, timeout: int = 120) -> dict:
    username, password = credentials()
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode())
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DataForSEO HTTP {exc.code}: {detail[:500]}") from exc
    task = (data.get("tasks") or [{}])[0]
    code = task.get("status_code")
    if code != 20000:
        raise RuntimeError(f"DataForSEO task error {code}: {task.get('status_message')}")
    return data
