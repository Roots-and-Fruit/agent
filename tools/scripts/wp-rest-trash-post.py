#!/usr/bin/env python3
"""Move a WordPress post to trash via REST (escape hatch — no delete ability)."""

from __future__ import annotations

import argparse
import base64
import json
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


def site_base(env: dict[str, str]) -> str:
    url = env.get("ROOTSANDFRUIT_MCP_URL", "").strip().rstrip("/")
    if "/wp-json/" in url:
        return url.split("/wp-json/")[0]
    return url


def trash_post(env: dict[str, str], post_id: int, force: bool = False) -> dict:
    user = env.get("ROOTSANDFRUIT_MCP_USERNAME", "").strip()
    password = env.get("ROOTSANDFRUIT_MCP_PASSWORD", "").strip()
    base = site_base(env)
    if not base or not user or not password:
        raise SystemExit("Set ROOTSANDFRUIT_MCP_URL, ROOTSANDFRUIT_MCP_USERNAME, ROOTSANDFRUIT_MCP_PASSWORD")

    auth = base64.b64encode(f"{user}:{password}".encode()).decode()
    qs = "?force=true" if force else ""
    req = urllib.request.Request(
        f"{base}/wp-json/wp/v2/posts/{post_id}{qs}",
        method="DELETE",
        headers={"Authorization": f"Basic {auth}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post_id", type=int, nargs="+", help="Post ID(s) to trash")
    parser.add_argument("--force", action="store_true", help="Permanently delete (requires cap)")
    parser.add_argument("--env", type=Path, default=Path(__file__).resolve().parents[2] / ".env")
    args = parser.parse_args()

    env = load_dotenv(args.env)
    for post_id in args.post_id:
        try:
            result = trash_post(env, post_id, force=args.force)
            status = result.get("status", "?")
            title = result.get("title", {}).get("rendered", "")
            print(f"OK post {post_id} -> {status} {title!r}")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"FAIL post {post_id}: HTTP {exc.code} {body}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
