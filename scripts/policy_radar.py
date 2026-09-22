#!/usr/bin/env python3
"""Convenience runner for the Policy Radar CLI."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable or "python3"

COMMANDS = {
    "sources": ["scripts/check_sources.py", "--no-note"],
    "scan": ["scripts/scan_instructions.py"],
    "overlap": ["scripts/analyze_overlap.py"],
    "recommend": ["scripts/generate_recommendations.py"],
}


def run_step(name: str, extra: list[str] | None = None) -> int:
    cmd = [PY, *COMMANDS[name]]
    if extra:
        cmd.extend(extra)
    print(f"\n$ {' '.join(cmd)}", flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    ap = argparse.ArgumentParser(description="Policy Radar automation runner")
    sub = ap.add_subparsers(dest="command", required=True)

    sub.add_parser("sources", help="Check official source docs for changes")
    sub.add_parser("scan", help="Inventory instruction files")
    sub.add_parser("overlap", help="Analyze overlaps from the inventory report")
    sub.add_parser("recommend", help="Generate markdown recommendations from overlap analysis")
    sub.add_parser("all", help="Run sources, scan, overlap, and recommendation generation")

    args = ap.parse_args()
    order = ["sources", "scan", "overlap", "recommend"] if args.command == "all" else [args.command]
    for name in order:
        code = run_step(name)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
