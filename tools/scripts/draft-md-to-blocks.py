#!/usr/bin/env python3
"""Convert article draft.md (publish body) to Gutenberg blocks JSON for blocks-create-page."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

DEFAULTS_PATH = Path(__file__).resolve().parents[2] / "content" / "block-defaults.json"


def load_block_defaults() -> dict:
    if DEFAULTS_PATH.is_file():
        return json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))
    return {
        "code": {
            "block_name": "core/code",
            "language_map": {"powershell": "powershell", "": "plaintext"},
        },
        "table": {"className": "is-style-stripes", "figure_class": "wp-block-table is-style-stripes"},
    }


BLOCK_DEFAULTS = load_block_defaults()
CODE = BLOCK_DEFAULTS["code"]
TABLE_DEFAULTS = BLOCK_DEFAULTS["table"]


# Typography → HTML entities in innerHTML (survives encoding layers; avoids mojibake on Windows).
TYPOGRAPHY_ENTITIES: tuple[tuple[str, str], ...] = (
    ("\u2014", "&mdash;"),  # em dash
    ("\u2013", "&ndash;"),  # en dash
    ("\u2018", "&#8216;"),  # left single quote
    ("\u2019", "&#8217;"),  # right single quote / apostrophe
    ("\u201c", "&ldquo;"),  # left double quote
    ("\u201d", "&rdquo;"),  # right double quote
    ("\u2026", "&hellip;"),  # ellipsis
)


def entities_in_html(html: str) -> str:
    for char, entity in TYPOGRAPHY_ENTITIES:
        html = html.replace(char, entity)
    return html


def md_inline(text: str) -> str:
    """Minimal inline markdown → HTML for paragraph/list content."""
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Italic: single * only when not part of rootsandfruit/*-style paths
    text = re.sub(r"(?<![/\w])\*([^*]+)\*(?![/\w])", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    return entities_in_html(text)


def plain_from_markdown(text: str) -> str:
    """Strip markdown to plain text for block attributes.content."""
    plain = text
    plain = re.sub(r"\*\*([^*]+)\*\*", r"\1", plain)
    plain = re.sub(r"(?<![/\w])\*([^*]+)\*(?![/\w])", r"\1", plain)
    plain = re.sub(r"`([^`]+)`", r"\1", plain)
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
    return plain


def typography_plain(text: str) -> str:
    """ASCII-safe plain text for attributes (avoids mojibake in block JSON attrs)."""
    for char, entity in TYPOGRAPHY_ENTITIES:
        if entity.startswith("&") and entity.endswith(";"):
            ascii_map = {
                "&mdash;": "-",
                "&ndash;": "-",
                "&ldquo;": '"',
                "&rdquo;": '"',
                "&#8216;": "'",
                "&#8217;": "'",
                "&hellip;": "...",
            }
            text = text.replace(char, ascii_map.get(entity, char))
        else:
            text = text.replace(char, entity)
    return text


def heading_block(content: str, level: int) -> dict:
    tag = f"h{level}"
    plain_text = typography_plain(plain_from_markdown(content))
    inner = md_inline(content)
    return {
        "name": "core/heading",
        "attributes": {"content": plain_text, "level": level},
        "innerHTML": f'<{tag} class="wp-block-heading">{inner}</{tag}>',
    }


def paragraph_block(text: str) -> dict:
    inner = md_inline(text.strip())
    plain = typography_plain(re.sub(r"<[^>]+>", "", inner))
    return {
        "name": "core/paragraph",
        "attributes": {"content": plain},
        "innerHTML": f"<p>{inner}</p>",
    }


def list_block(items: list[str], ordered: bool) -> dict:
    tag = "ol" if ordered else "ul"
    lis = "".join(f"<li>{md_inline(item)}</li>" for item in items)
    values = [typography_plain(re.sub(r"<[^>]+>", "", md_inline(i))) for i in items]
    return {
        "name": "core/list",
        "attributes": {"ordered": ordered, "values": values},
        "innerHTML": f'<{tag} class="wp-block-list">{lis}</{tag}>',
    }


PLAINTEXT_LANGS = frozenset({"", "plaintext", "text", "plain", "txt", "none"})


def code_block(code: str, lang: str = "") -> dict:
    """core/code — static block; matches WP 6.9 save() for Gutenberg validation."""
    lang_key = lang.lower().strip()
    mapped = CODE.get("language_map", {}).get(lang_key, lang_key)
    language = (mapped or "").strip()
    escaped = html.escape(code, quote=False)
    attrs: dict = {"content": code}
    if language.lower() not in PLAINTEXT_LANGS:
        lang_slug = re.sub(r"[^a-z0-9-]", "-", language.lower())
        inner = (
            f'<pre class="wp-block-code"><code class="language-{lang_slug}">'
            f"{escaped}</code></pre>"
        )
        attrs["language"] = language
    else:
        # Plain / unlabeled fences: no language attr, no language-* class (avoids invalid block).
        inner = f'<pre class="wp-block-code"><code>{escaped}</code></pre>'
    return {
        "name": CODE.get("block_name", "core/code"),
        "attributes": attrs,
        "innerHTML": inner,
    }


def table_cell_plain(text: str) -> str:
    """Plain cell text for core/table — attributes and innerHTML must match (no md_inline)."""
    return html.escape(typography_plain(plain_from_markdown(text)))


def table_block(rows: list[list[str]]) -> dict:
    if not rows:
        return paragraph_block("")
    head, *body = rows
    head_plain = [typography_plain(plain_from_markdown(c)) for c in head]
    body_plain = [[typography_plain(plain_from_markdown(c)) for c in row] for row in body]
    thead = "<thead><tr>" + "".join(f"<th>{table_cell_plain(c)}</th>" for c in head) + "</tr></thead>"
    tbody_rows = ""
    for row in body:
        tbody_rows += "<tr>" + "".join(f"<td>{table_cell_plain(c)}</td>" for c in row) + "</tr>"
    tbody = f"<tbody>{tbody_rows}</tbody>"
    figure_class = TABLE_DEFAULTS.get("figure_class", "wp-block-table is-style-stripes")
    stripe_class = TABLE_DEFAULTS.get("className", "is-style-stripes")
    inner = f'<figure class="{figure_class}"><table class="has-fixed-layout">{thead}{tbody}</table></figure>'
    return {
        "name": "core/table",
        "attributes": {
            "hasFixedLayout": True,
            "className": stripe_class,
            "head": head_plain,
            "body": body_plain,
        },
        "innerHTML": inner,
    }


def parse_table(lines: list[str]) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    i = 0
    while i < len(lines) and lines[i].strip().startswith("|"):
        row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if not all(re.match(r"^[-:\s]+$", c) for c in row):
            rows.append(row)
        i += 1
    return rows, i


def parse_draft(text: str) -> tuple[str, list[dict]]:
    lines = text.splitlines()
    title = ""
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]

    # Stop at first --- after body content (skip QA sections)
    body_lines: list[str] = []
    for line in lines:
        if line.strip() == "---":
            break
        body_lines.append(line)

    blocks: list[dict] = []
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("## "):
            blocks.append(heading_block(stripped[3:], 2))
            i += 1
            continue

        if stripped.startswith("### "):
            blocks.append(heading_block(stripped[4:], 3))
            i += 1
            continue

        if stripped.startswith("|"):
            rows, consumed = parse_table(body_lines[i:])
            blocks.append(table_block(rows))
            i += consumed
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < len(body_lines) and not body_lines[i].strip().startswith("```"):
                code_lines.append(body_lines[i])
                i += 1
            blocks.append(code_block("\n".join(code_lines), lang))
            i += 1
            continue

        if re.match(r"^[-*]\s+", stripped):
            items: list[str] = []
            while i < len(body_lines):
                s = body_lines[i].strip()
                m = re.match(r"^[-*]\s+(.+)", s)
                if not m:
                    break
                items.append(m.group(1))
                i += 1
            blocks.append(list_block(items, ordered=False))
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(body_lines):
                s = body_lines[i].strip()
                m = re.match(r"^\d+\.\s+(.+)", s)
                if not m:
                    break
                items.append(m.group(1))
                i += 1
            blocks.append(list_block(items, ordered=True))
            continue

        # Paragraph: collect until blank or structural line
        para_lines = [stripped]
        i += 1
        while i < len(body_lines):
            s = body_lines[i].strip()
            if (
                not s
                or s.startswith("#")
                or s.startswith("|")
                or s.startswith("```")
                or re.match(r"^[-*]\s+", s)
                or re.match(r"^\d+\.\s+", s)
            ):
                break
            para_lines.append(s)
            i += 1
        blocks.append(paragraph_block(" ".join(para_lines)))

    return title, blocks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Path to draft.md")
    parser.add_argument("-o", "--output", type=Path, help="Write blocks JSON here")
    parser.add_argument("--slug", help="Post slug for blocks-create-page")
    parser.add_argument("--excerpt", help="Post excerpt")
    parser.add_argument("--stdout", action="store_true", help="Print full create-page payload")
    args = parser.parse_args()

    text = args.draft.read_text(encoding="utf-8")
    title, blocks = parse_draft(text)

    payload = {
        "title": title,
        "post_type": "post",
        "status": "draft",
        "blocks": blocks,
    }
    if args.slug:
        payload["slug"] = args.slug
    if args.excerpt:
        payload["excerpt"] = args.excerpt

    out = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(out + "\n", encoding="utf-8")
        print(f"Wrote {len(blocks)} blocks to {args.output}", file=sys.stderr)
    if args.stdout or not args.output:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
