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
            self.assertEqual(plugin['version'], version)


if __name__ == '__main__':
    unittest.main()
