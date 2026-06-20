"""SERP corpus build + deterministic draft-vs-corpus analysis."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from dataforseo_client import post

STOPWORDS = {
    "about", "after", "also", "been", "before", "being", "both", "from",
    "have", "here", "into", "just", "like", "more", "most", "only", "other",
    "over", "same", "some", "such", "than", "that", "their", "them", "then",
    "there", "these", "they", "this", "through", "very", "what", "when",
    "where", "which", "while", "with", "would", "your", "wordpress", "https",
    "http", "www", "com", "github", "plugin", "plugins",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def slugify_url(url: str, rank: int) -> str:
    host = urlparse(url).netloc.replace("www.", "")
    host = re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-") or "page"
    return f"{rank:02d}-{host}"


def extract_organic_urls(serp_raw: dict, limit: int = 10) -> list[dict]:
    items = ((serp_raw.get("tasks") or [{}])[0].get("result") or [{}])[0].get("items") or []
    out: list[dict] = []
    for item in items:
        if item.get("type") != "organic":
            continue
        out.append({
            "rank": item.get("rank_absolute") or len(out) + 1,
            "url": item.get("url") or "",
            "title": item.get("title") or "",
            "description": item.get("description") or "",
        })
        if len(out) >= limit:
            break
    return out


def extract_ai_overview_markdown(serp_raw: dict) -> str:
    items = ((serp_raw.get("tasks") or [{}])[0].get("result") or [{}])[0].get("items") or []
    for item in items:
        if item.get("type") == "ai_overview":
            return (item.get("markdown") or item.get("text") or "").strip()
    return ""


def fetch_serp(keyword: str, *, depth: int = 10) -> dict:
    payload = [{
        "keyword": keyword,
        "location_code": 2840,
        "language_code": "en",
        "depth": depth,
        "load_async_ai_overview": True,
    }]
    return post("serp/google/organic/live/advanced", payload, timeout=180)


def fetch_page_markdown(url: str) -> tuple[str, int, str]:
    data = post("on_page/content_parsing/live", [{"url": url, "markdown_view": True}], timeout=120)
    item = ((data.get("tasks") or [{}])[0].get("result") or [{}])[0].get("items") or [{}]
    item = item[0] if item else {}
    status = int(item.get("status_code") or 0)
    md = (item.get("page_as_markdown") or "").strip()
    if md:
        return md, status, "ok"
    # Fallback: flatten structured page_content
    flat = flatten_page_content(item.get("page_content") or {})
    return flat, status, "flattened" if flat else "empty"


def flatten_page_content(node: object) -> str:
    parts: list[str] = []

    def walk(obj: object) -> None:
        if isinstance(obj, dict):
            if isinstance(obj.get("text"), str):
                parts.append(obj["text"])
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(node)
    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def tokenize(text: str) -> list[str]:
    return [
        w for w in re.findall(r"[a-z0-9]+", normalize(text))
        if len(w) > 3 and w not in STOPWORDS
    ]


def keyword_hits(needles: list[str], haystack: str) -> int:
    if not needles:
        return 0
    hits = 0
    for needle in needles:
        words = tokenize(needle)
        if not words:
            continue
        if sum(1 for w in words if w in haystack) >= max(1, len(words) // 2):
            hits += 1
    return hits


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [c.strip() for c in chunks if len(c.strip()) > 40]


def strip_draft_meta(draft: str) -> str:
    cut = draft.find("\n---\n")
    return draft[:cut] if cut != -1 else draft


RF_DELTA_MARKERS = [
    "rootsandfruit/",
    "set-post-author",
    "blocks-create-page",
    "enable-public-preview",
    "audit-mcp-abilities",
    "wordpress-rootsandfruit",
    "innerhtml",
    "no delete",
    "cache purge",
    "gk block mcp",
    "one mcp server",
    "public preview",
    "breeze cache",
    "test-wordpress-mcp-http",
]


def marker_delta_wins(draft: str, corpus: str) -> list[dict]:
    wins: list[dict] = []
    for marker in RF_DELTA_MARKERS:
        if marker in draft and marker not in corpus:
            wins.append({
                "delta": marker,
                "note": "Operator-specific marker in draft, absent from SERP corpus.",
            })
    return wins


def parse_baseline_delta(path: Path) -> tuple[list[str], list[str]]:
    if not path.is_file():
        return [], []
    text = path.read_text(encoding="utf-8")
    baseline: list[str] = []
    deltas: list[str] = []
    section = ""
    for line in text.splitlines():
        if line.startswith("## Baseline"):
            section = "baseline"
            continue
        if line.startswith("## Delta"):
            section = "delta"
            continue
        if line.startswith("## "):
            section = ""
            continue
        if line.startswith("- ") and section == "baseline":
            baseline.append(line[2:].strip())
        elif line.startswith("- ") and section == "delta":
            deltas.append(line[2:].strip())
        elif re.match(r"^\d+\.\s", line) and section == "delta":
            deltas.append(re.sub(r"^\d+\.\s*", "", line).strip())
    return baseline, deltas


@dataclass
class CorpusPaths:
    root: Path
    serp_dir: Path
    serp_raw: Path
    corpus_md: Path
    ai_overview_md: Path
    manifest: Path
    pages_dir: Path

    @classmethod
    def from_artifact_root(cls, artifact_root: Path) -> CorpusPaths:
        serp_dir = artifact_root / "serp"
        return cls(
            root=artifact_root,
            serp_dir=serp_dir,
            serp_raw=serp_dir / "serp_raw.json",
            corpus_md=serp_dir / "corpus.md",
            ai_overview_md=serp_dir / "ai_overview.md",
            manifest=serp_dir / "corpus_manifest.json",
            pages_dir=serp_dir / "pages",
        )


@dataclass
class SerpDeltaAnalysis:
    corpus_token_count: int = 0
    novel_claims: list[str] = field(default_factory=list)
    delta_wins: list[dict] = field(default_factory=list)
    baseline_gaps: list[dict] = field(default_factory=list)
    intent_signals: dict = field(default_factory=dict)
    recommended_fixes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "corpus_token_count": self.corpus_token_count,
            "novel_claims": self.novel_claims[:12],
            "delta_wins": self.delta_wins,
            "baseline_gaps": self.baseline_gaps,
            "intent_signals": self.intent_signals,
            "recommended_fixes": self.recommended_fixes,
        }


def load_corpus_text(paths: CorpusPaths) -> tuple[str, dict | None]:
    if not paths.corpus_md.is_file():
        return "", None
    corpus = paths.corpus_md.read_text(encoding="utf-8")
    manifest = None
    if paths.manifest.is_file():
        manifest = json.loads(paths.manifest.read_text(encoding="utf-8"))
    return corpus, manifest


def analyze_draft_vs_corpus(
    draft_text: str,
    corpus_text: str,
    *,
    baseline_bullets: list[str],
    delta_bullets: list[str],
    primary_intent: str = "informational",
    brief_proof_claims: list[str] | None = None,
) -> SerpDeltaAnalysis:
    draft = normalize(strip_draft_meta(draft_text))
    corpus = normalize(corpus_text)
    corpus_tokens = set(tokenize(corpus))
    draft_tokens = set(tokenize(draft))

    analysis = SerpDeltaAnalysis(corpus_token_count=len(corpus_tokens))

    for sentence in split_sentences(strip_draft_meta(draft_text)):
        words = tokenize(sentence)
        if len(words) < 6:
            continue
        novel_ratio = sum(1 for w in words if w not in corpus_tokens) / len(words)
        if novel_ratio >= 0.52:
            analysis.novel_claims.append(sentence.strip())

    for i, delta in enumerate(delta_bullets):
        in_draft = keyword_hits([delta], draft) > 0
        in_corpus = keyword_hits([delta], corpus) > 0
        if in_draft and not in_corpus:
            analysis.delta_wins.append({
                "delta": delta,
                "note": "Present in draft, weak or absent in SERP corpus.",
            })

    for win in marker_delta_wins(draft, corpus):
        if not any(w["delta"] == win["delta"] for w in analysis.delta_wins):
            analysis.delta_wins.append(win)

    for bullet in baseline_bullets:
        in_corpus = keyword_hits([bullet], corpus) > 0
        in_draft = keyword_hits([bullet], draft) > 0
        if in_corpus and not in_draft:
            analysis.baseline_gaps.append({
                "topic": bullet,
                "note": "Page-one covers this; draft should address or explicitly defer.",
            })

    nav_signals = [
        "mcp.json", "application password", "install", "configure", "connect cursor",
        "settings", "setup", "wire", "plugin install",
    ]
    info_signals = [
        "architecture", "workflow", "checklist", "abilities", "adapter", "preview",
        "draft", "blocks", "guardrail", "permission",
    ]
    nav_hits = sum(1 for s in nav_signals if s in draft)
    info_hits = sum(1 for s in info_signals if s in draft)
    analysis.intent_signals = {
        "primary_intent": primary_intent,
        "navigational_hits": nav_hits,
        "informational_hits": info_hits,
    }

    if primary_intent == "navigational" and nav_hits < 2:
        analysis.recommended_fixes.append(
            "Primary intent is navigational: add a short Cursor wiring subsection (mcp.json + Application Password)."
        )
    if analysis.baseline_gaps:
        top = analysis.baseline_gaps[0]["topic"]
        analysis.recommended_fixes.append(
            f"Baseline gap: page-one covers “{top[:80]}…” — cover in body or one deferral sentence with link."
        )
    if brief_proof_claims:
        weak = [c for c in brief_proof_claims if keyword_hits([c], draft) and not keyword_hits([c], corpus)]
        if not weak and not analysis.delta_wins and len(analysis.novel_claims) < 6:
            analysis.recommended_fixes.append(
                "Differentiation vs SERP corpus is thin — strengthen proof claims that competitors do not make."
            )

    unique_tokens = draft_tokens - corpus_tokens
    if len(unique_tokens) < 80:
        analysis.recommended_fixes.append(
            "Low lexical delta vs SERP corpus — add operator-specific examples only you can show."
        )

    return analysis


def score_baseline_coverage(analysis: SerpDeltaAnalysis, baseline_bullets: list[str], draft: str) -> tuple[int, str]:
    if not baseline_bullets:
        return 1, "No baseline bullets in keyword-intel report."
    gaps = len(analysis.baseline_gaps)
    if gaps == 0:
        return 2, "Draft covers baseline topics present in SERP corpus."
    if gaps <= max(1, len(baseline_bullets) // 3):
        return 1, f"{gaps} baseline topic(s) on page-one missing from draft."
    return 0, f"{gaps} table-stakes topics in SERP corpus not addressed in draft."


def score_serp_novelty_corpus(analysis: SerpDeltaAnalysis) -> tuple[int, str]:
    wins = len(analysis.delta_wins)
    novel = len(analysis.novel_claims)
    if wins >= 2 and novel >= 4:
        return 2, f"{wins} delta win(s) vs corpus; {novel} high-novelty sentences."
    if wins >= 1 or novel >= 2:
        return 1, f"Some differentiation ({wins} delta wins, {novel} novel sentences); strengthen further."
    return 0, "Draft largely overlaps SERP corpus without clear delta wins."


def score_intent_fit(analysis: SerpDeltaAnalysis) -> tuple[int, str]:
    intent = analysis.intent_signals.get("primary_intent", "informational")
    nav = analysis.intent_signals.get("navigational_hits", 0)
    info = analysis.intent_signals.get("informational_hits", 0)
    if intent == "navigational":
        if nav >= 2:
            return 2, f"Navigational intent served ({nav} wiring/install signals)."
        if nav >= 1 or info >= 4:
            return 1, "Partial navigational fit — add install/wiring steps for search intent."
        return 0, "Navigational keyword but draft lacks setup/wiring path."
    if info >= 4:
        return 2, "Informational intent served with explainer depth."
    if info >= 2:
        return 1, "Some explainer depth; add more how/why for intent."
    return 0, "Weak fit for informational intent."


def score_evidence_traceability(paths: CorpusPaths, analysis: SerpDeltaAnalysis) -> tuple[int, str]:
    if not paths.corpus_md.is_file():
        return 0, "No SERP corpus — run build_serp_corpus.py before IG audit."
    if paths.manifest.is_file() and analysis.corpus_token_count > 500:
        return 2, f"SERP corpus on disk ({analysis.corpus_token_count} tokens); scores corpus-backed."
    return 1, "Corpus present but thin — refresh SERP capture."


WIN_THEMES: list[tuple[str, str, list[str]]] = [
    (
        "Curated least-privilege abilities",
        "Page-one promotes broad MCP/REST exposure and plugin roundups; the draft documents a bounded rootsandfruit/* surface, permission basis, and explicit omissions (no delete, no cache purge).",
        ["rootsandfruit/", "no delete", "cache purge", "permission"],
    ),
    (
        "Guarded publish path",
        "Competitors stop at connect-and-edit; the draft adds a preview-gated checklist with set-post-author, Breeze purge, and enable-public-preview before publish-post.",
        ["set-post-author", "enable-public-preview", "public preview", "publish-post", "breeze"],
    ),
    (
        "Block-first body rules",
        "Generic results say create/update posts; the draft separates blocks-* for body vs update-post for title/excerpt and documents the innerHTML failure mode.",
        ["innerhtml", "blocks-", "update-post"],
    ),
    (
        "Single MCP architecture",
        "Listicles offer many servers; the draft commits to one Cursor MCP, in-process blocks, and explicit routing rules.",
        ["one mcp", "wordpress-rootsandfruit", "gk block"],
    ),
    (
        "Live operator evidence",
        "Vendor docs and AI summaries lack verifiable solo-operator detail; the draft names smoke scripts, plugin versions, and a real self-hosted stack.",
        ["audit-mcp", "test-wordpress", "ping", "cloudways", "proof"],
    ),
]


def _marker_hits(markers: list[str], haystack: str) -> bool:
    h = normalize(haystack)
    return any(m in h for m in markers)


def build_ig_why_summary(
    analysis: SerpDeltaAnalysis,
    *,
    scores: dict[str, int],
    score_notes: dict[str, str],
    total: int,
    max_score: int,
    recommendation: str,
    scoring_mode: str,
    page_one_summary: str = "",
) -> dict:
    """Plain-language WHY block for ig-audit.json and HTML render."""
    delta_markers = [w["delta"] for w in analysis.delta_wins]
    joined_deltas = " ".join(delta_markers)

    wins_vs_serp: list[dict[str, str]] = []
    for title, body, markers in WIN_THEMES:
        if _marker_hits(markers, joined_deltas) or _marker_hits(markers, " ".join(analysis.novel_claims)):
            wins_vs_serp.append({"title": title, "body": body})

    score_rationale = [
        f"{cat}: {score_notes[cat]}"
        for cat, val in scores.items()
        if val >= 1
    ]

    page_one_contrast = (
        page_one_summary.strip()
        or "Page-one and AI Overview mostly answer how to connect WordPress MCP (plugins, Application Passwords, broad CRUD)."
    )

    one_liner = (
        "This draft wins on information gain because it is not a connect-in-five-minutes tutorial — "
        "it documents a least-privilege, block-aware, preview-gated publish pipeline on a real self-hosted site, "
        "with named abilities, explicit omissions, and verification steps page-one does not assemble."
    )

    caveats: list[str] = []
    if scoring_mode != "brief-draft+serp-corpus":
        caveats.append("SERP corpus missing — scores are degraded; run build_serp_corpus.py.")
    if analysis.baseline_gaps:
        caveats.append(f"{len(analysis.baseline_gaps)} baseline topic(s) on page-one need coverage or explicit deferral.")
    if not caveats:
        caveats.append(
            "Score is corpus-backed and deterministic — not LLM/embeddings. Optional: mcp.json example for copy-paste navigational intent."
        )

    return {
        "one_liner": one_liner,
        "headline": f"{total}/{max_score} — {recommendation.replace('-', ' ')}",
        "score_rationale": score_rationale,
        "wins_vs_serp": wins_vs_serp,
        "page_one_contrast": page_one_contrast,
        "notable_novel_claims": [c[:220] for c in analysis.novel_claims[:5]],
        "delta_win_count": len(analysis.delta_wins),
        "caveats": caveats,
    }
