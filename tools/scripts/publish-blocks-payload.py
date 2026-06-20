#!/usr/bin/env python3
"""Push blocks-payload.json to an existing post via blocks-update (single MCP session)."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def load_invoke_module():
    spec = importlib.util.spec_from_file_location("invoke_mcp", SCRIPT_DIR / "invoke-mcp-ability.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path, help="blocks-payload.json from draft-md-to-blocks.py")
    parser.add_argument("--post-id", type=int, required=True)
    parser.add_argument("--env", type=Path, default=SCRIPT_DIR.parents[1] / ".env")
    parser.add_argument("--delay-ms", type=int, default=150, help="Pause between updates")
    args = parser.parse_args()

    invoke = load_invoke_module()
    env = invoke.load_dotenv(args.env)
    payload = json.loads(args.payload.read_text(encoding="utf-8"))
    blocks = payload.get("blocks") or []
    if not blocks:
        raise SystemExit("No blocks in payload")

    failed = 0
    for index, block in enumerate(blocks):
        update = {
            "post_id": args.post_id,
            "flat_index": index,
            "innerHTML": block.get("innerHTML", ""),
        }
        # core/list and core/table: attributes on update can wipe body content
        name = block.get("name", "")
        if block.get("attributes") and name not in ("core/list", "core/table"):
            update["attributes"] = block["attributes"]

        try:
            result, _session = invoke.invoke_ability(
                env,
                "rootsandfruit/blocks-update",
                update,
                session_id=None,
            )
            if not result.get("success"):
                raise RuntimeError(json.dumps(result, ensure_ascii=False))
            print(f"OK flat_index={index} {block.get('name')}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL flat_index={index} {block.get('name')}: {exc}", file=sys.stderr)
        if args.delay_ms > 0:
            time.sleep(args.delay_ms / 1000)

    if failed:
        raise SystemExit(f"{failed} block update(s) failed")
    print(f"Updated {len(blocks)} blocks on post {args.post_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
