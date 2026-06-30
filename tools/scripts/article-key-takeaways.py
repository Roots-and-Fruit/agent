#!/usr/bin/env python3
"""Load and validate article key takeaways (LCF _rf_key_takeaways repeater)."""

from __future__ import annotations

import re
from pathlib import Path

TAKEAWAY_MIN_ITEMS = 1
TAKEAWAY_MAX_ITEMS = 12
TAKEAWAY_TARGET_MIN_CHARS = 40
TAKEAWAY_TARGET_MAX_CHARS = 220
TAKEAWAY_HARD_MAX_CHARS = 280


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def load_takeaways_text(raw: str) -> list[str]:
    items: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        stripped = re.sub(r"^[-*]\s+", "", stripped)
        stripped = re.sub(r"^\d+\.\s+", "", stripped)
        text = normalize_text(stripped)
        if text:
            items.append(text)
    return items


def validate_takeaways(
    items: list[str],
    draft_path: Path | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if len(items) < TAKEAWAY_MIN_ITEMS:
        errors.append(f"at least {TAKEAWAY_MIN_ITEMS} takeaway required")
        return errors, warnings

    if len(items) > TAKEAWAY_MAX_ITEMS:
        errors.append(f"maximum {TAKEAWAY_MAX_ITEMS} takeaways allowed")

    for index, item in enumerate(items, start=1):
        length = len(item)
        if length < 20:
            errors.append(f"takeaway {index} too short ({length} chars)")
        elif length < TAKEAWAY_TARGET_MIN_CHARS:
            warnings.append(
                f"takeaway {index} short ({length} chars; target {TAKEAWAY_TARGET_MIN_CHARS}+)"
            )
        if length > TAKEAWAY_HARD_MAX_CHARS:
            errors.append(
                f"takeaway {index} too long ({length} chars; max {TAKEAWAY_HARD_MAX_CHARS})"
            )
        elif length > TAKEAWAY_TARGET_MAX_CHARS:
            warnings.append(
                f"takeaway {index} long ({length} chars; target under {TAKEAWAY_TARGET_MAX_CHARS})"
            )

    if draft_path and draft_path.is_file():
        body = draft_path.read_text(encoding="utf-8").lower()
        for index, item in enumerate(items, start=1):
            if len(item) >= 50 and item.lower() in body:
                warnings.append(f"takeaway {index} may duplicate draft body text")

    return errors, warnings


def resolve_takeaways(
    article_dir: Path,
    cli_items: list[str] | None = None,
    *,
    allow_missing: bool = False,
) -> list[str]:
    if cli_items:
        return load_takeaways_text("\n".join(cli_items))
    path = article_dir / "key-takeaways.txt"
    if path.is_file():
        return load_takeaways_text(path.read_text(encoding="utf-8"))
    if allow_missing:
        return []
    raise SystemExit(
        f"Missing {path}. One takeaway per line (1–{TAKEAWAY_MAX_ITEMS} items). "
        "Finalize at /voiceprint-audit; see content/README.md."
    )
