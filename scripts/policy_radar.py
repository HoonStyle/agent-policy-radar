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
    "discover": ["scripts/discover_sources.py"],
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

    sub.add_parser("discover", help="Find new guidance candidates in official documentation indexes")
    sub.add_parser("sources", help="Check official source docs for changes")
    sub.add_parser("scan", help="Inventory instruction files")
    sub.add_parser("overlap", help="Analyze overlaps from the inventory report")
    sub.add_parser("recommend", help="Generate markdown recommendations from overlap analysis")
    sub.add_parser("all", help="Run sources, scan, overlap, and recommendation generation")

    review = sub.add_parser("review", help="Draft a prompt cleanup diff without modifying the original")
    review.add_argument("target")
    review.add_argument("--proposal")
    review.add_argument("--output-dir")

    args = ap.parse_args()
    if args.command == "review":
        from review_prompt import main as review_main
        parameters = [args.target]
        for key in ("proposal", "output_dir"):
            value = getattr(args, key)
            if value:
                parameters.extend(["--" + key.replace("_", "-"), value])
        return review_main(parameters)
    order = ["discover", "sources", "scan", "overlap", "recommend"] if args.command == "all" else [args.command]
    for name in order:
        code = run_step(name)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    from audit import execute
    raise SystemExit(execute(sys.argv[1:], main))
