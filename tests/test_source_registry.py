import json
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def test_unique_official_sources(self):
        sources = json.loads((ROOT / 'data/source_registry.json').read_text(encoding='utf-8'))['sources']
        self.assertEqual(len(sources), len({s['id'] for s in sources}))
        self.assertEqual(len(sources), len({s['url'] for s in sources}))
        hosts = {'platform.claude.com', 'code.claude.com', 'developers.openai.com',
                 'cookbook.openai.com', 'modelcontextprotocol.io'}
        for source in sources:
            url = urlsplit(source['url'])
            self.assertEqual(url.scheme, 'https')
            self.assertIn(url.hostname, hosts)
            self.assertTrue(source['label'])

    def test_current_guidance_and_historical_label(self):
        sources = {s['id']: s for s in json.loads((ROOT / 'data/source_registry.json').read_text(encoding='utf-8'))['sources']}
        required = {'anthropic-release-notes', 'claude-opus55-prompting', 'claude-opus55-migration',
                    'openai-release-notes', 'openai-latest-model', 'openai-gpt6-sol',
                    'openai-gpt6-luna', 'openai-codex-models'}
        self.assertTrue(required <= sources.keys())
        self.assertIn('Historical reference', sources['openai-gpt5-prompting-guide']['label'])
