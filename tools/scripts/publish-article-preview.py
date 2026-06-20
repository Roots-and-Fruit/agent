#!/usr/bin/env python3
"""One-shot article preview publish: draft.md -> blocks -> WordPress draft + preview."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AGENT_ROOT = SCRIPT_DIR.parents[1]


def load_invoke():
    spec = importlib.util.spec_from_file_location("inv", SCRIPT_DIR / "invoke-mcp-ability.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def verify_blocks(blocks: list[dict]) -> None:
    code_blocks = 0
    cbp = 0
    tables = 0
    for b in blocks:
        name = b.get("name", "")
        if name == "core/code":
            code_blocks += 1
            attrs = b.get("attributes") or {}
            inner = b.get("innerHTML") or ""
            if not attrs.get("content") or not inner.startswith("<pre"):
                raise SystemExit("core/code block missing content or innerHTML")
        elif name == "kevinbatdorf/code-block-pro":
            cbp += 1
        elif name == "core/table":
            tables += 1
            if (b.get("attributes") or {}).get("className") != "is-style-stripes":
                raise SystemExit("core/table missing is-style-stripes")
    if code_blocks == 0:
        raise SystemExit("No core/code blocks in payload")
    if cbp:
        raise SystemExit(f"Payload must not contain Code Block Pro ({cbp} found)")
    print(f"Verify OK: {len(blocks)} blocks, {code_blocks} core/code, {tables} table(s)")


def verify_raw_post(post_id: int, expected_code_blocks: int) -> None:
    raw_script = SCRIPT_DIR / "wp-rest-get-post-raw.py"
    raw_check = subprocess.run(
        [sys.executable, str(raw_script), str(post_id)],
        cwd=AGENT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if raw_check.returncode != 0:
        raise SystemExit(f"Raw content check failed: {raw_check.stderr}")
    for line in reversed((raw_check.stdout or "").splitlines()):
        line = line.strip()
        if line.startswith("{"):
            markers = json.loads(line)
            if markers.get("code-block-pro", 0) > 0 or markers.get("shiki", 0) > 0:
                raise SystemExit(f"Post {post_id} contains Code Block Pro markup: {markers}")
            if markers.get("wp-block-code", 0) < expected_code_blocks:
                raise SystemExit(
                    f"Post {post_id} expected {expected_code_blocks} core/code block(s): {markers}"
                )
            if markers.get("is-style-stripes", 0) < 1:
                raise SystemExit(f"Post {post_id} missing striped table markup")
            return
    raise SystemExit(f"Could not parse raw content markers for post {post_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article_dir", type=Path, help="content/articles/<slug>/")
    parser.add_argument("--author", type=int, default=1)
    parser.add_argument("--excerpt", default="")
    args = parser.parse_args()

    article_dir = args.article_dir.resolve()
    slug = article_dir.name
    draft = article_dir / "draft.md"
    payload_path = article_dir / "blocks-payload.json"
    preview_path = article_dir / "preview.json"

    if not draft.is_file():
        raise SystemExit(f"Missing {draft}")

    conv_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "draft-md-to-blocks.py"),
        str(draft),
        "-o",
        str(payload_path),
        "--slug",
        slug,
    ]
    if args.excerpt:
        conv_cmd.extend(["--excerpt", args.excerpt])
    run(conv_cmd, cwd=AGENT_ROOT)

    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    verify_blocks(payload.get("blocks") or [])

    inv = load_invoke()
    env = inv.load_dotenv(AGENT_ROOT / ".env")
    result, _ = inv.invoke_ability(env, "rootsandfruit/blocks-create-page", payload)
    if not result.get("success"):
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))

    data = result.get("data") or result
    post_id = int(data.get("post_id") or data.get("id") or 0)
    if post_id <= 0:
        raise SystemExit(f"No post_id in create-page response: {json.dumps(data)}")

    author_result, _ = inv.invoke_ability(
        env,
        "rootsandfruit/set-post-author",
        {"post_id": post_id, "author": args.author},
    )
    if not author_result.get("success"):
        print("WARN set-post-author:", json.dumps(author_result, ensure_ascii=False), file=sys.stderr)

    preview_result, _ = inv.invoke_ability(
        env,
        "rootsandfruit/enable-public-preview",
        {"post_id": post_id},
    )
    if not preview_result.get("success"):
        raise SystemExit(json.dumps(preview_result, ensure_ascii=False, indent=2))

    preview_data = preview_result.get("data") or preview_result
    preview_url = preview_data.get("preview_url") or preview_data.get("url") or ""

    expected_code = sum(1 for b in payload.get("blocks") or [] if b.get("name") == "core/code")
    verify_raw_post(post_id, expected_code)

    get_result, _ = inv.invoke_ability(
        env,
        "rootsandfruit/blocks-get-page",
        {"post_id": post_id, "render": False},
    )
    live_blocks = ((get_result.get("data") or get_result).get("blocks") or []) if get_result.get("success") else []
    code_live = sum(1 for b in live_blocks if b.get("name") == "core/code")
    table_striped = sum(
        1
        for b in live_blocks
        if b.get("name") == "core/table"
        and (b.get("attributes") or {}).get("className") == "is-style-stripes"
    )

    preview_doc = {
        "post_id": post_id,
        "slug": slug,
        "status": "draft",
        "author_id": args.author,
        "edit_url": f"https://rootsandfruit.com/wp-admin/post.php?post={post_id}&action=edit",
        "preview_url": preview_url,
        "blocks_count": len(live_blocks) or len(payload.get("blocks") or []),
        "code_blocks": code_live,
        "striped_tables": table_striped,
        "created": date.today().isoformat(),
        "convert_code_pro": (
            "Open edit_url, focus each core/code block, toolbar Convert to Code Pro, Save"
        ),
        "note": "core/code via MCP; convert to Code Block Pro in editor before publish approval",
    }
    preview_path.write_text(json.dumps(preview_doc, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(preview_doc, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
