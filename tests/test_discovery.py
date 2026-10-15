import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import discover_sources as d


class DiscoveryTests(unittest.TestCase):
    def test_typesafe_guidance_without_generic_model_keywords(self):
        index = 'https://docs.typesafe.ai/llms.txt'
        self.assertIn(index, d.INDEXES)
        text = ('[State](/concepts/state.md)\n'
                '[Primitives (Questions)](/primitives.md)\n'
                '[Confidence](/confidence.md)\n'
                '[Agent skill](/agent-skill.md)\n'
                '[Confidence](https://docs.typesafe.ai.evil.example/confidence)\n'
                '[Confidence](https://docs.typesafe.ai@evil.example/confidence)\n'
                '[Confidence](https://docs.typesafe.ai:444/confidence)\n'
                '[Legal](/legal.md)')
        result = d.candidates(text, index)
        self.assertEqual({r['title'] for r in result},
                         {'State', 'Primitives (Questions)', 'Confidence', 'Agent skill'})
        self.assertTrue(all(not r['verified'] for r in result))

    def test_typesafe_terms_do_not_broaden_other_provider_matching(self):
        self.assertEqual(d.candidates('[State](/state)\n[Confidence](/confidence)',
                                      d.INDEXES[0]), [])

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
