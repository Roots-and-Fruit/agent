#!/usr/bin/env python3
"""Invoke one WordPress MCP ability via JSON-RPC (UTF-8 safe). Loads agent/.env."""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_dotenv(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.is_file():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def mcp_post(url: str, body: bytes, headers: dict[str, str]) -> urllib.response.addinfourl:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    return urllib.request.urlopen(req, timeout=120)


def invoke_ability(env: dict[str, str], ability_name: str, parameters: dict, session_id: str | None = None) -> tuple[dict, str]:
    url = env.get("ROOTSANDFRUIT_MCP_URL", "").strip()
    user = env.get("ROOTSANDFRUIT_MCP_USERNAME", "").strip()
    password = env.get("ROOTSANDFRUIT_MCP_PASSWORD", "").strip()
    if not url or not user or not password:
        raise SystemExit("Set ROOTSANDFRUIT_MCP_URL, ROOTSANDFRUIT_MCP_USERNAME, ROOTSANDFRUIT_MCP_PASSWORD in .env")

    auth = base64.b64encode(f"{user}:{password}".encode()).decode()
    base_headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }

    if not session_id:
        init_body = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "invoke-mcp-ability-py", "version": "1.0.0"},
                },
            }
        ).encode("utf-8")
        init_resp = mcp_post(url, init_body, base_headers)
        session_id = init_resp.headers.get("Mcp-Session-Id") or init_resp.headers.get("mcp-session-id")
        if not session_id:
            raise SystemExit("MCP initialize did not return Mcp-Session-Id header")

    exec_headers = {**base_headers, "Mcp-Session-Id": session_id}
    exec_body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "mcp-adapter-execute-ability",
                "arguments": {"ability_name": ability_name, "parameters": parameters},
            },
        },
        ensure_ascii=False,
    ).encode("utf-8")

    exec_resp = mcp_post(url, exec_body, exec_headers)
    payload = json.loads(exec_resp.read().decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(json.dumps(payload["error"], ensure_ascii=False))
    text = payload["result"]["content"][0]["text"]
    if not text or not text.strip():
        raise RuntimeError("Empty MCP ability response")
    return json.loads(text), session_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ability_name", help="e.g. rootsandfruit/blocks-update")
    parser.add_argument(
        "parameters",
        type=Path,
        help="Path to JSON parameters file (UTF-8)",
    )
    parser.add_argument(
        "--env",
        type=Path,
        default=Path(__file__).resolve().parents[2] / ".env",
        help="Path to agent/.env",
    )
    args = parser.parse_args()

    env = load_dotenv(args.env)
    parameters = json.loads(args.parameters.read_text(encoding="utf-8"))
    result, _session = invoke_ability(env, args.ability_name, parameters)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
