#!/usr/bin/env python3
"""Retry failed block indices from publish-blocks-payload output."""

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
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=Path)
    parser.add_argument("--post-id", type=int, required=True)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--delay-ms", type=int, default=800)
    args = parser.parse_args()

    invoke = load_invoke()
    env = invoke.load_dotenv(SCRIPT_DIR.parents[1] / ".env")
    blocks = json.loads(args.payload.read_text(encoding="utf-8"))["blocks"]
    failed = 0
    for index in args.indices:
        block = blocks[index]
        update = {
            "post_id": args.post_id,
            "flat_index": index,
            "innerHTML": block.get("innerHTML", ""),
        }
        name = block.get("name", "")
        if block.get("attributes") and name not in ("core/list", "core/table"):
            update["attributes"] = block["attributes"]
        try:
            result, _ = invoke.invoke_ability(env, "rootsandfruit/blocks-update", update)
            if not result.get("success"):
                raise RuntimeError(json.dumps(result, ensure_ascii=False))
            print(f"OK flat_index={index} {block.get('name')}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL flat_index={index}: {exc}", file=sys.stderr)
        time.sleep(args.delay_ms / 1000)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
