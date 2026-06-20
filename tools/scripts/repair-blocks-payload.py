#!/usr/bin/env python3
"""Repair block innerHTML using ref-based replace (lists/tables) or flat_index update."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def load_invoke():
    spec = importlib.util.spec_from_file_location("invoke_mcp", SCRIPT_DIR / "invoke-mcp-ability.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path)
    parser.add_argument("--post-id", type=int, required=True)
    parser.add_argument("--delay-ms", type=int, default=800)
    args = parser.parse_args()

    invoke = load_invoke()
    env = invoke.load_dotenv(SCRIPT_DIR.parents[1] / ".env")
    payload = json.loads(args.payload.read_text(encoding="utf-8"))
    blocks = payload["blocks"]

    page, _ = invoke.invoke_ability(env, "rootsandfruit/blocks-get-page", {"post_id": args.post_id})
    live = page["data"]["blocks"]
    if len(live) != len(blocks):
        print(f"WARN live {len(live)} blocks vs payload {len(blocks)}", file=sys.stderr)

    failed = 0
    for index, block in enumerate(blocks):
        if index >= len(live):
            failed += 1
            continue
        ref = live[index].get("ref")
        name = block.get("name", "")
        inner = block.get("innerHTML", "")
        try:
            if name in ("core/list", "core/table"):
                result, _ = invoke.invoke_ability(
                    env,
                    "rootsandfruit/blocks-mutate",
                    {
                        "post_id": args.post_id,
                        "op": "replace-block",
                        "ref": ref,
                        "block": {
                            "name": name,
                            "attributes": block.get("attributes") or {},
                            "innerHTML": inner,
                        },
                    },
                )
            else:
                result, _ = invoke.invoke_ability(
                    env,
                    "rootsandfruit/blocks-update",
                    {
                        "post_id": args.post_id,
                        "flat_index": index,
                        "innerHTML": inner,
                        **(
                            {"attributes": block["attributes"]}
                            if block.get("attributes") and name not in ("core/list", "core/table")
                            else {}
                        ),
                    },
                )
            if not result.get("success"):
                raise RuntimeError(json.dumps(result, ensure_ascii=False))
            print(f"OK {index} {name}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {index} {name}: {exc}", file=sys.stderr)
        time.sleep(args.delay_ms / 1000)

    if failed:
        raise SystemExit(f"{failed} block(s) failed")
    print(f"Repaired {len(blocks)} blocks on post {args.post_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
