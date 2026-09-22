#!/usr/bin/env python3
"""Classify instruction overlap/conflict candidates from inventory."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "reports" / "instruction_inventory.json"
JSON_REPORT = ROOT / "reports" / "overlap_analysis.json"
MD_REPORT = ROOT / "reports" / "overlap_analysis.md"

CATEGORIES = {
    "global-safety": ["approval", "approve", "승인", "destructive", "파괴", "delete", "삭제", "credential", "secret", "api key", "비공개", "외부 전송", "privacy", "개인정보"],
    "transport": ["telegram", "텔레그램", "attach", "thread", "channel"],
    "tool-domain": ["api", "endpoint", "cli", "tool", "browser", "official", "공식", "조회", "search"],
    "project-local": ["repo", "project", "build", "test", "git", "workspace", "프로젝트", "레포"],
    "model-harness": ["claude", "codex", "gpt", "gemini", "model", "prompt", "CLAUDE.md", "AGENTS.md", "instruction", "지침"],
    "cost-external-api": ["cost", "비용", "paid", "api", "external", "외부", "전송", "jev", "typesafe"],
}

CONFLICT_PAIRS = [
    ("always", "never"), ("항상", "절대"), ("무조건", "금지"),
    ("auto", "approval"), ("자동", "승인"), ("delete", "keep"), ("삭제", "유지"),
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def classify(text: str) -> list[str]:
    low = text.lower()
    cats = []
    for cat, terms in CATEGORIES.items():
        if any(t.lower() in low for t in terms):
            cats.append(cat)
    return cats or ["uncategorized"]


def scope_rank(scope: str) -> int:
    return {"global": 0, "project": 1, "skill": 2, "telegram-skill": 2, "mcp": 2}.get(scope, 3)


def excerpt_map(records):
    out = defaultdict(list)
    seen = set()
    for r in records:
        if r.get("error"):
            continue
        for field in ("strong_lines", "policy_lines", "model_lines", "imports"):
            for hit in r.get(field, []):
                text = hit.get("text", "").strip()
                if not text:
                    continue
                key = re.sub(r"\s+", " ", text.lower())
                if text.startswith('#'):
                    continue
                sig = (key, r["path"], hit.get("line"), text)
                if sig in seen:
                    continue
                seen.add(sig)
                out[key].append({"path": r["path"], "scope": r["scope"], "line": hit.get("line"), "text": text, "field": field})
    return out


def recommendation_for(scopes: set[str], cats: list[str]) -> str:
    # Similarity alone cannot establish authority, obsolescence or safe deletion.
    return "Review needed: confirm actual loading scope, official guidance and observed behavior. Duplication alone does not justify removal."


def has_conflict(texts: list[str]) -> bool:
    joined = "\n".join(texts).lower()
    return any(a in joined and b in joined for a, b in CONFLICT_PAIRS)


def main() -> int:
    inv = load_json(INVENTORY)
    records = inv.get("records", [])
    candidates = []

    # Exact/near-exact repeated sentence fingerprints.
    owners_by_fp = defaultdict(list)
    for r in records:
        for fp in r.get("fingerprints", {}):
            owners_by_fp[fp].append({"path": r.get("path"), "scope": r.get("scope"), "text": fp})
    for fp, owners in owners_by_fp.items():
        paths = {o["path"] for o in owners}
        scopes = {o["scope"] for o in owners}
        if len(paths) < 2:
            continue
        cats = classify(fp)
        candidates.append({
            "type": "duplicate-sentence",
            "risk": "low" if len(scopes) == 1 else "medium",
            "categories": cats,
            "scopes": sorted(scopes, key=scope_rank),
            "evidence": owners[:20],
            "recommendation": recommendation_for(scopes, cats),
            "approval_required": True,
            "auto_edit_allowed": False,
        })

    # Repeated policy/model excerpts.
    for key, hits in excerpt_map(records).items():
        paths = {h["path"] for h in hits}
        scopes = {h["scope"] for h in hits}
        if len(paths) < 2:
            continue
        texts = [h["text"] for h in hits]
        cats = classify("\n".join(texts))
        signal = has_conflict(texts)
        conflict = False  # Keyword co-occurrence is not semantic conflict evidence.
        candidates.append({
            "type": "policy-excerpt-overlap",
            "keyword_signal": signal,
            "conflict_verified": False,
            "risk": "high" if conflict else ("medium" if len(scopes) > 1 else "low"),
            "categories": cats,
            "scopes": sorted(scopes, key=scope_rank),
            "evidence": hits[:20],
            "recommendation": "Conflict candidate: compare exact authority and do not auto-resolve." if conflict else recommendation_for(scopes, cats),
            "approval_required": True,
            "auto_edit_allowed": False,
        })

    # Sort for readability.
    candidates.sort(key=lambda c: ({"high": 0, "medium": 1, "low": 2}.get(c["risk"], 3), c["type"], ",".join(c["categories"])))
    report = {"candidate_count": len(candidates), "candidates": candidates[:500]}
    JSON_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# Instruction Overlap Analysis", "", f"Candidates: {len(candidates)}", ""]
    for i, c in enumerate(candidates[:80], 1):
        lines += [f"## {i}. {c['type']} — {c['risk']}", "", f"- Categories: {', '.join(c['categories'])}", f"- Scopes: {', '.join(c['scopes'])}", f"- Approval required: {c['approval_required']}", f"- Auto-edit allowed: {c['auto_edit_allowed']}", f"- Recommendation: {c['recommendation']}", "", "Evidence:", ""]
        for e in c["evidence"][:6]:
            loc = f"{e.get('path')}:{e.get('line')}" if e.get("line") else e.get("path")
            lines.append(f"- `{loc}` — {e.get('text', '')[:220]}")
        lines.append("")
    MD_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"candidates: {len(candidates)}")
    print(f"reports: {JSON_REPORT.relative_to(ROOT)}, {MD_REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
