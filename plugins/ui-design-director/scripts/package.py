#!/usr/bin/env python3
"""Validate local package boundaries and make a deterministic distribution ZIP."""
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package_files():
    files = [ROOT / name for name in ("plugin.json", "README.md", "SOURCES.md", "VERIFICATION.md", "LICENSE")]
    # npm omits .gitignore; it is useful in source ZIPs, not a runtime dependency.
    if (ROOT / ".gitignore").is_file():
        files.append(ROOT / ".gitignore")
    for folder in ("skills", "scripts", "tests", "docs", ".claude-plugin", ".codex-plugin"):
        files.extend(p for p in (ROOT / folder).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    for path in files:
        if not path.is_file() or path.is_symlink() or ROOT not in path.resolve().parents:
            raise ValueError("Missing or unsafe package member: " + str(path))
    return sorted(files)


def validate(files):
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest["name"]):
        raise ValueError("Invalid plugin name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        raise ValueError("Invalid package version")
    for folder in (".claude-plugin", ".codex-plugin"):
        adapter = json.loads((ROOT / folder / "plugin.json").read_text(encoding="utf-8"))
        for key in ("name", "version", "description", "author"):
            if adapter.get(key) != manifest.get(key):
                raise ValueError(folder + " diverges on " + key)
        if any(k in adapter for k in ("hooks", "mcpServers", "settings")):
            raise ValueError("Unexpected runtime side effects in skill-only package")
    if json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))["skills"] != "./skills/":
        raise ValueError("Invalid Codex skill root")
    for skill in ("design-director", "presentation-design", "document-design"):
        if not (ROOT / "skills" / skill / "SKILL.md").is_file():
            raise ValueError("Skill missing: " + skill)
    for path in files:
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                local = (path.parent / target.split("#")[0]).resolve()
                if ROOT not in local.parents or not local.exists():
                    raise ValueError(f"Broken or external local reference in {path.name}: {target}")
    return manifest


def main():
    files = package_files()
    manifest = validate(files)
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f'{manifest["name"]}-{manifest["version"]}.zip'
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(manifest["name"] + "/" + relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(digest + "  " + archive.name + "\n", encoding="utf-8")
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError("Archive integrity check failed")
    print(json.dumps({"archive": str(archive), "files": len(files), "bytes": archive.stat().st_size,
                      "sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
