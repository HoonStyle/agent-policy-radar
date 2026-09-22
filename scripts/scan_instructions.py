#!/usr/bin/env python3
"""Inventory global/project/skill/MCP instruction files."""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "data" / "instruction_targets.json"
REPORT = ROOT / "reports" / "instruction_inventory.json"

STRONG_WORDS = ["always", "never", "must", "do not", "무조건", "항상", "절대", "반드시", "금지"]
POLICY_TERMS = ["approval", "approve", "승인", "credential", "api key", "secret", "비공개", "외부 전송", "destructive", "파괴", "telegram", "mcp", "CLAUDE.md", "AGENTS.md"]
MODEL_TERMS = ["claude", "codex", "gpt", "gemini", "astra", "sonnet", "opus", "haiku"]


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def expand_path(p: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(p))).resolve()


def unique_paths(config: dict) -> list[tuple[str, Path, str]]:
    seen = set()
    out = []
    for t in config.get("targets", []):
        path = expand_path(t["path"])
        key = str(path)
        if path.is_file() and key not in seen:
            seen.add(key)
            out.append((t.get("scope", "unknown"), path, t.get("id", path.name)))
    for g in config.get("globs", []):
        pattern = os.path.expandvars(os.path.expanduser(g["pattern"]))
        for match in glob.glob(pattern):
            path = Path(match).resolve()
            key = str(path)
            if path.is_file() and key not in seen:
                seen.add(key)
                out.append((g.get("scope", "unknown"), path, path.stem))
    return out


def lines_matching(lines: list[str], terms: list[str]) -> list[dict]:
    out = []
    for i, line in enumerate(lines, 1):
        low = line.lower()
        hits = [t for t in terms if t.lower() in low]
        if hits:
            out.append({"line": i, "hits": hits, "text": line.strip()})
    return out


def sentence_fingerprints(text: str) -> Counter:
    chunks = text.splitlines()
    c = Counter()
    for chunk in chunks:
        norm = re.sub(r"\s+", " ", chunk.strip().lower())
        # Preserve numbers, versions, operators and condition punctuation.
        norm = norm.strip()
        if len(norm) >= 35:
            c[norm] += 1
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-bytes", type=int, default=1_000_000)
    args = ap.parse_args()

    config = load_json(TARGETS, {"targets": [], "globs": []})
    records = []
    all_fp = Counter()

    for scope, path, tid in unique_paths(config):
        # MCP config values may contain credentials. Do not read or excerpt them.
        # Also reject arbitrary cache/config file types regardless of their label.
        if scope == "mcp" or path.suffix.lower() != ".md":
            records.append({"id": tid, "scope": scope, "path": str(path),
                            "excluded": True, "reason": "configuration values are not instruction text"})
            continue
        try:
            raw = path.read_bytes()
            truncated = len(raw) > args.max_bytes
            text = raw[: args.max_bytes].decode("utf-8", "replace")
            lines = text.splitlines()
            fp = sentence_fingerprints(text)
            all_fp.update(fp)
            records.append({
                "id": tid,
                "scope": scope,
                "path": str(path),
                "relative_path": str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path),
                "bytes": len(raw),
                "truncated": truncated,
                "line_count": len(lines),
                "heading_count": sum(1 for l in lines if l.lstrip().startswith("#")),
                "strong_lines": lines_matching(lines, STRONG_WORDS),
                "policy_lines": lines_matching(lines, POLICY_TERMS),
                "model_lines": lines_matching(lines, MODEL_TERMS),
                "imports": lines_matching(lines, ["@AGENTS.md", "@CLAUDE.md", "import", "읽", "load"]),
                "fingerprints": dict(fp.most_common(200)),
            })
        except Exception as e:  # noqa: BLE001
            records.append({"id": tid, "scope": scope, "path": str(path), "error": repr(e)})

    duplicate_sentences = {k: v for k, v in all_fp.items() if v > 1}
    report = {
        "target_count": len(records),
        "records": records,
        "duplicate_sentence_count": len(duplicate_sentences),
        "duplicate_sentences": dict(Counter(duplicate_sentences).most_common(300)),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"scanned {len(records)} instruction files")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
