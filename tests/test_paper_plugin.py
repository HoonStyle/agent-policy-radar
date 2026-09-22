import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/paper-research'


class PaperPluginTests(unittest.TestCase):
    def test_optional_catalog_and_references(self):
        self.assertFalse((ROOT / 'skills/paper-research').exists())
        for name in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
            data = json.loads((ROOT / name).read_text(encoding='utf-8'))
            entries = [x for x in data['plugins'] if x['name'] == 'paper-research']
            self.assertEqual(len(entries), 1)
            source = entries[0]['source']
            self.assertEqual(source if isinstance(source, str) else source['path'], './plugins/paper-research')
        skill = PLUGIN / 'skills/paper-research/SKILL.md'
        text = skill.read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\nname: paper-research\n'))
        for relative in re.findall(r'\]\((references/[^)]+)\)', text):
            self.assertTrue((skill.parent / relative).is_file(), relative)
        self.assertNotIn('/Users/', text)

    def test_no_automatic_runtime(self):
        for name in ('plugin.json', '.claude-plugin/plugin.json'):
            manifest = json.loads((PLUGIN / name).read_text(encoding='utf-8'))
            for forbidden in ('hooks', 'mcpServers', 'dependencies'):
                self.assertNotIn(forbidden, manifest)
