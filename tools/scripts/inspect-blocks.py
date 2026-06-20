#!/usr/bin/env python3
"""Inspect blocks from blocks-get-page JSON dump."""
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
blocks = (data.get("data") or data).get("blocks") or []
for i, b in enumerate(blocks):
    name = b.get("name", "")
    if "code" in name or name == "core/table":
        attrs = b.get("attributes", {})
        inner = b.get("innerHTML", "")
        code = (attrs.get("code") or attrs.get("content") or "")[:60]
        preview = code.encode("ascii", "replace").decode("ascii")
        print(
            f"{i:3} {name:35} className={attrs.get('className')!r} "
            f"inner={len(inner)} codeHTML={len(attrs.get('codeHTML') or '')} "
            f"preview={preview!r}"
        )
