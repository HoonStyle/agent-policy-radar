"""Offline regression tests; never scan the real user's home."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scanner', ROOT / 'scripts/scan_instructions.py')
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class TargetsTest(unittest.TestCase):
    def test_default_home_targets(self):
        paths = [
            '.claude/CLAUDE.md', '.codex/AGENTS.md', '.codex/AGENTS.override.md',
            'Documents/한글 project/CLAUDE.md', 'Documents/other/AGENTS.md',
            'Documents/dev/demo/CLAUDE.md', 'Documents/dev/demo/AGENTS.md',
            '.claude/skills/example/SKILL.md', '.codex/skills/example/SKILL.md',
            '.claude/plugins/cache/market/plugin/1.0/skills/example/SKILL.md',
            '.codex/plugins/cache/market/plugin/1.0/skills/example/SKILL.md',
        ]
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp).resolve()
            for relative in paths:
                p = home / relative
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('Fixture instructions only.', encoding='utf-8')
            # MCP/credential contents should not be needed for these targets.
            secret = home / '.claude/plugins/cache/market/plugin/1.0/settings.json'
            secret.write_text('{}', encoding='utf-8')
            config = json.loads((ROOT / 'data/instruction_targets.json').read_text(encoding='utf-8'))
            config['targets'] = [t for t in config['targets'] if t['path'].startswith('~')]
            config['globs'] = [g for g in config['globs'] if g['pattern'].startswith('~')]
            with patch.dict(os.environ, {'HOME': str(home), 'USERPROFILE': str(home)}):
                found = [p for _, p, _ in scanner.unique_paths(config)]
            self.assertEqual(set(found), {home / p for p in paths})
            self.assertEqual(len(found), len(set(found)))


if __name__ == '__main__':
    unittest.main()
