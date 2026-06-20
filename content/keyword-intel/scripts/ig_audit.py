#!/usr/bin/env python3
"""Score a draft against brief + SERP baseline corpus for IG audit JSON output."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from serp_corpus import (  # noqa: E402
    CorpusPaths,
    analyze_draft_vs_corpus,
    build_ig_why_summary,
    load_corpus_text,
    parse_baseline_delta,
    score_baseline_coverage,
    score_intent_fit,
    score_serp_novelty_corpus,
    strip_draft_meta,
)

CATEGORIES = [
    "Delta Fidelity",
    "Artifact Realization",
    "Baseline Coverage",
    "SERP Novelty",
    "Intent Fit",
    "Risk Honesty",
]

LEGACY_CATEGORY_MAP = {
    "Evidence Traceability": "Baseline Coverage",
    "Decision Utility": "Intent Fit",
}


class BriefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.delta_titles: list[str] = []
        self.delta_artifacts: list[str] = []
        self.proof_claims: list[str] = []
        self._in_delta_card = False
        self._in_h3 = False
        self._in_dt = False
        self._in_dd = False
        self._current_dt = ""
        self._buf = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get("class", "") or ""
        if tag == "article" and "delta-card" in classes:
            self._in_delta_card = True
        if self._in_delta_card and tag == "h3":
            self._in_h3 = True
            self._buf = ""
        if self._in_delta_card and tag == "dt":
            self._in_dt = True
            self._buf = ""
        if self._in_delta_card and tag == "dd":
            self._in_dd = True
            self._buf = ""
        if tag == "ol" and "structure-list" in classes:
            pass

    def handle_endtag(self, tag: str) -> None:
        if tag == "h3" and self._in_h3:
            title = self._buf.strip()
            if title:
                self.delta_titles.append(title)
            self._in_h3 = False
        if tag == "dt" and self._in_dt:
            self._current_dt = self._buf.strip()
            self._in_dt = False
        if tag == "dd" and self._in_dd:
            text = self._buf.strip()
            if self._current_dt.lower().startswith("required artifact"):
                self.delta_artifacts.append(text)
            elif self._current_dt.lower().startswith("proof claim"):
                self.proof_claims.append(text)
            self._in_dd = False
        if tag == "article" and self._in_delta_card:
            self._in_delta_card = False

    def handle_data(self, data: str) -> None:
        if self._in_h3 or self._in_dt or self._in_dd:
            self._buf += data


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def keyword_hits(needles: list[str], haystack: str) -> int:
    if not needles:
        return 0
    hits = 0
    for needle in needles:
        words = [w for w in re.split(r"\W+", normalize(needle)) if len(w) > 3]
        if not words:
            continue
        if sum(1 for w in words if w in haystack) >= max(1, len(words) // 2):
            hits += 1
    return hits


def score_delta_fidelity(brief: BriefParser, draft: str) -> tuple[int, str]:
    if not brief.delta_titles:
        return 1, "Brief has no delta cards; scored partial by default."
    hits = keyword_hits(brief.delta_titles, draft)
    ratio = hits / len(brief.delta_titles)
    if ratio >= 0.8:
        return 2, f"Draft reflects {hits}/{len(brief.delta_titles)} delta titles."
    if ratio >= 0.4:
        return 1, f"Draft partially reflects {hits}/{len(brief.delta_titles)} delta titles."
    return 0, f"Draft missing most delta titles ({hits}/{len(brief.delta_titles)})."


def score_artifact_realization(brief: BriefParser, draft: str) -> tuple[int, str]:
    if not brief.delta_artifacts:
        return 1, "No required artifacts listed in brief."
    hits = keyword_hits(brief.delta_artifacts, draft)
    ratio = hits / len(brief.delta_artifacts)
    if ratio >= 0.7:
        return 2, f"Required artifacts represented ({hits}/{len(brief.delta_artifacts)})."
    if ratio >= 0.35:
        return 1, f"Some artifacts weak or missing ({hits}/{len(brief.delta_artifacts)})."
    return 0, f"Required artifacts largely absent ({hits}/{len(brief.delta_artifacts)})."


def score_risk_honesty(draft: str) -> tuple[int, str]:
    risk_words = ["limit", "caveat", "draft", "before publish", "not", "avoid", "manual", "stop"]
    hits = sum(1 for w in risk_words if w in draft)
    if hits >= 4:
        return 2, "Limits and caveats appear stated."
    if hits >= 2:
        return 1, "Partial caveat coverage."
    return 0, "Add plain limits (draft-only, preview gate, etc.)."


def recommendation(total: int) -> tuple[str, str]:
    if total >= 10:
        return "publish-ready", "Draft meets publish threshold."
    if total >= 8:
        return "revise-once", "One revision pass recommended before preview publish."
    if total >= 6:
        return "revise-first", "Major gaps; revise draft using serp_delta fixes."
    return "no-publish", "Draft not ready; rework against brief and SERP corpus."


def load_primary_intent(artifact_root: Path | None) -> str:
    if artifact_root is None:
        return "informational"
    top_n = artifact_root / "scored" / "top_n.json"
    if top_n.is_file():
        data = json.loads(top_n.read_text(encoding="utf-8"))
        return (data.get("primary_metrics") or {}).get("main_intent", "informational")
    return "informational"


def build_output(
    brief_path: Path,
    draft_path: Path,
    artifact_root: Path | None,
    brief: BriefParser,
    draft_text: str,
) -> dict:
    draft_norm = normalize(strip_html(draft_text) if draft_path.suffix == ".html" else draft_text)

    corpus_paths = CorpusPaths.from_artifact_root(artifact_root) if artifact_root else None
    corpus_text, _ = load_corpus_text(corpus_paths) if corpus_paths else ("", None)

    baseline_bullets: list[str] = []
    delta_bullets: list[str] = []
    if artifact_root:
        baseline_bullets, delta_bullets = parse_baseline_delta(artifact_root / "reports" / "baseline-delta.md")

    primary_intent = load_primary_intent(artifact_root)
    serp_analysis = analyze_draft_vs_corpus(
        draft_text,
        corpus_text,
        baseline_bullets=baseline_bullets,
        delta_bullets=delta_bullets or brief.proof_claims,
        primary_intent=primary_intent,
        brief_proof_claims=brief.proof_claims,
    )

    if corpus_paths and corpus_paths.serp_dir.is_dir():
        serp_delta_path = brief_path.parent / "serp_delta.json"
        serp_delta_path.write_text(json.dumps(serp_analysis.to_dict(), indent=2) + "\n", encoding="utf-8")

    if corpus_text and corpus_paths:
        scorers = [
            score_delta_fidelity(brief, draft_norm),
            score_artifact_realization(brief, draft_norm),
            score_baseline_coverage(serp_analysis, baseline_bullets, draft_norm),
            score_serp_novelty_corpus(serp_analysis),
            score_intent_fit(serp_analysis),
            score_risk_honesty(draft_norm),
        ]
        scoring_mode = "brief-draft+serp-corpus"
        compared = f"SERP corpus ({corpus_paths.manifest.name if corpus_paths.manifest.is_file() else 'corpus.md'}) + brief deltas"
    else:
        scorers = [
            score_delta_fidelity(brief, draft_norm),
            score_artifact_realization(brief, draft_norm),
            (0, "No SERP corpus — run build_serp_corpus.py first."),
            (0, "No SERP corpus — cannot score novelty vs page-one."),
            (1, "Intent fit not scored without keyword-intel metrics."),
            score_risk_honesty(draft_norm),
        ]
        scoring_mode = "brief-draft-only-degraded"
        compared = "Brief only (SERP corpus missing)"

    scores = {cat: s[0] for cat, s in zip(CATEGORIES, scorers)}
    notes = {cat: s[1] for cat, s in zip(CATEGORIES, scorers)}
    total = sum(scores.values())
    rec, rec_plain = recommendation(total)

    blockers: list[str] = []
    fix_first: list[str] = []
    for cat, val in scores.items():
        if val == 0:
            blockers.append(f"{cat}: {notes[cat]}")
        elif val == 1:
            fix_first.append(f"{cat}: {notes[cat]}")

    fix_first = serp_analysis.recommended_fixes[:3] + fix_first

    keep_these: list[str] = []
    for win in serp_analysis.delta_wins[:4]:
        keep_these.append(win["delta"][:120])

    page_one_summary = ""
    if corpus_paths and corpus_paths.ai_overview_md.is_file():
        page_one_summary = corpus_paths.ai_overview_md.read_text(encoding="utf-8")[:400]

    ig_why = build_ig_why_summary(
        serp_analysis,
        scores=scores,
        score_notes=notes,
        total=total,
        max_score=12,
        recommendation=rec,
        scoring_mode=scoring_mode,
        page_one_summary=page_one_summary,
    )

    return {
        "audit_mode": "draft-article",
        "scoring_mode": scoring_mode,
        "page_intent": brief_path.parent.name,
        "page_intent_note": f"Draft audit for {brief_path.parent.name}",
        "target_url": "",
        "date": date.today().isoformat(),
        "compared_against": compared,
        "recommendation": rec,
        "recommendation_plain": rec_plain,
        "total_score": total,
        "max_score": 12,
        "scores": scores,
        "score_notes": notes,
        "serp_delta_summary": {
            "novel_claim_count": len(serp_analysis.novel_claims),
            "delta_win_count": len(serp_analysis.delta_wins),
            "baseline_gap_count": len(serp_analysis.baseline_gaps),
            "recommended_fixes": serp_analysis.recommended_fixes,
        },
        "ig_why_summary": ig_why,
        "keep_these": keep_these,
        "fix_first": fix_first[:5],
        "blockers": blockers[:5],
        "next_steps": (blockers + fix_first)[:6]
        or (["Run /rf-article-publish in preview mode"] if rec == "publish-ready" else ["Proceed to information-gain-auditor HTML render"]),
        "rewrite_target_score": 10,
        "brief_path": str(brief_path),
        "draft_path": str(draft_path),
        "corpus_path": str(corpus_paths.corpus_md) if corpus_paths and corpus_paths.corpus_md.is_file() else "",
        "serp_delta_path": str(brief_path.parent / "serp_delta.json"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score draft against brief + SERP corpus.")
    parser.add_argument("--brief", required=True, type=Path)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--artifact-root", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if not args.brief.is_file():
        print(f"Error: brief not found: {args.brief}", file=sys.stderr)
        return 1
    if not args.draft.is_file():
        print(f"Error: draft not found: {args.draft}", file=sys.stderr)
        return 1

    brief_html = args.brief.read_text(encoding="utf-8")
    brief_parser = BriefParser()
    brief_parser.feed(brief_html)

    draft_text = args.draft.read_text(encoding="utf-8")
    artifact_root = args.artifact_root
    if artifact_root is None:
        slug = args.brief.parent.name
        candidate = args.brief.parents[2] / "keyword-intel" / "output" / slug
        if candidate.is_dir():
            artifact_root = candidate

    output = build_output(args.brief, args.draft, artifact_root, brief_parser, draft_text)
    out_path = args.output or (args.brief.parent / "ig-audit.json")
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {out_path}")
    print(f"Mode: {output['scoring_mode']}")
    print(f"Total: {output['total_score']}/{output['max_score']} — {output['recommendation']}")
    why = output.get("ig_why_summary") or {}
    if why.get("one_liner"):
        print(f"\nWhy: {why['one_liner']}")
    if output.get("serp_delta_summary", {}).get("recommended_fixes"):
        print("Top fixes:")
        for fix in output["serp_delta_summary"]["recommended_fixes"][:3]:
            print(f"  - {fix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
