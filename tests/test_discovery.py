import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import discover_sources as d


class DiscoveryTests(unittest.TestCase):
    def test_links_and_boundaries(self):
        text = '[Model migration](/docs/migration)\n[Model migration](/docs/migration#x)\n[Prompt](https://evil.example/a)\n[Prompt](https://code.claude.com@evil.example/a)\n[Home](/home)'
        result = d.candidates(text, d.INDEXES[0])
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0]['verified'])

    def test_history_and_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(d, 'INDEXES', [d.INDEXES[0]]), patch.object(d, 'fetch', return_value=('[New model](/docs/model)', d.INDEXES[0])):
                self.assertEqual(d.discover(tmp), 0)
                self.assertEqual(d.discover(tmp), 0)
            reports = [json.loads(p.read_text(encoding='utf-8')) for p in Path(tmp).glob('*/report.json')]
            self.assertEqual({r['candidates'][0]['status'] for r in reports}, {'first-seen', 'previously-seen'})
            with patch.object(d, 'INDEXES', [d.INDEXES[0]]), patch.object(d, 'fetch', side_effect=TimeoutError('timeout')):
                self.assertEqual(d.discover(tmp), 1)
            self.assertEqual(len(list(Path(tmp).glob('*/report.json'))), 3)
