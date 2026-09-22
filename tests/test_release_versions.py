"""Prevent releasing a new plugin with a stale marketplace version."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseVersionsTest(unittest.TestCase):
    def test_marketplace_and_plugin_versions_match(self):
        def load(name):
            return json.loads((ROOT / name).read_text(encoding='utf-8'))
        version = load('package.json')['version']
        self.assertEqual(load('plugin.json')['version'], version)
        self.assertEqual(load('.claude-plugin/plugin.json')['version'], version)
        market = load('.claude-plugin/marketplace.json')
        self.assertEqual(market['version'], version)
        for plugin in market['plugins']:
            base = ROOT / plugin['source']
            manifest = json.loads((base / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
            portable = json.loads((base / 'plugin.json').read_text(encoding='utf-8'))
            self.assertEqual(manifest['version'], portable['version'])
            if 'version' in plugin:
                self.assertEqual(plugin['version'], manifest['version'])

    def test_review_is_separate(self):
        skill = 'review-workflow'
        self.assertFalse((ROOT / 'skills' / skill).exists())
        self.assertTrue((ROOT / 'plugins' / skill / 'skills' / skill / 'SKILL.md').is_file())
        for file in ('.claude-plugin/plugin.json', 'plugin.json'):
            data = json.loads((ROOT / file).read_text(encoding='utf-8'))
            self.assertNotIn('dependencies', data)
        codex = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        entries = [p for p in codex['plugins'] if p['name'] == skill]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['source']['path'], './plugins/review-workflow')


if __name__ == '__main__':
    unittest.main()
