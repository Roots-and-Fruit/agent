#!/usr/bin/env python3
"""Build SERP baseline corpus from DataForSEO (SERP + On-Page content parsing)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from serp_corpus import (  # noqa: E402
    CorpusPaths,
    extract_ai_overview_markdown,
    extract_organic_urls,
    fetch_page_markdown,
    fetch_serp,
    slugify_url,
)


def load_keyword(artifact_root: Path, override: str | None) -> str:
    if override:
        return override.strip()
    manifest_path = artifact_root / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        kw = manifest.get("primary_keyword")
        if kw:
            return str(kw)
    raise SystemExit(f"No keyword: pass --keyword or create {manifest_path}")


def build_corpus(artifact_root: Path, keyword: str, *, depth: int = 10, skip_fetch: bool = False) -> dict:
    paths = CorpusPaths.from_artifact_root(artifact_root)
    paths.serp_dir.mkdir(parents=True, exist_ok=True)
    paths.pages_dir.mkdir(parents=True, exist_ok=True)

    if skip_fetch and paths.serp_raw.is_file() and paths.corpus_md.is_file():
        return json.loads(paths.manifest.read_text(encoding="utf-8"))

    print(f"Fetching SERP for: {keyword}")
    serp_raw = fetch_serp(keyword, depth=depth)
    paths.serp_raw.write_text(json.dumps(serp_raw, indent=2) + "\n", encoding="utf-8")

    organic = extract_organic_urls(serp_raw, limit=depth)
    ai_md = extract_ai_overview_markdown(serp_raw)
    if ai_md:
        paths.ai_overview_md.write_text(ai_md + "\n", encoding="utf-8")

    page_records: list[dict] = []
    corpus_parts: list[str] = [
        f"# SERP Baseline Corpus — {keyword}",
        f"Generated: {date.today().isoformat()}",
        "",
    ]

    if ai_md:
        corpus_parts.extend([
            "## Google AI Overview",
            "",
            ai_md,
            "",
            "---",
            "",
        ])

    for i, row in enumerate(organic, start=1):
        url = row["url"]
        title = row.get("title") or url
        print(f"  [{i}/{len(organic)}] {url}")
        md, status, parse_mode = fetch_page_markdown(url)
        slug = slugify_url(url, i)
        page_path = paths.pages_dir / f"{slug}.md"
        header = f"---\nurl: {url}\ntitle: {json.dumps(title)}\nstatus_code: {status}\nparse_mode: {parse_mode}\n---\n\n"
        page_path.write_text(header + md + "\n", encoding="utf-8")
        page_records.append({
            "rank": row.get("rank", i),
            "url": url,
            "title": title,
            "file": str(page_path.relative_to(artifact_root)).replace("\\", "/"),
            "status_code": status,
            "parse_mode": parse_mode,
            "char_count": len(md),
        })
        corpus_parts.extend([
            f"## Rank {row.get('rank', i)}: {title}",
            f"Source: {url}",
            "",
            md if md else "_[No extractable body text]_",
            "",
            "---",
            "",
        ])

    paths.corpus_md.write_text("\n".join(corpus_parts) + "\n", encoding="utf-8")

    manifest = {
        "keyword": keyword,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "location_code": 2840,
        "language_code": "en",
        "depth": depth,
        "organic_count": len(page_records),
        "ai_overview_chars": len(ai_md),
        "corpus_chars": paths.corpus_md.stat().st_size,
        "pages": page_records,
        "dataforseo_endpoints": [
            "serp/google/organic/live/advanced",
            "on_page/content_parsing/live",
        ],
    }
    paths.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SERP baseline corpus via DataForSEO.")
    parser.add_argument("--artifact-root", type=Path, required=True, help="keyword-intel/output/<slug>/")
    parser.add_argument("--keyword", type=str, default=None, help="Override primary keyword")
    parser.add_argument("--depth", type=int, default=10, help="Organic results to fetch (max 10)")
    parser.add_argument("--skip-fetch", action="store_true", help="Use existing corpus if present")
    args = parser.parse_args()

    if not args.artifact_root.is_dir():
        print(f"Error: artifact root not found: {args.artifact_root}", file=sys.stderr)
        return 1

    keyword = load_keyword(args.artifact_root, args.keyword)
    manifest = build_corpus(args.artifact_root, keyword, depth=min(args.depth, 10), skip_fetch=args.skip_fetch)
    print(f"Wrote corpus: {args.artifact_root / 'serp' / 'corpus.md'}")
    print(f"Pages: {manifest['organic_count']} | AI Overview chars: {manifest['ai_overview_chars']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
