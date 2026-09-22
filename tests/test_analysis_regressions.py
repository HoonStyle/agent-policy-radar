import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import scan_instructions as scan
import analyze_overlap as analyze
import generate_recommendations as recommend
import check_sources as sources


class Regressions(unittest.TestCase):
    def test_source_statuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = root/'registry.json'
            registry.write_text('{"sources":[{"id":"fixture","url":"https://example.invalid"}]}', encoding='utf-8')
            with patch.multiple(sources, ROOT=root, REGISTRY=registry, STATE=root/'state.json', SNAP_DIR=root/'snapshots', REPORT=root/'report.json'), patch.object(sys, 'argv', ['sources', '--no-note']):
                for status, text in [('first-seen', 'a'), ('unchanged', 'a'), ('changed', 'b')]:
                    with patch.object(sources, 'fetch', return_value=(text, {})):
                        self.assertEqual(sources.main(), 0)
                    record = json.loads((root/'report.json').read_text(encoding='utf-8'))
                    self.assertEqual(record['results'][0]['status'], status)
                with patch.object(sources, 'fetch', side_effect=TimeoutError('fixture')):
                    self.assertEqual(sources.main(), 1)
                self.assertEqual(json.loads((root/'report.json').read_text(encoding='utf-8'))['results'][0]['status'], 'failed')

    def test_numbers_versions_and_conditions(self):
        a = 'Always wait 5 minutes before retrying version 1.2.3 requests.'
        for b in [a.replace('5', '10'), a.replace('1.2.3', '1.3.3'), a.replace('before', 'after')]:
            self.assertNotEqual(scan.sentence_fingerprints(a), scan.sentence_fingerprints(b))
        prefix = 'Always consider ' + 'context ' * 30
        records = [{'path': str(i), 'scope': 'skill', 'strong_lines': [{'line': 1, 'text': prefix + str(i)}]} for i in range(2)]
        self.assertEqual(len(analyze.excerpt_map(records)), 2)

    def test_no_credential_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / 'mcp.json'
            config.write_text('{"api_key":"FAKE_SECRET_ONLY"}', encoding='utf-8')
            out = root / 'inventory.json'
            with patch.object(scan, 'REPORT', out), patch.object(scan, 'ROOT', root), patch.object(scan, 'unique_paths', return_value=[('mcp', config, 'fixture')]), patch.object(sys, 'argv', ['scan']):
                scan.main()
            text = out.read_text(encoding='utf-8')
            self.assertNotIn('FAKE_SECRET_ONLY', text)
            self.assertTrue(json.loads(text)['records'][0]['excluded'])

    def test_no_false_conflict_and_current_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inv = root / 'inventory.json'
            analysis = root / 'analysis.json'
            line = 'Always ask approval; never delete files without approval.'
            inv.write_text(json.dumps({'records': [{'path': str(i), 'scope': 'skill', 'strong_lines': [{'line': 1, 'text': line}]} for i in range(2)]}), encoding='utf-8')
            with patch.multiple(analyze, ROOT=root, INVENTORY=inv, JSON_REPORT=analysis, MD_REPORT=root/'analysis.md'):
                analyze.main()
            data = json.loads(analysis.read_text(encoding='utf-8'))
            self.assertEqual(data['candidates'][0]['type'], 'policy-excerpt-overlap')
            self.assertNotEqual(data['candidates'][0]['risk'], 'high')
            with patch.multiple(recommend, ROOT=root, ANALYSIS=analysis, OUT_DIR=root/'recommendations'):
                recommend.main()
                current = root/'recommendations/current.json'
                old = json.loads(current.read_text(encoding='utf-8'))
                analysis.write_text('{"candidates":[]}', encoding='utf-8')
                recommend.main()
                new = json.loads(current.read_text(encoding='utf-8'))
                self.assertEqual(new['candidate_count'], 0)
                self.assertEqual(new['files'], [])
                self.assertNotEqual(old['run'], new['run'])
                self.assertTrue((root/'recommendations'/old['files'][0]).exists())
