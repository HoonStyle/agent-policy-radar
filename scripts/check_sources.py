#!/usr/bin/env python3
"""Check official model/harness documentation for content changes.

Outputs:
- data/source_state.json
- data/snapshots/<source-id>.txt
- reports/source_changes.json
- optional sources/YYYY-MM-DD-source-changes.md when changes are detected
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "source_registry.json"
STATE = ROOT / "data" / "source_state.json"
SNAP_DIR = ROOT / "data" / "snapshots"
REPORT = ROOT / "reports" / "source_changes.json"

KEYWORDS = [
    "CLAUDE.md", "AGENTS.md", "prompt", "instruction", "instructions",
    "model", "reasoning", "Codex", "Claude Code", "MCP", "tool", "tools",
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def today() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()


def normalize_text(raw: str, content_type: str | None) -> str:
    if "html" in (content_type or "").lower() or raw.lstrip().startswith("<!DOCTYPE"):
        raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.I | re.S)
        raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip() + "\n"


def fetch(url: str, timeout: int) -> tuple[str, dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": "agent-policy-radar/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read(5_000_000).decode("utf-8", "replace")
        headers = {k.lower(): v for k, v in r.headers.items()}
        headers["status"] = str(getattr(r, "status", ""))
        return normalize_text(body, headers.get("content-type")), headers


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def keyword_hits(text: str) -> list[str]:
    low = text.lower()
    return sorted({k for k in KEYWORDS if k.lower() in low})


def excerpt_changed_keywords(text: str, limit: int = 12) -> list[str]:
    lines = []
    for line in text.splitlines():
        if any(k.lower() in line.lower() for k in KEYWORDS):
            clean = line.strip()
            if clean:
                lines.append(clean[:220])
        if len(lines) >= limit:
            break
    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--write-note-on-first", action="store_true")
    ap.add_argument("--no-note", action="store_true")
    args = ap.parse_args()

    registry = load_json(REGISTRY, {"sources": []})
    state = load_json(STATE, {"sources": {}})
    state.setdefault("sources", {})
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    changes = []
    checked_at = now_iso()

    for src in registry.get("sources", []):
        sid = src["id"]
        url = src["url"]
        prev = state["sources"].get(sid, {})
        item = {"id": sid, "label": src.get("label", sid), "url": url, "kind": src.get("kind"), "checked_at": checked_at}
        try:
            text, headers = fetch(url, args.timeout)
            digest = sha256(text)
            old_digest = prev.get("sha256")
            changed = bool(old_digest and old_digest != digest)
            first_seen = not bool(old_digest)
            snap_path = SNAP_DIR / f"{sid}.txt"
            snap_path.write_text(text, encoding="utf-8")
            state["sources"][sid] = {
                **src,
                "sha256": digest,
                "etag": headers.get("etag"),
                "last_modified": headers.get("last-modified"),
                "content_type": headers.get("content-type"),
                "last_checked_at": checked_at,
                "snapshot": str(snap_path.relative_to(ROOT)),
                "keyword_hits": keyword_hits(text),
            }
            item.update({
                "ok": True,
                "changed": changed,
                "first_seen": first_seen,
                "old_sha256": old_digest,
                "new_sha256": digest,
                "etag": headers.get("etag"),
                "last_modified": headers.get("last-modified"),
                "keyword_hits": keyword_hits(text),
                "excerpts": excerpt_changed_keywords(text),
            })
            if changed or (first_seen and args.write_note_on_first):
                changes.append(item)
        except Exception as e:  # noqa: BLE001 - CLI report should continue
            item.update({"ok": False, "changed": False, "error": repr(e)})
            changes.append(item)

    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {"checked_at": checked_at, "changes": changes}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if changes and not args.no_note:
        note = ROOT / "sources" / f"{today()}-source-changes.md"
        lines = [f"# Source Changes — {today()}", "", f"Checked at: `{checked_at}`", ""]
        for c in changes:
            lines += [f"## {c['label']}", "", f"- URL: {c['url']}", f"- OK: {c.get('ok')}", f"- Changed: {c.get('changed')}", f"- First seen: {c.get('first_seen', False)}"]
            if c.get("error"):
                lines.append(f"- Error: `{c['error']}`")
            if c.get("keyword_hits"):
                lines.append(f"- Keyword hits: {', '.join(c['keyword_hits'])}")
            if c.get("excerpts"):
                lines += ["", "Relevant excerpt candidates:", ""]
                lines += [f"> {x}" for x in c["excerpts"]]
            lines.append("")
        lines += ["## Interpretation", "", "This is a source-change detection note. It does not approve edits to local instructions.", ""]
        note.write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {note.relative_to(ROOT)}")

    print(f"checked {len(registry.get('sources', []))} sources; changes/errors: {len(changes)}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
